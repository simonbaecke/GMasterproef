from rdflib import Graph,Namespace,Literal
from rdflib.namespace import RDF

g = Graph()
g.parse("alice.ttl")

dc = Namespace("http://purl.org/dc/elements/1.1/")
ex = Namespace("http://example.com/")

queryy = """
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?title
WHERE {
  ?book dc:title ?title .
}
"""

results = g.query(queryy)

for r in results:
    print(r)