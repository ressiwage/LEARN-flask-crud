from mysql import engines, tables, inspectors
from flask import Flask, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy import select
from itertools import groupby
from datetime import datetime

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
    u_b = {}
    for k,v in groupby(sorted(users_books, key=lambda x:x['users.id']),key=lambda x:x['users.id']):
        u_b[k] = [{i.replace('books.', ''):j for i,j in book.items()  if 'books.' in i} for book in list(v)]
    for i,_ in enumerate(users):
        users[i]['books'] = u_b.get(users[i]['id'])
    
    for i in range(len(users)):
        if users[i].get('books')!=None:
            for j in range(len(users[i]['books'])):
                if users[i]['books'][j].get('took')!=None:
                    users[i]['books'][j]['took'] = users[i]['books'][j]['took'].strftime( "%d-%m-%Y")
                if users[i]['books'][j].get('returned')!=None:
                    users[i]['books'][j]['returned'] = users[i]['books'][j]['returned'].strftime("%d-%m-%Y")
        else:
            users[i]['books']=[]
    
    print(users)
    return render_template('index.html', users=users)
        
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
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
