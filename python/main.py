from mysql import engines, tables, inspectors
from flask import Flask, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy import select
from itertools import groupby


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
            *[column.label(str(column)) for column in books.c]
            ).select_from(
            users
            .join(rel, rel.c.user_id==users.c.id, isouter=True)
            .join(books, rel.c.book_id==books.c.id, isouter=True))
            ).all()]
        users = [dict(u._mapping) for u in session.execute(select(users.c).select_from(users)).all()]
    print(users_books)
    u_b = {}
    for k,v in groupby(sorted(users_books, key=lambda x:x['users.id']),key=lambda x:x['users.id']):
        u_b[k] = [{i:j for i,j in book.items() if 'book.' in i} for book in list(v)]
    for i,_ in enumerate(users):
        users[i]['books'] = u_b[users[i]['id']]
    return render_template('index.html', users=users)
        

        
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
