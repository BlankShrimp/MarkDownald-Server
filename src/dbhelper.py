import MySQLdb

conn = MySQLdb.connect(host='localhost', user='hdk', passwd='sbhdk', db='winmd')


def registry(userid, nickname, passwd):
    cursor = conn.cursor()
    cursor.execute("select userid from users where (userid='%s');" %(userid))
    row = cursor.fetchone()
    if row:
        cursor.close()
        return "EXISTED-USER"
    else:
        cursor.execute("insert into users values ('%s', '%s', '%s');" %(userid, nickname, passwd))
        cursor.close()
        conn.commit()
        return 0


def examine_user(userid, passwd):
    cursor = conn.cursor()
    cursor.execute("select userid, passwd from users where (userid='%s');" %(userid))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        return "MISSING-USER"
    else:
        if (passwd != row[1]):
            cursor.close()
            return "WRONG-PASSWD"
        else:
            cursor.close()
            return 0


def insert_note(userid, passwd, noteid, title, folderid, value):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        try:
            cursor.execute("insert into notes values (%s, '%s', %s, '%s', '%s', now());"
                       % (noteid, title, folderid, value, userid))
        except MySQLdb._exceptions.IntegrityError:
            return "EXISTED-NOTE"
        cursor.close()
        conn.commit()
        return 0


def delete_note(userid, passwd, noteid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("delete from notes WHERE userid = '%s' AND noteid = %s" % (userid, noteid))
        cursor.close()
        conn.commit()
        return 0


def select_single_note(userid, passwd, noteid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("select * from notes where userid = '%s' AND noteid = %s" % (userid, noteid))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return row
        else:
            return "MISSING-NOTE"


def update_note(userid, passwd, noteid, title, folderid, value):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        if select_single_note(userid, passwd, noteid) == "MISSING-NOTE":
            return "MISSING-NOTE"
        else:
            cursor = conn.cursor()
            cursor.execute("update notes set title = '%s', folderid = %s, value = '%s', cdate = now() "
                           "WHERE noteid = %s AND userid = '%s';"
                           % (title, folderid, value, noteid, userid))
            cursor.close()
            conn.commit()
            return 0


def insert_folder(userid, passwd, folderid, foldername, parentid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        try:
            cursor.execute("insert into notes folders (%s, '%s', '%s', %s);"
                       % (folderid, userid, foldername, parentid))
        except MySQLdb._exceptions.IntegrityError:
            return "EXISTED-FOLDER"
        cursor.close()
        conn.commit()
        return 0


def delete_folder(userid, passwd, folderid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("delete from folders WHERE userid = '%s' AND folderid = %s" % (userid, folderid))
        cursor.close()
        conn.commit()
        return 0


def select_single_folder(userid, passwd, folderid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("delete from folders WHERE userid = '%s' AND folderid = %s" % (userid, folderid))
        cursor.close()
        conn.commit()
        return 0


def update_folder(userid, passwd, folderid, foldername, parentid):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        if select_single_folder(userid, passwd, folderid) == "MISSING-FOLDER":
            return "MISSING-FOLDER"
        else:
            cursor = conn.cursor()
            cursor.execute("update folders set foldername = '%s', parentid = %s "
                           "WHERE folderid = %s AND userid = '%s';"
                           % (foldername, parentid, folderid, userid))
            cursor.close()
            conn.commit()
            return 0


def select_all_notes(userid, passwd):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("select * from notes where userid = '%s'" % (userid))
        results = cursor.fetchall()
        cursor.close()
        conn.commit()
        return results


def select_all_folders(userid, passwd):
    vali_result = examine_user(userid, passwd)
    if vali_result:
        return vali_result
    else:
        cursor = conn.cursor()
        cursor.execute("select * from folders where userid = '%s'" % (userid))
        results = cursor.fetchall()
        cursor.close()
        conn.commit()
        return results


registry("a", "c", "c")
