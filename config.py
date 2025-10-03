import os 

config = {"host":os.environ.get("host","localhost"),"user":os.environ.get("user","root"),"database":os.environ.get("database","Anonymous_Chat_Bot"),"password":os.environ.get("password","Yy@?00112234")}
TOKEN = os.environ.get("TOKEN","8304136905:AAEYtWUjEwArss_5X-kg06VcRIW1ZmVrHtI")
channel_photos_cid = os.environ.get("channel_photos_cid","-1002669712767")
channel_translate_cid = os.environ.get("channel_translate_cid","-1002894220096")
channel_block_clinets_cid = os.environ.get("channel_block_clients_cid","-1003098780118")