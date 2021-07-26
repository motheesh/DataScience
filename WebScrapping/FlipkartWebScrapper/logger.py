import logging as lg
import time
from flask import current_app as app

class logger:
    def log_error(error,errorType):
        filename=time.strftime("%m_%d_%Y")
        lg.basicConfig(filename=f'{app.config["LOG_PATH"]}{filename}.log',level=lg.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s")
        if errorType=="error":
            lg.error(error)
        elif errorType=="warning":
            lg.warning(error)
        elif errorType=="debug":
            lg.debug(error)
        elif errorType=="info":
            lg.info(error)