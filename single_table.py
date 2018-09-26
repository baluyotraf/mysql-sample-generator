from mysql import *
from generators import *
import os
import random
import string


DIR_NAME = os.path.dirname(os.path.abspath(__file__))
TABLE_NAME = 'employees'
TABLE_COLUMNS = [
    Column('id', Column.INT, Column.AUTO_INCREMENT, Column.PRIMARY_KEY),
    Column('first_name', Column.STRING(), Column.NOT_NULL),
    Column('last_name', Column.STRING(), Column.NOT_NULL),
    Column('middle_name', Column.STRING(), Column.NOT_NULL),
    Column('age', Column.INT, Column.NOT_NULL),
    Column('mobile_no', Column.STRING(), Column.NOT_NULL),
    Column('salary', Column.INT, Column.NOT_NULL),
    Column('level', Column.INT, Column.NOT_NULL),
]
INSERT_COLUMN = [c.name for c in TABLE_COLUMNS if c.name != 'id']
DATA_COUNT = 1000


def gint():
    return generate_integer(0, 100)


def gstr():
    return generate_alphanum_string(5)


def values_generator(count):
    columns = [c for c in TABLE_COLUMNS if c.name != 'id']
    for _ in range(count):
        yield [gint() if c.dtype == Column.INT else gstr()
               for c in columns]


def write_line(file, string):
    file.write(string + '\n')


if __name__ == '__main__':
    seed = input('Enter a seed: ')
    seed = seed.lower()
    random.seed(seed)

    a, b = sorted([gint(), gint()])
    x, y = sorted(random.choices(string.ascii_lowercase, k=2))

    print('A:', a, 'B:', b)
    print('X:', x, 'Y:', y)

    db = Database(seed)
    table = Table(TABLE_NAME, TABLE_COLUMNS)

    output_path = os.path.join(DIR_NAME, seed + '.sql')
    with open(output_path, 'w') as file:
        write_line(file, db.create())
        write_line(file, db.use())
        write_line(file, table.create())
        write_line(file, table.insert(INSERT_COLUMN, values_generator(DATA_COUNT)))

