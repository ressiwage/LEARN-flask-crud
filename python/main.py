from mysql import engines, tables, inspectors
from flask import Flask, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from itertools import groupby
from datetime import datetime
import json

app = Flask(__name__)


@app.route('/table/<string:name>', methods=['POST'])
def _test(name):
    with Session(engines['library']) as session:
        js = request.get_json(silent=True)

@app.route('/', methods=['GET'])
def index():
    users = tables['library']['users']
    books = tables['library']['books']
    rel = tables['library']['r_u_b']
    with Session(engines['library']) as session:
        users_books = [dict(u._mapping) for u in session.execute(
            select(
            *[column.label(str(column)) for column in users.c],
            *[column.label(str(column)) for column in books.c],
            rel.c.take_ts.label('books.took'),
            rel.c.return_ts.label('books.returned')
            ).select_from(
            users
            .join(rel, rel.c.user_id==users.c.id)
            .join(books, rel.c.book_id==books.c.id))
            ).all()]
        users = [dict(u._mapping) for u in session.execute(select(users.c).select_from(users)).all()]
        books = [dict(b._mapping) for b in session.execute(select(books.c).select_from(books)).all()]
    u_b = {}
    for k,v in groupby(sorted(users_books, key=lambda x:x['users.id']),key=lambda x:x['users.id']):
        u_b[k] = [{i.replace('books.', ''):j for i,j in book.items()  if 'books.' in i} for book in list(v)]
    for i,_ in enumerate(users):
        users[i]['books'] = u_b.get(users[i]['id'])
    
    for i in range(len(users)):
        if users[i].get('books')!=None:
            users[i]['books_current'] = len([b for b in users[i]['books'] if b.get('returned')==None or b.get('returned') > datetime.now() ])
            users[i]['last_visit'] = max([max([b['took'] if b['took']!=None else datetime(1970,1,1), b['returned'] if b['returned']!=None else datetime(1970,1,1)]) for b in users[i]['books']]).strftime( "%d-%m-%Y")
            genres=[g['genre'] for g in users[i]['books']]
            users[i]['fav_genre'] = sorted([[g, genres.count(g)] for g in genres], key=lambda x:x[0])[-1][0]

            for j in range(len(users[i]['books'])):
                if users[i]['books'][j].get('took')!=None:
                    users[i]['books'][j]['took'] = users[i]['books'][j]['took'].strftime( "%d-%m-%Y")
                if users[i]['books'][j].get('returned')!=None:
                    users[i]['books'][j]['returned'] = users[i]['books'][j]['returned'].strftime("%d-%m-%Y")
        else:
            users[i]['books']=[]
    authors = sorted([[a, [b['author'] for b in books].count(a)] for a in [b['author'] for b in books]], key=lambda a:a[1])
    genres = sorted([[a, [b['genre'] for b in books].count(a)] for a in [b['genre'] for b in books]], key=lambda a:a[1])

    mostreadablegenres=[]
    for i in genres:
        if i[0] not in mostreadablegenres:
            mostreadablegenres.append(i[0])
    
    
    mostreadable = authors[0][0]
    return render_template('index.html', 
                           users=users, 
                           totalbooks=len(books), 
                           totalusers=len(users), 
                           mostreadable=mostreadable, 
                           mostreadablegenres=mostreadablegenres[::-1])
        
@app.route('/clients', methods=['GET'])
def users():
    users = tables['library']['users']
    with Session(engines['library']) as session:
        users = [dict(u._mapping) for u in session.execute(select(users.c).select_from(users)).all()]
    print(users)
    return render_template('clients.html', users=users)
        
@app.route('/books', methods=['GET'])
def books():
    books = tables['library']['books']
    with Session(engines['library']) as session:
        books = [dict(u._mapping) for u in session.execute(select(books.c).select_from(books)).all()]
    return render_template('books.html', books=books)

@app.route('/journal', methods=['GET'])
def journal():
    users = tables['library']['users']
    books = tables['library']['books']
    rel = tables['library']['r_u_b']
    with Session(engines['library']) as session:
        users_books = [dict(u._mapping) for u in session.execute(
            select(
            *[column.label(str(column)) for column in users.c],
            *[column.label(str(column)) for column in books.c],
            rel.c.take_ts.label('books.took'),
            rel.c.return_ts.label('books.returned'),
            rel.c.id.label('r_id')
            ).select_from(
            users
            .join(rel, rel.c.user_id==users.c.id)
            .join(books, rel.c.book_id==books.c.id))
            ).all()]
        users= [dict(u._mapping) for u in session.execute(select(users.c).select_from(users)).all()]
        books=[dict(u._mapping) for u in session.execute(select(books.c).select_from(books)).all()]
    return render_template('journal.html', relations = users_books, users=users,books=books)

@app.route('/edit-<string:table>-<int:id>', methods=['POST'])
def edit(table, id):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        js = request.form
        if table=='r_u_b':
            take = js['t'] if js['t']!='' else None
            ret = js['r'] if js['r']!='' else None
            session.execute(update(t).values(user_id=js['c'].split('|')[0], book_id=js['b'].split('|')[0], take_ts=take, return_ts=ret).where(t.c.id==id))
        if table=='users':
            session.execute(update(t).values(name=js['n']).where(t.c.id==id))
        if table=='books':
            session.execute(update(t).values(name=js['n'], author=js['a'], genre=js['g']).where(t.c.id==id))
        session.commit()
    return {'code':'200'}

@app.route('/create-<string:table>', methods=['POST'])
def create(table):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        js = request.form
        if table=='r_u_b':
            take = js['t'] if js['t']!='' else None
            ret = js['r'] if js['r']!='' else None
            d = {'user_id':js['c'].split('|')[0], 'book_id':js['b'].split('|')[0], 'take_ts':take, 'return_ts':ret}
            session.execute(insert(t).values(**{i:j for i,j in d.items() if j!=None}))
        if table=='users':
            session.execute(insert(t).values(name=js['n']))
        if table=='books':
            session.execute(insert(t).values(name=js['n'], author=js['a'], genre=js['g']))
        session.commit()
    return {'code':'200'}

@app.route('/delete-<string:table>-<int:id>', methods=['POST'])
def delete(table, id):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        session.execute(t.delete().where(t.c.id==id))
        session.commit()
    return {'code':'200'}
    
# session.execute(insert(t).values().where(t.c.id==id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
