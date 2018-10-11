from mysql import *
from generators import *
import os
import random
import string


DIR_NAME = os.path.dirname(os.path.abspath(__file__))
PARENT_TABLE = Table(name='authors',
                     col_mods=[
                         Column('id', Column.INT, Column.AUTO_INCREMENT, Column.PRIMARY_KEY),
                         Column('first_name', Column.STRING(), Column.NOT_NULL),
                         Column('last_name', Column.STRING(), Column.NOT_NULL),
                     ])

CHILD_TABLE = Table(name='books',
                    col_mods=[
                        Column('id', Column.INT, Column.AUTO_INCREMENT, Column.PRIMARY_KEY),
                        Column('title', Column.STRING(), Column.NOT_NULL),
                        Column('pages', Column.INT, Column.NOT_NULL),
                        Column('author_id', Column.INT),
                        ForeignKey('author_id', 'authors', 'id')
                    ])
DATA_COUNT = 200
CHILD_MULTIPLIER = 5


def gfid():
    id = random.randint(1, DATA_COUNT+1)
    if id == DATA_COUNT+1:
        return None
    else:
        return id


def gint():
    return generate_integer(0, 100)


def gstr():
    return generate_alphanum_string(5)


def data_generator(column):
    if column.name.endswith('_id'):
        return gfid()
    elif column.dtype == Column.INT:
        return gint()
    else:
        return gstr()


def row_generator(count, col_mods):
    columns = [c for c in col_mods
               if isinstance(c, Column) and c.name != 'id']
    data = [[data_generator(c) for c in columns] for _ in range(count)]
    return columns, data


def write_line(file, string):
    file.write(string + '\n')


if __name__ == '__main__':
    seed = input('Enter a seed: ')
    seed = seed.lower()
    random.seed(seed + 'multi')

    a, b = sorted([gint(), gint()])
    x, y = sorted(random.choices(string.ascii_lowercase, k=2))

    print('A:', a, 'B:', b)
    print('X:', x, 'Y:', y)

    db = Database(seed)
    ptable = PARENT_TABLE
    ctable = CHILD_TABLE

    output_path = os.path.join(DIR_NAME, seed + '.sql')
    with open(output_path, 'w') as file:
        write_line(file, db.create())
        write_line(file, db.use())
        write_line(file, ptable.create())
        write_line(file, ctable.create())
        write_line(file, ptable.insert(*row_generator(DATA_COUNT, ptable.col_mods)))
        write_line(file, ctable.insert(*row_generator(DATA_COUNT*CHILD_MULTIPLIER, ctable.col_mods)))
    input()
