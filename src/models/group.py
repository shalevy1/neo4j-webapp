from database import get_db


class Group(object):

    @classmethod
    def serialize_group(cls, group):
        if group is None:
            return None
        else:
            return {
                'group_id': cls.form_group_id(group['groupLink']),
                'group_name': group['groupName'],
                'group_link': group['groupLink']
            }

    @classmethod
    def serialize_groups(cls, groups):
        groups_list = []
        for group in groups:
            groups_list.append(cls.serialize_group(group))
        return groups_list

    @classmethod
    def form_group_link(cls, group_id):
        return "https://www.facebook.com/groups/" + group_id

    @classmethod
    def form_group_id(cls, group_link):
        return group_link[32:]

    @classmethod
    def get_groups(cls):
        with get_db() as session:
            return cls.serialize_groups(session.run("MATCH (g:Group) RETURN g").value())

    @classmethod
    def get_group(cls, group_id):
        with get_db() as session:
            group_link = cls.form_group_link(group_id)
            return cls.serialize_group(session.run("MATCH (g:Group {groupLink: $group_link}) RETURN g",
                                                   group_link=group_link).single().value())

    @classmethod
    def get_group_members(cls, group_id):
        with get_db() as session:
            group_link = cls.form_group_link(group_id)
            from src.models.user import User
            return User.serialize_users(session.run("MATCH (u:User)-[:IS_MEMBER_OF]->(g:Group {groupLink: $group_link})"
                                                    "RETURN u", group_link=group_link).value())

    @classmethod
    def add_group(cls, group_id, group_name):
        with get_db() as session:
            group_link = cls.form_group_link(group_id)
            return cls.serialize_group(session.run("CREATE (g:Group {"
                                                   "groupName: $group_name, "
                                                   "groupLink: $group_link"
                                                   "}) RETURN g",
                                                   group_name=group_name,
                                                   group_link=group_link).single().value())

    @classmethod
    def update_group(cls, old_group_id, group_id, group_name):
        with get_db() as session:
            old_group_link = cls.form_group_link(old_group_id)
            group_link = cls.form_group_link(group_id)
            return cls.serialize_group(session.run("MATCH (g:Group {groupLink: $old_group_link}) SET g = {"
                                                   "groupLink: $group_link, "
                                                   "groupName: $group_name"
                                                   "} RETURN g",
                                                   old_group_link=old_group_link,
                                                   group_link=group_link,
                                                   group_name=group_name).single().value())

    @classmethod
    def delete_group(cls, group_id):
        with get_db() as session:
            group_link = cls.form_group_link(group_id)
            session.run("MATCH (g:Group {groupLink: $group_link}) DETACH DELETE g", group_link=group_link)
