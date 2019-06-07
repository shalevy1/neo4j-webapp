from database import get_db


class User(object):

    @classmethod
    def serialize_user(cls, user):
        if user is None:
            return None
        return {
            'user_id': user['userFBlink'],
            'username': user['userName'],
            'user_basic_info': user['userBasicInfo'],
            'user_contact_info': user['userContactInfo'],
            'user_relationship_info': user['userRelationshipInfo']
        }

    @classmethod
    def serialize_users(cls, users):
        users_list = []
        for user in users:
            users_list.append(cls.serialize_user(user))
        return users_list

    @classmethod
    def get_users(cls):
        with get_db() as session:
            users = session.run("MATCH (n:User) RETURN n")
            if users is None:
                return None
            else:
                return cls.serialize_users(users.value())

    @classmethod
    def get_user(cls, user_id):
        with get_db() as session:
            if user_id.isdigit():
                user_id = "profile.php?id=" + user_id
            user_id = "https://www.facebook.com/" + user_id
            user = session.run("MATCH (n:User {userFBlink: $user_id}) RETURN n", user_id=user_id).single()
            if user is None:
                return None
            else:
                return cls.serialize_user(user.value())

    @classmethod
    def add_user(cls, user_id, username, user_basic_info, user_contact_info, user_relationship_info):
        with get_db() as session:
            if user_id.isdigit():
                user_id = "profile.php?id=" + user_id
            user_id = "https://www.facebook.com/" + user_id
            return cls.serialize_user(
                session.run("CREATE (n:User { "
                            "userFBlink: $user_id, "
                            "userName: $username, "
                            "userBasicInfo: $user_basic_info, "
                            "userContactInfo: $user_contact_info, "
                            "userRelationship: $user_relationship_info"
                            "}) RETURN n",
                            user_id=user_id,
                            username=username,
                            user_basic_info=user_basic_info,
                            user_contact_info=user_contact_info,
                            user_relationship_info=user_relationship_info).single().value())

    @classmethod
    def update_user(cls, user_id, username, user_basic_info, user_contact_info, user_relationship_info):
        with get_db() as session:
            if user_id.isdigit():
                user_id = "profile.php?id=" + user_id
            user_id = "https://www.facebook.com/" + user_id
            return cls.serialize_user(
                session.run("MATCH (n:User {userFBlink: “https://www.facebook.com/”+$user_id})"
                            "SET n = {"
                            "userFBlink: $user_id,"
                            "userName: $username,"
                            "userBasicInfo: $user_basic_info,"
                            "userContactInfo: $user_contact_info,"
                            "userRelationship: $user_relationship_info"
                            "} RETURN n",
                            user_id=user_id,
                            username=username,
                            user_basic_info=user_basic_info,
                            user_contact_info=user_contact_info,
                            user_relationship_info=user_relationship_info).single().value())

    @classmethod
    def delete_user(cls, user_id):
        with get_db() as session:
            if user_id.isdigit():
                user_id = "profile.php?id=" + user_id
            user_id = "https://www.facebook.com/" + user_id
            session.run("MATCH (n:User {userFBlink: $user_id}) DETACH DELETE n", user_id=user_id)

