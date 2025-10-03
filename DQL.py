import mysql.connector
from config import config

def get_user_data(cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor(dictionary=True)
    cur.execute("select * from user where cid = %s",(cid,))
    data = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if data == None :
        return {}
    return data


def get_all_user_data() :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor(dictionary=True)
    cur.execute("select * from user")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def get_chat_data(user1_cid,user2_cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM chat WHERE (user1_cid=%s AND user2_cid=%s) OR (user1_cid=%s AND user2_cid=%s)",(user1_cid, user2_cid, user2_cid, user1_cid))       
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def get_message_data(cid_sender,mid_sender) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor(dictionary=True)
    cur.execute("select * from message where cid_sender = %s and mid_sender = %s",(cid_sender,mid_sender))
    data = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return data
