

import requests
import re
from requests.exceptions import RequestException
import pymongo


MONGO_URL = 'localhost:27017'
MONGO_DB = 'ttjj'
MONGO_TABLE = 'option_list'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
}

def read(condition={}):
    return db[MONGO_TABLE].find_one(condition)

def read_more(condition={}):
    return db[MONGO_TABLE].find(condition)


def update_to_mongo(target, result):
    return db[MONGO_TABLE].update_one(target,{ "$set": result })

def save_to_mongo(result, id_name):
    if db[MONGO_TABLE].update({id_name: result[id_name]}, {'$set': result}, True):
        print('save cuccessful', result)
        return True
    return False

def get_response(url,params,headers=headers):
    try:
        response = requests.get(url,params=params,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('err: %s' % e)


def re_func(compile_str,text):
    pattern =  re.compile(compile_str,re.S)
    result =  re.match(pattern,text)
    return result