from multiprocessing import cpu_count
import configs.logging

version = '0.0.11'
app_name = 'malproxy'
debug_mode = False
port = 8181

# GUnicorn configs
workers = cpu_count() * 2 + 1
bind = "0.0.0.0:" + str(port)
