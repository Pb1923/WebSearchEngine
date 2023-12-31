#
# Libraries
#

import pymongo
from flask import Flask, request, render_template, flash
from flask_paginate import Pagination, get_page_args

# create app instance
app = Flask(__name__)


#
# Routes
#

@app.route('/')
def home():
    if 'search' in request.args:
        connect_uri = 'mongodb+srv://bhadoria1923:bhadoria1923@cluster0.b8ruxqv.mongodb.net/PB_Search_engine?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)

        # create db client
        db = client.PB_Search_engine

        search_results = db.search_results.find({'$text': {'$search': request.args.get('search')}})

        for entry in search_results:
            flash(entry, 'success')

        # close connection
        client.close()

    return render_template('search.html')


@app.route('/search_results')
def search_results():
    if 'search' in request.args:
        connect_uri = 'mongodb+srv://bhadoria1923:bhadoria1923@cluster0.b8ruxqv.mongodb.net/PB_Search_engine?retryWrites=true&w=majority'

        client = pymongo.MongoClient(connect_uri)

        # create db client
        db = client.PB_Search_engine

        query = db.search_results.find({'$text': {'$search': request.args.get('search')}})
        search_results = []

        for doc in query:
            search_results.append(doc)

        # close connection
        client.close()

        # automatic pagination handling
        total = len(search_results)
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('search_results.html',
                               search_results=search_results[offset: offset + per_page],
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               len=len)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, threaded=True)