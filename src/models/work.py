class Work(object):

    @classmethod
    def serialize_work(cls, work):
        if work is None:
            return None
        else:
            return {
                'work_place_name': work['workPlaceName'],
                'work_place_link': work['workPlaceLink']
            }

    @classmethod
    def serialize_works(cls, works):
        works_list = []
        for work in works:
            works_list.append(cls.serialize_user(work))
        return works_list
