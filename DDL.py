import mysql.connector
from config import config

def create_database() :
    new_config = {key : value for key,value in config.items() if key != "database"}
    conn = mysql.connector.connect(**new_config)
    cur = conn.cursor()
    cur.execute("drop database if exists Anonymous_Chat_Bot;")
    cur.execute("create database if not exists Anonymous_Chat_Bot;")
    conn.commit()
    cur.close()
    conn.close()
    print("database created successfully.")

def create_table_user() :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("""
                create table user(
                        cid                             bigint primary key,
                        photo_mid_in_channel            bigint,
                        chat_with_cid                   bigint,
                        lat                             DECIMAL(10,8),
                        `long`                          DECIMAL(11,8),
                        name                            varchar(100) not null,
                        last_name                       varchar(100),
                        user_name                       varchar(100),
                        first_name                      varchar(100) not null,
                        age                             TINYINT unsigned not null,
                        city                            varchar(100) not null,
                        gender                          enum("male","female") not null,
                        block_or_active_by_admin        varchar(10) default "active",
                        join_at                         timestamp default current_timestamp,
                        last_update                     timestamp default current_timestamp on update current_timestamp
                )
                """)
    conn.commit()
    cur.close()
    conn.close()
    print("user table created successfully.")

def create_table_chat() :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("""
                create table chat(
                    chat_status             enum("active","block","deactive")  default 'active',
                    user1_cid               bigint not null,
                    user2_cid               bigint not null,
                    creat_at                timestamp default current_timestamp,
                    foreign key (user1_cid)  references user(cid),
                    foreign key (user2_cid) references user(cid),
                    primary key (user1_cid,user2_cid)
                )
                """)
    conn.commit()
    cur.close()
    conn.close()
    print("chat table created successfully.")
    

def create_table_message() :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("""
                create table message(
                    message_text                TEXT,
                    cid_sender                  bigint not null ,
                    cid_reciver                 bigint not null , 
                    mid_sender                  INT unsigned not null ,
                    message_type                enum("text","photo","audio","voice","video","document","sticker","animation","location","contact") not null default "text",
                    sent_at                     timestamp default current_timestamp,
                    foreign key (cid_sender)    references user(cid),
                    foreign key (cid_reciver)   references user(cid),
                    primary key (cid_sender,mid_sender)
                )
                """)
    conn.commit()
    cur.close()
    conn.close()
    print("table messgae created successfully . ")

if __name__ == "__main__" :
    create_database()
    create_table_user()
    create_table_chat()
    create_table_message()
#create_database()
#create_table_user()
#create_table_chat()
#create_table_message()