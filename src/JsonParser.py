import json


def dump_single_note(input):
    obj = [{
        'noteid' : int(input[0]),
        'title' : input[1],
        'folderid' : int(input[2]),
        'value' : input[3],
        'userid' : input[4],
        'cdate' : input[5]
    }]
    return json.dumps(obj)


def dump_all_notes(input):
    obj = []
    for row in input:
        temp = [{
            'noteid' : int(row[0]),
            'title' : row[1],
            'folderid' : int(row[2]),
            'value' : row[3],
            'userid' : row[4],
            'cdate' : row[5]
        }]
        obj.append(temp)
    return json.dumps(obj)


def dump_all_folder(input):
    obj = []
    for row in input:
        temp = [{
            'folder' : int(row[0]),
            'userid' : row[1],
            'foldername' : row[3],
            'parentid' : int(row[2]),
        }]
        obj.append(temp)
    return json.dumps(obj)
