_INDENT = '    '


def _process_name(name):
    return '`' + name + '`'


class Database:

    __create__ = 'CREATE DATABASE {name};'
    __use__ = 'USE {name};'

    def __init__(self, name):
        self.name = name

    def create(self):
        return self.__create__.format(name=_process_name(self.name))

    def use(self):
        return self.__use__.format(name=_process_name(self.name))


class Table:

    __create__ = 'CREATE TABLE {name} (\n{columns}\n);'
    __insert__ = 'INSERT INTO {name}({col_names})\nVALUES\n{values}\n;'

    def __init__(self, name, col_mods):
        self.name = name
        self.col_mods = col_mods

    def create(self):
        column_defs = ',\n'.join([_INDENT + str(c) for c in self.col_mods])
        return self.__create__.format(name=_process_name(self.name),
                                      columns=column_defs)

    # noinspection PyMethodMayBeStatic
    def _process_value(self, value):
        if value is None:
            return 'null'
        elif isinstance(value, str):
            return "'" + value + "'"
        else:
            return str(value)

    def _process_values(self, values):
        values = [self._process_value(v) for v in values]
        values = ', '.join(values)
        return _INDENT + '(' + values + ')'

    def insert(self, columns, values):
        col_names = [c.name if isinstance(c, Column) else c for c in columns]
        col_names = ', '.join([_process_name(cn) for cn in col_names])
        values = ',\n'.join([self._process_values(vs) for vs in values])
        return self.__insert__.format(name=_process_name(self.name),
                                      col_names=col_names,
                                      values=values)


class Column:

    INT = 'INT'
    PRIMARY_KEY = 'PRIMARY KEY'
    AUTO_INCREMENT = 'AUTO_INCREMENT'
    NOT_NULL = 'NOT NULL'
    STRING = lambda chars=255: 'VARCHAR({})'.format(chars)

    def __init__(self, name, dtype, *mods):
        self.name = name
        self.dtype = dtype
        self.mods = mods

    def __str__(self):
        details_list = [_process_name(self.name), self.dtype]
        details_list.extend(self.mods)
        return ' '.join(details_list)


class ForeignKey:

    __sql__ = 'FOREIGN KEY ({col_name})\n' + \
              _INDENT * 2 + 'REFERENCES {ptable}({pcol_name})'

    def __init__(self, col_name, ptable, pcol_name):
        self.col_name = col_name
        self.ptable = ptable
        self.pcol_name = pcol_name

    def __str__(self):
        return self.__sql__.format(col_name=_process_name(self.col_name),
                                   ptable=_process_name(self.ptable),
                                   pcol_name=_process_name(self.pcol_name))


if __name__ == '__main__':
    db = Database('db')
    print(db.create())
    print(db.use())
    cols = [
        Column('id', Column.INT, Column.PRIMARY_KEY, Column.AUTO_INCREMENT),
        Column('name', Column.STRING())
    ]
    tbl = Table('tbl', cols)
    print(tbl.create())
    col_names = ['id', 'name']
    values = [[1, 'raf'], [2, 'Arietta']]
    print(tbl.insert(col_names, values))
    print(ForeignKey('author_id', 'tbl', 'id'))

