from neo4j import GraphDatabase
from json import dumps

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "1223334444"))


def get_users(tx):
    return tx.run("MATCH (n:User) RETURN n LIMIT 25").value()


def serialize_user(user):
    return {
        'user_id': user['userFBlink'],
        'username': user['userName'],
        'user_basic_info': user['userBasicInfo'],
        'user_contact_info': user['userContactInfo'],
        'user_relationship_info': user['userRelationshipInfo']
    }


def serialize_users(users):
    users_list = []
    for user in users:
        users_list.append(serialize_user(user))
    return users_list


if __name__ == '__main__':
    with driver.session() as session:
        users = session.read_transaction(get_users)
        print(dumps(serialize_users(users)))
        driver.close()
