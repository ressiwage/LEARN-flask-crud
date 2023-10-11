from itertools import groupby
from datetime import datetime
from enum import Enum


class Adapter(Enum):
    def make_json_for_index(users, books, users_books):
        u_b = {}
        for k, v in groupby(sorted(users_books, key=lambda x: x['users.id']), key=lambda x: x['users.id']):
            u_b[k] = [{i.replace('books.', ''): j for i, j in book.items(
            ) if 'books.' in i} for book in list(v)]
        for i, _ in enumerate(users):
            users[i]['books'] = u_b.get(users[i]['id'])

        for i in range(len(users)):
            if users[i].get('books') is not None:
                users[i]['books_current'] = len([b for b in users[i]['books'] if b.get(
                    'returned') is None or b.get('returned') > datetime.now()])
                users[i]['last_visit'] = max([max([b['took'] if b['took'] is not None else datetime(
                    1970, 1, 1), b['returned'] if b['returned'] is not None else datetime(1970, 1, 1)]) for b in users[i]['books']]).strftime("%d-%m-%Y")
                genres = [g['genre'] for g in users[i]['books']]
                users[i]['fav_genre'] = sorted(
                    [[g, genres.count(g)] for g in genres], key=lambda x: x[0])[-1][0]

                for j in range(len(users[i]['books'])):
                    if users[i]['books'][j].get('took') is not None:
                        users[i]['books'][j]['took'] = users[i]['books'][j]['took'].strftime(
                            "%d-%m-%Y")
                    if users[i]['books'][j].get('returned') is not None:
                        users[i]['books'][j]['returned'] = users[i]['books'][j]['returned'].strftime(
                            "%d-%m-%Y")
            else:
                users[i]['books'] = []
        authors = sorted([[a, [b['author'] for b in books].count(a)]
                          for a in [b['author'] for b in books]], key=lambda a: a[1])
        genres = sorted([[a, [b['genre'] for b in books].count(a)]
                        for a in [b['genre'] for b in books]], key=lambda a: a[1])

        mostreadablegenres = []
        for i in genres:
            if i[0] not in mostreadablegenres:
                mostreadablegenres.append(i[0])

        mostreadable = authors[0][0]

        return {'mostreadablegenres': mostreadablegenres[::-1], 'mostreadable': mostreadable}
