from multiprocessing import cpu_count
import configs.logging
import configs.plexdictionary

users_db = 'configs/users.json'

version = '0.0.19'
app_name = 'malproxy'
debug_mode = False
port = 8181

# GUnicorn configs
workers = cpu_count() * 2 + 1
bind = "0.0.0.0:" + str(port)
