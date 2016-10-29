﻿import os

version = "0.0.1"
debug = False

## PATHS & FILENAMES ##

dir_data = "data"
dir_cache = "cache"
dir_log = "logs"
log_error = os.path.join(dir_log, "error.log")
log_normal = os.path.join(dir_log, "activity.log")
log_debug = os.path.join(dir_log, "debug.log")
db_path = os.path.join(dir_data, "happypanda.db")

## DATABASE

db_version = [0]
db_session = None

## SERVER

local_port = 5577
web_port = local_port + 1
same_network = True
host = '0.0.0.0' if same_network else "localhost"
client_limit = None
postfix = b'end'
data_size = 1024
public_server = False