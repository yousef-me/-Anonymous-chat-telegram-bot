import mysql.connector
from config import config

def add_to_user(cid,name,first_name,lat,long,age,city,gender,chat_with_cid=None,last_name=None,user_name=None,photo_mid_in_channel=None,invit_link = None,block_or_active_by_admin="active") :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("insert into user(cid,name,first_name,photo_mid_in_channel,chat_with_cid,last_name,user_name,age,city,gender,lat,`long`,block_or_active_by_admin) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cid,name,first_name,photo_mid_in_channel,chat_with_cid,last_name,user_name,age,city,gender,lat,long,block_or_active_by_admin))
    conn.commit()
    cur.close()
    conn.close()

def change_admin_block(status,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    print("start")
    cur.execute("update user set block_or_active_by_admin= %s where cid = %s",(status,cid))
    print("end")
    conn.commit()
    cur.close()
    conn.close()

def change_user_photo(new_mid,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set photo_mid_in_channel = %s where cid = %s",(new_mid,cid))
    conn.commit()
    cur.close()
    conn.close()

def change_user_in_chat(cid,second_user_cid=None):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set chat_with_cid  = %s where cid = %s",(second_user_cid,cid))
    cur.execute("update user set chat_with_cid  = %s where cid = %s",(cid,second_user_cid))
    conn.commit()
    cur.close()
    conn.close()

def change_user_name(new_name,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set name = %s where cid = %s",(new_name,cid))
    conn.commit()
    cur.close()
    conn.close()

def change_user_age(new_age,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set age = %s where cid = %s",(new_age,cid))
    conn.commit()
    cur.close()
    conn.close()

def change_user_city(new_city,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set city = %s where cid = %s",(new_city,cid))
    conn.commit()
    cur.close()
    conn.close()


def change_user_gender(new_gender,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set gender = %s where cid = %s",(new_gender,cid))
    conn.commit()
    cur.close()
    conn.close()

def change_user_lat_long(new_lat,new_long,cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update user set lat = %s where cid = %s",(new_lat,cid))
    cur.execute("update user set `long` = %s where cid = %s",(new_long,cid))
    

def add_to_chat(user1_cid,user2_cid,chat_status = "active") :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    try :
        cur.execute("insert into chat(user1_cid,user2_cid,chat_status) values(%s,%s,%s)",(user1_cid,user2_cid,chat_status))
    except :
        cur.execute("delete from chat where user1_cid = %s and user2_cid = %s",(user1_cid,user2_cid))
        cur.execute("insert into chat(user1_cid,user2_cid,chat_status) values(%s,%s,%s)",(user1_cid,user2_cid,chat_status))
    
    conn.commit()
    cur.close()
    conn.close()
    
def change_chat_status(new_chat_status,user1_cid,user2_cid) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    try :
        cur.execute("update chat set chat_status = %s where user1_cid = %s and user2_cid = %s",(new_chat_status,user1_cid,user2_cid))
    except :
        cur.execute("update chat set chat_status = %s where  user1_cid = %s and user2_cid = %s",(new_chat_status,user2_cid,user1_cid))
    
    conn.commit()
    cur.close()
    conn.close()    

def add_to_message(cid_sender,cid_reciver,mid_sender,message_type="text",message_text = None) :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("insert into message(cid_sender,cid_reciver,mid_sender,message_type,message_text) values(%s,%s,%s,%s,%s)",(cid_sender,cid_reciver,mid_sender,message_type,message_text))
    conn.commit()
    cur.close()
    conn.close()
