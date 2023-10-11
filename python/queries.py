from enum import Enum
from sqlalchemy import select, update, insert
from mysql import tables

users = tables['library']['users']
books = tables['library']['books']
rel = tables['library']['r_u_b']


class Queries(Enum):
    select_books_and_users = select(
                *[column.label(str(column)) for column in users.c],
                *[column.label(str(column)) for column in books.c],
                rel.c.take_ts.label('books.took'),
                rel.c.return_ts.label('books.returned'),
                rel.c.id.label('r_id')
            ).select_from(
                users
                .join(rel, rel.c.user_id == users.c.id)
                .join(books, rel.c.book_id == books.c.id))

    def edit_table(table_name, json, table, id, session):
        if table_name == 'r_u_b':
            take = json['t'] if json['t'] != '' else None
            ret = json['r'] if json['r'] != '' else None
            session.execute(update(table).values(user_id=json['c'].split('|')[0], book_id=json['b'].split(
                '|')[0], take_ts=take, return_ts=ret).where(table.c.id == id))
        if table_name == 'users':
            session.execute(update(table).values(name=json['n']).where(table.c.id == id))
        if table_name == 'books':
            session.execute(update(table).values(
                name=json['n'], author=json['a'], genre=json['g']).where(table.c.id == id))
    
    def create_entry(table_name, json, table, session):
        if table_name == 'r_u_b':
            take = json['t'] if json['t'] != '' else None
            ret = json['r'] if json['r'] != '' else None
            d = {'user_id': json['c'].split('|')[0], 'book_id': json['b'].split('|')[
                0], 'take_ts': take, 'return_ts': ret}
            session.execute(insert(table).values(
                **{i: j for i, j in d.items() if j is not None}))
        if table_name == 'users':
            session.execute(insert(table).values(name=json['n']))
        if table_name == 'books':
            session.execute(insert(table).values(
                name=json['n'], author=json['a'], genre=json['g']))

    def delete_entry(t, id, session):
        session.execute(t.delete().where(t.c.id == id))