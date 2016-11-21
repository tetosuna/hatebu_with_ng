import urllib2
import sqlite3
import re
from lxml import etree
from flask import Flask, g, render_template, request, redirect, url_for

app = Flask(__name__)
hatebuurl = 'http://b.hatena.ne.jp/hotentry.rss'

@app.before_request
def before_request():
    g.db = sqlite3.connect('/data/ng.db')

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/title', methods=['POST'])
def edit_title():
    c = g.db.cursor()
    if request.form["_method"] == 'POST':
        sql = 'insert into ng_titles values("%s", "root")' % request.form["word"]
        c.execute(sql)
        g.db.commit()
        return redirect(url_for("hatebu"))

    if request.form["_method"] == 'DELETE':
        sql = 'delete from ng_titles where word="%s"' % request.form["word"]
        c.execute(sql)
        g.db.commit()
        return redirect(url_for("hatebu"))

@app.route('/domain', methods=['POST'])
def edit_domain():
    c = g.db.cursor()
    if request.form["_method"] == 'POST':
        sql = 'insert into ng_domains values("%s", "root")' % request.form["word"]
        c.execute(sql)
        g.db.commit()
        return redirect(url_for("hatebu"))

    if request.form["_method"] == 'DELETE':
        sql = 'delete from ng_domains where word="%s"' % request.form["word"]
        c.execute(sql)
        g.db.commit()
        return redirect(url_for("hatebu"))

@app.route('/')
def hatebu():
    c = g.db.cursor()
    sqldomain = 'select word from ng_domains'
    sqltitle = 'select word from ng_titles'
    c.execute(sqldomain)
    ngdomains = c.fetchall()
    c.execute(sqltitle)
    ngtitles = c.fetchall()
    return render_template('index.html', ngdomains=ngdomains, ngtitles=ngtitles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
