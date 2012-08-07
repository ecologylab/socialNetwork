import datetime


def GetDateTime(time):
    format = "%a %b %d %H:%M:%S %Y"
    time_format = time.strftime(format)
    return time_format

def GetDict(queryobj):
    tags_list = []
    for tag in queryobj.tags.all():
        tags_list.append(tag.tag)
    info_dict = dict(get_composition_metadata_response = dict(metadata = dict(username = queryobj.user.username,title = queryobj.name,description = queryobj.description, created = GetDateTime(queryobj.added),tags = dict(tag = tags_list))))
    return info_dict
