from database import get_db


class Group(object):

    @classmethod
    def serialize_group(cls, group):
        if group is None:
            return None
        else:
            return {
                'group_name': group['groupName'],
                'group_link': group['groupLink']
            }

    @classmethod
    def serialize_groups(cls, groups):
        groups_list = []
        for group in groups:
            groups_list.append(cls.serialize_user(group))
        return groups_list
