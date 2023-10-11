from mysql import engines, tables
from flask import Flask, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy import select
from utils import result_to_list
from queries import Queries
from adapter import Adapter

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    users = tables['library']['users']
    books = tables['library']['books']
    with Session(engines['library']) as session:
        users_books = result_to_list(session.execute(
            Queries.select_books_and_users.value))
        users = result_to_list(session.execute(
            select(users.c).select_from(users)))
        books = result_to_list(session.execute(
            select(books.c).select_from(books)))

    return render_template('index.html',
                           users=users,
                           totalbooks=len(books),
                           totalusers=len(users),
                           **Adapter.make_json_for_index(users, books, users_books))


@app.route('/clients', methods=['GET'])
def users():
    users = tables['library']['users']
    with Session(engines['library']) as session:
        users = result_to_list(session.execute(
            select(users.c).select_from(users)))
    return render_template('clients.html', users=users)


@app.route('/books', methods=['GET'])
def books():
    books = tables['library']['books']
    with Session(engines['library']) as session:
        books = result_to_list(session.execute(
            select(books.c).select_from(books)))
    return render_template('books.html', books=books)


@app.route('/journal', methods=['GET'])
def journal():
    users = tables['library']['users']
    books = tables['library']['books']
    with Session(engines['library']) as session:
        users_books = result_to_list(session.execute(
            Queries.select_books_and_users.value))
        users = result_to_list(session.execute(
            select(users.c).select_from(users)))
        books = result_to_list(session.execute(
            select(books.c).select_from(books)))
    return render_template('journal.html', relations=users_books, users=users, books=books)


@app.route('/edit-<string:table>-<int:id>', methods=['POST'])
def edit(table, id):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        js = request.form
        Queries.edit_table(table, js, t, id, session)
        session.commit()
    return {'code': '200'}


@app.route('/create-<string:table>', methods=['POST'])
def create(table):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        js = request.form
        Queries.create_entry(table, js, t, session)
        session.commit()
    return {'code': '200'}


@app.route('/delete-<string:table>-<int:id>', methods=['POST'])
def delete(table, id):
    with Session(engines['library']) as session:
        t = tables['library'][table]
        Queries.delete_entry(t, id, session)
        session.commit()
    return {'code': '200'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
