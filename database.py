from flask import g
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "1223334444"

driver = GraphDatabase.driver(uri, auth=(user, password))


def get_db():
    '''
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db
    '''
    return driver.session()
