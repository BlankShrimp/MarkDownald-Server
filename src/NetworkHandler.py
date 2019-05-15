from socket import *
import json
import JsonParser
import DBHelper

conn = socket(AF_INET, SOCK_STREAM)
conn.bind(('',4687))
conn.listen(40)

while True:
    new_conn, addr = conn.accept()
    msg = new_conn.recv(1024).decode()

    obj = json.loads(msg)
    if obj['instruction'] == 'reg':
        result = DBHelper.registry(obj['userid'], obj['passwd'], obj['nickname'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'add_note':
        result = DBHelper.insert_note(obj['userid'], obj['passwd'], obj['noteid'], obj['title'], obj['folderid'], obj['value'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'del_note':
        result = DBHelper.delete_note(obj['userid'], obj['passwd'], obj['noteid'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'sel_note':
        result = DBHelper.select_single_note(obj['userid'], obj['passwd'], obj['noteid'])
        if isinstance(result, str):
            new_conn.send(result.encode())
        else:
            new_conn.send(JsonParser.dump_single_note(result).encode())
    elif obj['instruction'] == 'up_note':
        result = DBHelper.update_note(obj['userid'], obj['passwd'], obj['noteid'], obj['title'], obj['folderid'], obj['value'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'add_folder':
        result = DBHelper.insert_folder(obj['userid'], obj['passwd'], obj['folderid'], obj['foldername'], obj['parentid'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'del_folder':
        result = DBHelper.delete_folder(obj['userid'], obj['passwd'], obj['folderid'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'up_folder':
        result = DBHelper.update_folder(obj['userid'], obj['passwd'], obj['folderid'], obj['foldername'], obj['parentid'])
        new_conn.send(result.encode())
    elif obj['instruction'] == 'sel_notes':
        result = DBHelper.select_all_notes(obj['userid'], obj['passwd'])
        if isinstance(result, str):
            new_conn.send(result.encode())
        else:
            new_conn.send(JsonParser.dump_all_notes(result).encode())
    elif obj['instruction'] == 'sel_folders':
        result = DBHelper.select_all_folders(obj['userid'], obj['passwd'])
        if isinstance(result, str):
            new_conn.send(result.encode())
        else:
            new_conn.send(JsonParser.dump_all_folder(result).encode())
    new_conn.close()
