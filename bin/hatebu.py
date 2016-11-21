import urllib2
import sqlite3
import re
import os
from lxml import etree
from flask import Flask, g, Response

app = Flask(__name__)
#hatebuurl = 'http://feeds.feedburner.com/hatena/b/hotentry'
hatebuurl = 'http://b.hatena.ne.jp/hotentry.rss'

@app.before_request
def before_request():
    g.domain = os.environ.get("MYDOMAIN")
    g.db = sqlite3.connect('/data/ng.db')

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def filter_domain(con, xml):
    c = con.cursor()
    root=etree.fromstring(xml)
    namespace= {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'myrdf': 'http://purl.org/rss/1.0/'}

    sql = 'select word from ng_domains'
    for domain in c.execute(sql):
        for i in root.xpath('/rdf:RDF/myrdf:item/myrdf:link', namespaces=namespace):
            if re.search(domain[0], i.text):
                root.remove(i.getparent())
                for j in root.xpath('/rdf:RDF/myrdf:channel/myrdf:items/rdf:Seq/rdf:li[@rdf:resource="%s"]' % (i.text), namespaces=namespace):
                    j.getparent().remove(j)
    return etree.tostring(root, encoding="utf-8")

def filter_title(con, xml):
    c = con.cursor()
    root=etree.fromstring(xml)
    namespace= {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'myrdf': 'http://purl.org/rss/1.0/'}

    sql = 'select word from ng_titles'
    for title in c.execute(sql):
        for i in root.xpath('/rdf:RDF/myrdf:item/myrdf:title', namespaces=namespace):
            if re.search(title[0], i.text):
                link = i.xpath('../myrdf:link', namespaces=namespace)[0]
                root.remove(i.getparent())
                for j in root.xpath('/rdf:RDF/myrdf:channel/myrdf:items/rdf:Seq/rdf:li[@rdf:resource="%s"]' % (link.text), namespaces=namespace):
                    j.getparent().remove(j)
    return etree.tostring(root, encoding="utf-8")


def change_channel(domain, xml):
    root=etree.fromstring(xml)
    namespace= {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'myrdf': 'http://purl.org/rss/1.0/', 'atom10': 'http://www.w3.org/2005/Atom', 'feedburner': 'http://rssnamespace.org/feedburner/ext/1.0'}
    root.xpath('/rdf:RDF/myrdf:channel', namespaces=namespace)[0].set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', domain)
    root.xpath('/rdf:RDF/myrdf:channel/myrdf:link', namespaces=namespace)[0].text = domain
    root.xpath('/rdf:RDF/myrdf:channel/myrdf:title', namespaces=namespace)[0].text = 'hatena bookmark with ng'
    atomlink = root.xpath('/rdf:RDF/myrdf:channel/atom10:link', namespaces=namespace)
    for link in atomlink:
        link.getparent().remove(link)
    fblink = root.xpath('/rdf:RDF/myrdf:channel/feedburner:info', namespaces=namespace)
    for link in fblink:
        link.getparent().remove(link)

    return etree.tostring(root, encoding="utf-8")

@app.route('/')
def hatebu():
    fp = urllib2.urlopen(hatebuurl)
    xml = fp.read()
    fp.close
    xml = change_channel(g.domain, xml)
    xml = filter_domain(g.db, xml)
    xml = filter_title(g.db, xml)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml
    return Response(xml, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
