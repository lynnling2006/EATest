# load config.ini
import configparser
import app


config = configparser.ConfigParser()
config.read(app.BASE_DIR + "/config/config.ini")

config.api_base_url = config['api']['base_url'] 
config.festivals_path = config['festivals']['path']
config.threshold_throttle = config['threshold']['throttle']
config.threshold_elapsed = config['threshold']['elapsed']
config.festivals_url = config.api_base_url + config.festivals_path
