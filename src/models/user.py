from database import get_db
from src.models.group import Group
from src.models.work import Work


class User(object):

    @classmethod
    def serialize_user(cls, user):
        if user is None:
            return None
        return {
            'user_id': cls.form_user_id(user['userFBlink']),
            'user_fb_link': user['userFBlink'],
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
    def form_user_fb_link(cls, user_id):
        if user_id.isdigit():
            user_fb_link = "https://www.facebook.com/profile.php?id=" + user_id
        else:
            user_fb_link = "https://www.facebook.com/" + user_id
        return user_fb_link

    @classmethod
    def form_user_id(cls, user_fb_link):
        if "profile.php?id=" in user_fb_link:
            user_id = user_fb_link[40:]
        else:
            user_id = user_fb_link[25:]
        return user_id

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
            user_fb_link = cls.form_user_fb_link(user_id)
            user = session.run("MATCH (n:User {userFBlink: $user_fb_link}) RETURN n", user_fb_link=user_fb_link).single()
            if user is None:
                return None
            else:
                return cls.serialize_user(user.value())

    @classmethod
    def add_user(cls, user_id, username, user_basic_info, user_contact_info, user_relationship_info):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            return cls.serialize_user(
                session.run("CREATE (n:User { "
                            "userFBlink: $user_fb_link, "
                            "userName: $username, "
                            "userBasicInfo: $user_basic_info, "
                            "userContactInfo: $user_contact_info, "
                            "userRelationshipInfo: $user_relationship_info"
                            "}) RETURN n",
                            user_fb_link=user_fb_link,
                            username=username,
                            user_basic_info=user_basic_info,
                            user_contact_info=user_contact_info,
                            user_relationship_info=user_relationship_info).single().value())

    @classmethod
    def update_user(cls, old_user_id, user_id, username, user_basic_info, user_contact_info, user_relationship_info):
        with get_db() as session:
            old_user_fb_link = cls.form_user_fb_link(old_user_id)
            user_fb_link = cls.form_user_fb_link(user_id)
            return cls.serialize_user(
                session.run("MATCH (n:User {userFBlink: $old_user_fb_link})"
                            "SET n = {"
                            "userFBlink: $user_fb_link,"
                            "userName: $username,"
                            "userBasicInfo: $user_basic_info,"
                            "userContactInfo: $user_contact_info,"
                            "userRelationshipInfo: $user_relationship_info"
                            "} RETURN n",
                            old_user_fb_link=old_user_fb_link,
                            user_fb_link=user_fb_link,
                            username=username,
                            user_basic_info=user_basic_info,
                            user_contact_info=user_contact_info,
                            user_relationship_info=user_relationship_info).single().value())

    @classmethod
    def delete_user(cls, user_id):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            session.run("MATCH (n:User {userFBlink: $user_fb_link}) DETACH DELETE n", user_fb_link=user_fb_link)

    @classmethod
    def get_user_works(cls, user_id):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            return Work.serialize_works(session.run("MATCH (n:User {userFBlink: $user_fb_link})-->(w:WorkPlace) RETURN w", user_fb_link=user_fb_link).value())

    @classmethod
    def add_user_work(cls, user_id, work_place_name, work_place_link):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            return Work.serialize_work(session.run("MATCH (n:User {userFBlink: $user_fb_link})"
                                                   "CREATE (n)-[:WORK_AT]->(w:WorkPlace {"
                                                   "workPlaceName: $work_place_name, "
                                                   "workPlaceLink: $work_place_link})",
                                                   user_fb_link=user_fb_link,
                                                   work_place_name=work_place_name,
                                                   work_place_link=work_place_link).single().value())

    @classmethod
    def delete_user_work(cls, user_id, work_place_link):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            session.run("MATCH (n:User {userFBlink: $user_fb_link})-[:WORK_AT]->"
                        "(w:WorkPlace {workPlaceLink: $work_place_link}) "
                        "DETACH DELETE w",
                        user_fb_link=user_fb_link,
                        work_place_link=work_place_link)

    @classmethod
    def get_user_groups(cls, user_id):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            return Group.serialize_groups(
                session.run("MATCH (n:User {userFBlink: $user_fb_link})-[:IS_MEMBER_OF]->(g:Group) RETURN g",
                            user_fb_link=user_fb_link).value())

    @classmethod
    def join_group(cls, user_id, group_link):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            session.run("MATCH (n:User {userFBlink: $user_fb_link}), "
                        "(g:Group {groupLink: $group_link}) "
                        "CREATE (n)-[:IS_MEMBER_OF]->(g)",
                        user_fb_link=user_fb_link,
                        group_link=group_link)

    @classmethod
    def leave_group(cls, user_id, group_link):
        with get_db() as session:
            user_fb_link = cls.form_user_fb_link(user_id)
            session.run("MATCH (n:User {userFBlink: $user_fb_link})"
                        "-[r:IS_MEMBER_OF]->"
                        "(g:Group {groupLink: $group_link})"
                        "DELETE r",
                        user_fb_link=user_fb_link,
                        group_link=group_link)

