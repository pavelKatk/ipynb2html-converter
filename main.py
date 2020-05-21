# -*- coding: utf-8 -*-
 
import json
import telebot
from nbconvert import HTMLExporter
import nbformat
import requests
import os
import time
 
config = json.loads(open("config.json").read())
token = config["token"]

telebot.apihelper.proxy = {'https': 'socks5h://localhost:9050'}
 
bot = telebot.TeleBot(token)
 
def converter(input_file):
    f = open(input_file, 'r').read()
    jake_notebook = nbformat.reads(f, as_version=4)
    jake_notebook.cells[0]
    html_exporter = HTMLExporter()
    (body, resources) = html_exporter.from_notebook_node(jake_notebook)

    with open(input_file.split('.ipynb')[0] + '.html', 'w') as out:
        out.write(body)

    os.remove(input_file)
 
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello! Send me your jupyter notebook and I will try to convert his to html.')
 
@bot.message_handler(content_types=['document'])
def send_text(message):
    try:
        file_name = message.document.file_name
        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        src = file_name

        if not os.path.exists('tmp'): os.makedirs('tmp') 

        save_dir = r'tmp'
        full_name = save_dir + '/' + src
 
        with open(full_name, 'wb') as new_file:
            new_file.write(downloaded_file)
 
        converter(full_name)
        file_to_send = open(full_name.split('.ipynb')[0] + '.html', 'rb')
        bot.send_document(message.chat.id, data = file_to_send)
        file_to_send.close()
 
        os.remove(full_name.split('.ipynb')[0] + '.html')
 
    except Exception as ex:
        for i in os.listdir(save_dir):
            try:
                os.remove(save_dir + '/' + i)
            except:
                pass
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))
 
bot.infinity_polling()
