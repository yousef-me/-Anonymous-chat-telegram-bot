import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from DML import *
from DQL import *
from translation import *
import logging
import requests
import random

bot = telebot.TeleBot(TOKEN)

logging.basicConfig(filename="project.log",level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

channel_translate_mids = {
    "first_start_and_get_name"    : 3,
    "get_age"                     : 4,
    "get_city"                    : 5,
    "invalid_message"             : 6,
    "male_profile_picture"        : 7,
    "female_profile_picture"      : 8,
    "get_gender"                  : 9,
    "end_of_getting_info"         :10,
    "loc_saved"                   :11,
    "change_user_photo"           :12,
    "main_page"                   :13,
    "profile_photo_changed"       :14,
    "get_search_status"           :15,
    "close_the_chat"              :16,
    "exit_from_chat"              :17,
    "please_wait"                 :18,
    "accept_or_reject"            :19,
    "start_chat"                  :20,
    "change_info"                 :21,
    "get_new_name"                :22,
    "saved"                       :23,
    "end_chat"                    :24,
    "block"                       :25,
    "try_again"                   :26
}

channel_photos_mids = {
    "male_profile_picture"      :       32,
    "female_profile_picture"    :       33
}

def listener(messages) :
    for message in messages : 
        if message.content_type == "text" :
            print(f"{message.chat.id} {message.chat.first_name} {message.text}")
        else :
            print(f"{message.chat.id} {message.chat.first_name} send a {message.content_type}")
bot.set_update_listener(listener)

def log_message(cid,message) :
    message_content = message.content_type
    if message_content == "text" :
        logging.info(f"{cid} SEND : {message.text}")
    else : 
        logging.info(f"{cid} SEND {message_content}")

def is_new_user(cid) :
    data = get_all_user_data()
    for user in data :
        if user["cid"] == cid :
            return False
    return True

def gen_age_keys() :
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(10,100) :
        markup.add(str(i))
    return markup
user_data = {} #{cid : {info}, ...}

def gen_location_key() :
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(translate["get_location"],request_location=True))
    return markup

def gen_gender_key() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["female"],callback_data="gender_is_female"),InlineKeyboardButton(translate["male"],callback_data="gender_is_male"))
    return markup

def gen_profile_caption(cid) :
    user_data = get_user_data(cid)
    name = user_data["name"]
    age = user_data["age"]
    city = user_data["city"]
    gender = user_data["gender"]
    caption = f'{translate["name"]} : {name}\n{translate["age"]} : {age}\n{translate["city"]} : {city}\n{translate["gender"]} : {translate[gender]}'
    return caption

def gen_profile_markup() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["change_info"],callback_data="change_info"),InlineKeyboardButton(translate["change_photo"],callback_data="change_photo"))
    return markup

def gen_main_keys() :
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(translate["search"])
    markup.add(translate["profile"])
    return markup


def send_profile(cid) :
    user = get_user_data(cid)
    bot.copy_message(cid,channel_photos_cid,user["photo_mid_in_channel"],caption=gen_profile_caption(cid),reply_markup=gen_profile_markup())

def gen_change_info_keys() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["gender"],callback_data="change_info_gender"),InlineKeyboardButton(translate["city"],callback_data="change_info_city"))
    markup.add(InlineKeyboardButton(translate["name"],callback_data="change_info_name"),InlineKeyboardButton(translate["age"],callback_data="change_info_age"))
    return markup

def gen_search_keys() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["male"],callback_data="search_for_male"),InlineKeyboardButton(translate["female"],callback_data="search_for_female"))
    markup.add(InlineKeyboardButton(translate["same_age"],callback_data="search_for_sameage"),InlineKeyboardButton(translate["near_location"],callback_data="search_for_nearlocation"))
    markup.add(InlineKeyboardButton(translate["random"],callback_data="search_for_random"))
    return markup

def del_main_user_from_data(cid,data) :
    for index in range(len(data)) :
        user = data[index]
        if user["cid"] == cid :
            data.pop(index)
            break
    return data

def gen_yes_or_no_keys() :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["yes"],callback_data="chat_accepted"),InlineKeyboardButton(translate["no"],callback_data="chat_rejected"))
    return markup

def in_chat(cid) :
    data = get_user_data(cid)
    if data.get("chat_with_cid") == None :
        return False
    return True

def get_second_user_cid(cid) :
    data = get_user_data(cid)
    return data["chat_with_cid"]

def gen_in_chat_main_keys() :
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(translate["end_chat"]))
    markup.add(KeyboardButton(translate["block"]))
    return markup

def get_male_user_data(data) :
    for user in data :
        if user["gender"] == "male" :
            return user
    return None

def get_female_user_data(data) :
    for user in data :
        if user["gender"] == "female" :
            return user
    return None

def get_same_age_user_data(first_user,data) :
    new_data = []
    for user in data :
        if first_user["age"] == user["age"] :
            return user
    return None

def get_dist(first_user,second_user) :
    long1 = first_user["long"]
    lat1 = first_user["lat"]
    long2 = first_user["long"]
    lat2 = first_user["lat"]
    res = requests.get(f"http://router.project-osrm.org/route/v1/driving/{long1},{lat1};{long2},{lat2}?overview=false")        
    data = res.json()
    dist = data["routes"][0]["distance"]
    return dist

def get_near_user_data(data,user_data) :
    dist_data = [] #[(user,dist) , ...]
    for user in data :
        second_user = user
        first_user = user_data
        dist = get_dist(first_user,second_user)
        dist_data.append((user,dist))
    min_dist = dist_data[0][1]
    for user, dist in dist_data :
        if dist < min_dist :
            min_dist = dist
        return user
    
def start_chat_handler(cid,second_user,user_data) :
    user = second_user
    second_user_cid = user["cid"]
    second_user_data = get_user_data(second_user_cid)
    change_user_in_chat(cid,second_user_cid)
    bot.copy_message(second_user_cid,channel_photos_cid,user_data["photo_mid_in_channel"],caption=gen_profile_caption(cid))
    bot.copy_message(cid,channel_photos_cid,second_user_data["photo_mid_in_channel"],caption=gen_profile_caption(second_user_cid))
    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["start_chat"],reply_markup=gen_in_chat_main_keys())
    bot.copy_message(second_user_cid,channel_translate_cid,channel_translate_mids["start_chat"],reply_markup=gen_in_chat_main_keys())                   

def del_in_chat_users_from_data(data) :
    new_data = []
    for user in data :
        if user["chat_with_cid"] == None :
            new_data.append(user)
    return new_data

def gen_admin_block_keys(cid) :
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(translate["admin_block"],callback_data=f"block_{cid}"))
    return markup

def block_or_no_by_user(first_user_cid,second_user_cid) :
    data = get_chat_data(first_user_cid,second_user_cid)
    if data == None :
        return False
    for chat in data :
        if chat["chat_status"] == "block" :
            return True
    return False

def block_or_no_by_admin(cid) :
    data = get_user_data(cid)
    if data["block_or_active_by_admin"] == "active" :
        return False
    return True

def del_block_users(data,first_user_cid) :
    new_data = []
    for user in data :
        second_user_cid = user["cid"]
        if not block_or_no_by_user(first_user_cid,second_user_cid) and not block_or_no_by_admin(second_user_cid) :
            new_data.append(user)
    return new_data

hide_board = ReplyKeyboardRemove()

@bot.message_handler(func = lambda message :  in_chat(message.chat.id))
def send_messages_to_second_user_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    mid = message.message_id
    second_user_cid = get_second_user_cid(cid)
    data = message.text
    add_to_message(cid,second_user_cid,mid,"text",message.text)
    if data == translate["end_chat"] :
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["end_chat"],reply_markup=gen_main_keys())
        bot.copy_message(second_user_cid,channel_translate_cid,channel_translate_mids["end_chat"],reply_markup=gen_main_keys()) 
        change_user_in_chat(cid,None)
        change_user_in_chat(second_user_cid,None)
        change_chat_status("deactive",cid,second_user_cid)
    elif data == translate["block"] :
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["block"],reply_markup=gen_main_keys())
        bot.copy_message(second_user_cid,channel_translate_cid,channel_translate_mids["end_chat"],reply_markup=gen_main_keys()) 
        change_user_in_chat(cid,None)
        change_user_in_chat(second_user_cid,None)
        change_chat_status("block",cid,second_user_cid)
        bot.send_message(channel_block_clinets_cid,str(second_user_cid),reply_markup=gen_admin_block_keys(second_user_cid))
    else :
        bot.copy_message(second_user_cid,cid,mid)

@bot.message_handler(commands=["start"])
def start_command_hanlder(message):
    cid = message.chat.id
    if is_new_user(cid) :
        user_data.setdefault(cid,{})
        user_data[cid]["first_name"] = message.chat.first_name
        if message.chat.last_name != None :
            user_data[cid]["last_name"] = message.chat.last_name
        logging.info(f"{cid} started the bot .")
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["first_start_and_get_name"])
    else :
        if block_or_no_by_admin(cid) :
            return
        send_profile(cid)

@bot.message_handler(func = lambda message : user_data.get(message.chat.id) != None and user_data.get(message.chat.id, {}).get("name") == None)
def get_name_handler(message) :
    cid = message.chat.id
    user_data[cid]["name"] = message.text
    markup = gen_age_keys()
    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_age"],reply_markup=markup)

@bot.message_handler(func = lambda message : user_data.get(message.chat.id) != None and user_data.get(message.chat.id, {}).get("age") == None)
def get_age_handler(message) :
    cid = message.chat.id
    age = message.text
    try :
        age = int(age)
    except :
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["invalid_message"])
    else :
        if 10 <= age <= 100 :
            user_data[cid]["age"] = message.text
            markup = gen_location_key()
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_city"],reply_markup=markup)
        else :
            default_handler(message)

@bot.message_handler(content_types=["location"])
def get_city_handler(message) :
    cid = message.chat.id
    if not in_chat(message.chat.id) :
        if user_data.get(message.chat.id) != None and user_data.get(message.chat.id, {}).get("city") == None :
            lat = message.location.latitude
            long = message.location.longitude
            params = {
                "longitude" : long,
                "latitude"  : lat
            }
            res = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client",params=params)
            data = res.json()
            city = data["city"]
            user_data[cid]["city"] = city
            user_data[cid]["lat"] = lat
            user_data[cid]["long"] = long
            markup = gen_gender_key()
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["loc_saved"],reply_markup=hide_board)
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_gender"],reply_markup=markup)
        elif change_info_dict.get(cid) == "change_city" :
            if block_or_no_by_admin(cid) :
                return    
            new_location_handler(message)
        else :
            if block_or_no_by_admin(cid) :
                return
            default_handler(message)
    else :
        if block_or_no_by_admin(cid) :
            return  
        default_handler(message)

@bot.callback_query_handler(func = lambda call : call.data.startswith("gender"))
def get_gender_handler(call) :
    cid = call.message.chat.id
    call_id = call.id
    if is_new_user(cid) :
        gender = call.data.split("_")[-1]
        call_id = call.id
        user_data[cid]["gender"] = gender
        user_data[cid]["photo_mid"] = channel_photos_mids["male_profile_picture"] if user_data[cid]["gender"] == "male" else channel_photos_mids["female_profile_picture"]
        user = user_data[cid]
        add_to_user(cid,user["name"],user["first_name"],user["lat"],user["long"],user["age"],user["city"],user["gender"],last_name=user.get("last_name"),user_name=call.from_user.username,photo_mid_in_channel=user["photo_mid"])
        bot.answer_callback_query(call_id,translate["end_of_getting_info_callback_answer"])
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["end_of_getting_info"],reply_markup=gen_main_keys())
        send_profile(cid)
        user_data.pop(cid)
    elif change_info_dict.get(cid) == "change_gender" :
        if block_or_no_by_admin(cid) :
            return  
        change_info_dict.pop(cid)
        gender = call.data.split("_")[-1]
        change_user_gender(gender,cid)
        change_user_photo(channel_photos_mids["male_profile_picture"] if gender == "male" else channel_photos_mids["female_profile_picture"],cid)
        bot.answer_callback_query(call_id,translate["gender_changed"])
        send_profile(cid)
    else :
        if block_or_no_by_admin(cid) :
            return  
        bot.answer_callback_query(call_id,translate["invalid_message"])
        
getting_profile_photo_step = {} #{cid : step , ...}
@bot.callback_query_handler(func = lambda call : call.data == "change_photo")
def change_info_handler(call) :
    cid = call.message.chat.id
    if block_or_no_by_admin(cid) :
        return
    call_id = call.id
    mid = call.message.message_id
    if not in_chat(cid) :
        getting_profile_photo_step[cid] = True
        bot.answer_callback_query(call_id,translate["req_picture_call_ans"])
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["change_user_photo"])
    else :
        bot.answer_callback_query(call_id,translate["invalid_message"])

@bot.message_handler(content_types=["photo"])
def change_profile_photo_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    if not in_chat(cid) :
        if getting_profile_photo_step.get(cid) :
            photo = bot.copy_message(channel_photos_cid,cid,message.message_id)
            change_user_photo(photo.message_id,cid)
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["profile_photo_changed"])
            send_profile(cid)
            getting_profile_photo_step.pop(cid)
        else :
            default_handler(message)
    else :
        default_handler(message)

@bot.callback_query_handler(func = lambda call : call.data == "change_info")
def change_info_handler(call) :
    cid = call.message.chat.id
    if block_or_no_by_admin(cid) :
        return
    call_id = call.id
    mid = call.message.message_id
    if not in_chat(cid) :
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["change_info"],reply_markup=gen_change_info_keys())
        bot.answer_callback_query(call_id,translate["change_info_call_answer"])
    else :
        bot.answer_callback_query(call_id,translate["invalid_message"])

change_info_dict = {}   #{cid : change_name,change_gender,change_age,change_city , ...}
@bot.callback_query_handler(func = lambda call : call.data.startswith("change_info"))
def get_new_info_handler(call) :
    call_id = call.id
    mid = call.message.message_id
    cid = call.message.chat.id
    if block_or_no_by_admin(cid) :
        return
    data = call.data
    data = data.split("_")[-1]
    change_info_dict[cid] = "change_" + data
    if not in_chat(cid) :
        if data == "name" :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_new_name"])
            bot.answer_callback_query(call_id,translate["change_name_call_answer"])  
        elif data == "age" :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_age"],reply_markup=gen_age_keys())
            bot.answer_callback_query(call_id,translate["change_age_call_answer"])
        elif data == "gender" :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_gender"],reply_markup=gen_gender_key())
            bot.answer_callback_query(call_id,translate["change_gender_call_answer"])
        elif data == "city" :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_city"],reply_markup=gen_location_key())
            bot.answer_callback_query(call_id,translate["change_location_call_answer"])
    else :
        bot.answer_callback_query(call_id,translate["invalid_message"])

@bot.message_handler(content_types=["location"])
def new_location_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    if change_info_dict.get(cid) == "change_city" :
        change_info_dict.pop(cid)
        lat = message.location.latitude
        long = message.location.longitude
        params = {
            "longitude" : long,
            "latitude"  : lat
        }
        res = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client",params=params)
        data = res.json()
        city = data["city"]
        change_user_city(city,cid)
        change_user_lat_long(lat,long,cid)
        bot.copy_message(cid,channel_translate_cid,channel_translate_mids["loc_saved"],reply_markup=gen_main_keys())
    else :
        default_handler(message)

@bot.message_handler(func = lambda message : change_info_dict.get(message.chat.id) == "change_name" or change_info_dict.get(message.chat.id) == "change_age")
def change_name_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    if change_info_dict.get(message.chat.id) == "change_name" :
        change_user_name(message.text,cid)
        send_profile(cid)
        change_info_dict.pop(cid)
    else :
        age = message.text
        try :
            age = int(age)
        except :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["invalid_message"])
        else :
            if 10 <= age <= 100 :
                bot.copy_message(cid,channel_translate_cid,channel_translate_mids["saved"],reply_markup=gen_main_keys())
                change_user_age(int(message.text),cid)
                change_info_dict.pop(cid)
                send_profile(cid)
            else :
                default_handler(message)

@bot.message_handler(func = lambda message : message.text == translate["profile"])
def get_profile_main_key_hanlder(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    send_profile(cid)

@bot.message_handler(func = lambda message : message.text == translate["search"])
def search_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["get_search_status"],reply_markup=gen_search_keys())

@bot.callback_query_handler(func = lambda call : call.data.startswith("search"))
def search_callback_handler(call):
    cid = call.message.chat.id
    if block_or_no_by_admin(cid) :
        return
    call_id = call.id
    mid = call.message.message_id
    chat_status = call.data.split("_")[-1]
    main_user_data = get_user_data(cid)
    all_users_data = get_all_user_data()
    all_users_data = del_main_user_from_data(cid,all_users_data)
    all_users_data = del_in_chat_users_from_data(all_users_data)
    all_users_data = del_block_users(all_users_data,cid)
 

    if main_user_data.get("chat_with_cid") == None :
        if all_users_data == [] :
            bot.answer_callback_query(call_id,translate["try_again"])
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["try_again"],reply_markup=gen_main_keys())
        else :
            bot.copy_message(cid,channel_translate_cid,channel_translate_mids["please_wait"])
            bot.answer_callback_query(call_id,translate["wait_please"])
            if chat_status == "random" : 
                while True :
                    number = random.randint(0,len(all_users_data)-1)
                    second_user_data = all_users_data[number]
                    if second_user_data.get("chat_with_cid") == None :
                        start_chat_handler(cid,second_user_data,main_user_data)
                        add_to_chat(cid,second_user_data["cid"])
                        break
            elif chat_status == "male" :
                second_user_data = get_male_user_data(all_users_data)
                if second_user_data == None :
                    bot.answer_callback_query(call_id,translate["try_again"])
                    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["try_again"],reply_markup=gen_main_keys())
                else :
                    start_chat_handler(cid,second_user_data,main_user_data)
                    add_to_chat(cid,second_user_data["cid"])
                                    
            elif chat_status == "female" :
                second_user_data = get_female_user_data(all_users_data)
                if second_user_data == None :
                    bot.answer_callback_query(call_id,translate["try_again"])
                    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["try_again"],reply_markup=gen_main_keys())
                else :
                    start_chat_handler(cid,second_user_data,main_user_data)
                    add_to_chat(cid,second_user_data["cid"])
                            
            elif chat_status == "nearlocation" :
                second_user_data = get_near_user_data(all_users_data,main_user_data)
                start_chat_handler(cid,second_user_data,main_user_data)
                add_to_chat(cid,second_user_data["cid"])
                        
            else :
                second_user_data = get_same_age_user_data(main_user_data,all_users_data)
                if second_user_data == None :
                    bot.answer_callback_query(call_id,translate["try_again"])
                    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["try_again"],reply_markup=gen_main_keys())
                else :        
                    start_chat_handler(cid,second_user_data,main_user_data)
                    add_to_chat(cid,second_user_data["cid"])
    else :
        bot.answer_callback_query(call_id,translate["you_are_on_a_chat"])

@bot.callback_query_handler(func= lambda call : call.data.startswith("block"))
def admin_block_handler(call) :
    cid = call.message.chat.id
    data = call.data
    second_user_cid = int(data.split("_")[-1])
    call_id = call.id
    change_admin_block("block",second_user_cid)
    bot.answer_callback_query(call_id,translate["kick_user"])

@bot.message_handler(func = lambda message : True)
def default_handler(message) :
    cid = message.chat.id
    if block_or_no_by_admin(cid) :
        return
    bot.copy_message(cid,channel_translate_cid,channel_translate_mids["invalid_message"])

bot.infinity_polling()