""" Модуль для работы с 1C """
import os, json
from time import time
import requests
from source.data import config
from loguru import logger

onec_user = config.onec_user
onec_pass = config.onec_pass
hostname = config.onec_host

#получаем информацию о пользователе из 1С по токен
def Login(number, chat_id):
    time_start = time()
    session = requests.Session()
    session.auth = (onec_user, onec_pass)
    payload = {
        "chat_id" : str(chat_id) ,
        "contact_phone_number" : str(number)
    }
    response = session.post(f"https://{hostname}/Login", data=json.dumps(payload))
    #print (response.text) #debug
    time_stop = time()
    #my_log = ["user_login", response.status_code, time_stop - time_start] #log
    logger.info(f"[ ] {response.status_code}, {time_stop - time_start}")
    #return response.text, my_log
    #return response.status_code, 
    return response 

#получаем список заказ-нарядов
def LastOrders(chat_id):
    time_start = time()
    session = requests.Session()
    session.auth = (onec_user, onec_pass)
    payload = {
        "chat_id" : str(chat_id)
    }
    response = session.get(f"https://{hostname}/LastOrders", data=json.dumps(payload))
    time_stop = time()
    #my_log = ["LastOrders", response.status_code, time_stop - time_start] #log
    logger.info(f"[ ] {response.status_code}, {time_stop - time_start}")
    #return response.text, my_log
    return response.status_code, response.text

# Валидация номера заказ-наряда
def Order(chat_id, doc_number):
    """ Валидация номера заказ-наряда """
    time_start = time()
    session = requests.Session()
    session.auth = (onec_user, onec_pass)
    payload = {
        "chat_id" : str(chat_id),
        "docnumber" : str(doc_number),

    }
    response = session.get(f"https://{hostname}/Order", data=json.dumps(payload))
    time_stop = time()
    #my_log = ["Order", response.status_code, time_stop - time_start] #log
    logger.info(f"[ ] {response.status_code}, {time_stop - time_start}")
    #return response.text, my_log
    #print (response.text)
    return response.status_code, response.text

# Регистрация контента
def Content(chat_id, text, file_info): 
    """ Регистрация контента в заказ-наряд """
    time_start = time()
    session = requests.Session()
    session.auth = (onec_user, onec_pass)
    payload = {
        "chat_id" : str(chat_id),
        "order_guid" : file_info[0],
        "file_path" : file_info[3],
        "file_type" : file_info[2],
        "file_ext" : file_info[1],
        "file_descr" : str(text),

    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = session.put(f"https://{hostname}/Content", data=json.dumps(payload))
    time_stop = time()
    #my_log = ["Order", response.status_code, time_stop - time_start] #log
    logger.info(f"[ ] Статус: {response.status_code} | {response.reason}, {time_stop - time_start}")
    #return response.text, my_log
    #print (response.reason) # debug
    return response.status_code, response, json.dumps(payload, ensure_ascii=False)