from mysql import engines, tables, inspectors
from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select


app = Flask(__name__)


@app.route('/table/<string:name>', methods=['POST'])
def get_table(name):
    with Session(engines['library']) as session:
        js = request.get_json(silent=True)

@app.route('/', methods=['GET'])
def get_table(name):
    table = tables['library'][name]
    with Session(engines['library']) as session:
        data = [i._mapping for i in session.execute(select(table.c).select_from(table)).all()]
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
