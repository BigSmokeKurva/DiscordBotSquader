#               Импорт не служебных модулей
import logging
import logging.config
import datetime as dt
#

class Logger:
    def __init__(self):
        today=dt.datetime.today().strftime("%Y.%m.%d-%H;%M")
        config={
            "version":1,
            "handlers":{
                "fileHandler":{
                    "class":"logging.FileHandler",
                    "formatter":"mainFormatter",
                    "filename":f"logs/{today}.log",
                    "encoding":"UTF-8"
                },
                "consoleHandler":{
                    "class":"logging.StreamHandler",
                    "formatter":"mainFormatter",
                    "stream":"ext://sys.stdout"
                }
            },
            "loggers":{
                "main":{
                    "handlers":["fileHandler","consoleHandler"],
                    "level":"DEBUG",
                }
            },
            "formatters":{
                "mainFormatter":{
                    "format":"%(asctime)s|%(moduleName)-11s|%(levelname)s >> %(message)s",
                    "datefmt":"%Y.%m.%d-%H:%M"
                }
            }
        }
        logging.config.dictConfig(config)   