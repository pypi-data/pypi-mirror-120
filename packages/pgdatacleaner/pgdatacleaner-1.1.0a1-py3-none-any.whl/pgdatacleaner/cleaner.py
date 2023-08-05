import argparse
import csv
import json
import logging
import random
from collections import defaultdict, namedtuple
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from threading import Lock

import faker
from slugify import slugify

logging.basicConfig()
LOG = logging.getLogger(__name__)
FAKER = faker.Faker()
SERIALS = {}
SERIAL_LOCK = Lock()


def tla(*_):
    c = "QWERTYUIOPLKJHGFDSAMNBVCXZ"
    return "".join(random.choice(c) for _ in range(5))


def serial(name, seed=0):
    if name not in SERIALS:
        SERIALS[name] = seed

    def cap(_):
        with SERIAL_LOCK:
            SERIALS[name] += 1
            return SERIALS[name]

    return cap


def random_slug(*_):
    c = "QWERTYUIOPLKJHGFDSAMNBVCXZ"
    return "".join(random.choice(c) for _ in range(15))


def slug(args):

    if not args:
        return random_slug

    def slug_with_args(field, row):
        return slugify(row[args[0]])

    return slug_with_args


def generic(fn):
    """Helper for generic faker functions that take no arguments"""

    def fake_maker(*args):
        @wraps(fn)
        def faker(field, row):
            return fn()

        return faker

    return fake_maker


FieldMapSpec = namedtuple("FieldMapSpec", "col spec mapper")


class RowMapper:
    def __init__(self, piis_for_table):
        """Sort column mappers according to dependencies"""
        self.mappers = []
        remaining = dict(piis_for_table.items())
        added = set()
        count = len(remaining)
        while remaining:
            for col, (spec, mapper) in remaining.items():
                depends = [d for d in spec["depends"].split(",") if d]
                if not depends or all([dep in added for dep in depends]):
                    self.mappers.append(FieldMapSpec(col, spec, mapper))
                    added.add(col)
            for v in added:
                del remaining[v]
            assert len(remaining) < count
            count = len(remaining)

    def mask(self, row):
        for mapspec in self.mappers:
            row[mapspec.col] = mapspec.mapper(row[mapspec.col], row)
        return row


FAKERS = {
    "person_firstname": generic(FAKER.first_name),
    "person_familyname": generic(FAKER.last_name),
    "person_name": generic(FAKER.name),
    "tla": tla,
    "business_name": generic(FAKER.company),
    "slug": slug,
    "null": generic(lambda: None),
    "text_short": generic(FAKER.sentence),
    "text": generic(FAKER.paragraph),
    "email": lambda _: FAKER.email(domain="example.com"),  # TODO
    "user_agent": lambda _: FAKER.user_agent(),
    "url": lambda _: FAKER.uri(),
    "url_image": lambda _: FAKER.image_url(),
    "phonenumber": lambda _: FAKER.msisdn()[:11],
    "address": lambda _: FAKER.address(),
    "city": lambda _: FAKER.city(),
    "zipcode": lambda _: FAKER.postcode(),
    "filename": lambda _: FAKER.file_name(),
    "inet_addr": lambda _: FAKER.ipv4(),  # TODO private?
    "username": slug,
    "int": lambda _: random.randint(0, 300000000),  # TODO: arg+default
    "password": slug,
    # TODO: arg+default instead?
    "serial": None,
}


def get_mapper(
    table_schema, table_name, column_name, data_type, pii_type, depends, args, **_
):
    if pii_type == "serial":
        return serial(f"{table_schema}.{table_name}.{column_name}", 200000000)
    else:
        return FAKERS[pii_type](args.split(","))


def get_piis(source_csv: str):
    source = csv.DictReader(source_csv, delimiter=";")
    tables: dict = defaultdict(dict)
    for line in source:

        if line["pii"] == "yes":
            try:
                mapper = get_mapper(**line)
                tables[f"{line['table_schema']}.{line['table_name']}"][
                    line["column_name"]
                ] = (line, mapper)
            except:
                LOG.exception(f"Erroring on '{line}'")
                raise
    return tables


def mask_pii(table: str, pii_spec, dsn, keepers):
    print(f"Executing {table}")
    row_mapper = RowMapper(pii_spec[table])
    if dsn.startswith("postgres"):
        import psycopg2

        conn = psycopg2.connect(dsn)
        read_cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        read_cursor.execute(
            f"""SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
                            FROM   pg_index i
                            JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                                 AND a.attnum = ANY(i.indkey)
                            WHERE  i.indrelid = '{table}'::regclass
                            AND    i.indisprimary;"""
        )
        write_cursor = conn.cursor()
        write_cursor.execute("SET CONSTRAINTS ALL DEFERRED")
        p = "%"
    else:
        import sqlite3

        conn = sqlite3.connect(dsn)
        conn.row_factory = sqlite3.Row
        read_cursor = conn.cursor()
        read_cursor.execute(
            f"SELECT name from pragma_table_info(?) WHERE pk=1", (table.split(".")[1],)
        )
        write_cursor = conn.cursor()
        p = "?"
    pks = [row[0] for row in read_cursor]
    if keepers is None:
        read_cursor.execute(f"SELECT * FROM {table}")
    else:
        read_cursor.execute(
            f"SELECT * FROM {table} WHERE {pks[0]} NOT IN ({p})", keepers
        )
    for row in read_cursor:

        new_row = row_mapper.mask({k: row[k] for k in row.keys()})
        where = " AND ".join((f"{colname}={p}") for colname in pks)
        replacements = ",".join((f"{colname}={p}") for colname in new_row.keys())
        new_values = [new_row[k] for k in new_row.keys()]
        old_values = [row[k] for k in pks]
        sql = f"UPDATE {table} SET {replacements} WHERE {where}"
        values = new_values + old_values
        try:
            write_cursor.execute(sql, values)
            assert write_cursor.rowcount == 1
        except Exception:
            LOG.exception(f"Table: {table}\n SQL: {sql}")
            raise
    conn.commit()
    LOG.info(f"{table} commited")


def clean(executors: int, filename: str, dburl: str, keep_filename: str):
    if not keep:
        keep = {}
    else:
        keep = json.load(open(keep))
    executor = ThreadPoolExecutor(max_workers=executors)
    tasks = []
    source_csv = open(filename).read()
    for table, pii_spec in get_piis(source_csv).items():

        if mappers:
            LOG.info(f"{table}:  masking {', '.join(mappers.keys())}")
            tasks.append(
                executor.submit(mask_pii, table, pii_spec, dburl, keep.get(table, None))
            )
        else:
            LOG.debug(f"{table}: not masking")

    completed = 0
    taskcount = len(tasks)
    LOG.debug(f"{taskcount} tasks submitted")
    for task in tasks:
        task.result()
        completed += 1
        LOG.debug(f"{completed}/{taskcount}")
    LOG.info("Done")


def main():

    parser = argparse.ArgumentParser(
        epilog=f"Available pii_types / fakes: {', '.join((key for key in sorted(FAKERS.keys())))}"
    )

    parser.add_argument(
        "-d",
        "--dburl",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
    )
    parser.add_argument(
        "--keep",
        type=str,
        help='JSON file mapping rows to not mask {"schema.table": ["pk1", "pk2"]}',
        default=None,
    )
    parser.add_argument(
        "--fixed",
        type=str,
        help='JSON file mapping fixed masks: {"schema.table": {"pk1": {"col": "val"}]}',
        default=None,
    )
    parser.add_argument("-e", "--executors", type=int, default=2)
    args = parser.parse_args()
    clean(
        executors=args.executors,
        filename=args.filename,
        dburl=args.dburl,
        keep_filename=args.keep,
    )


if __name__ == "__main__":
    main()
