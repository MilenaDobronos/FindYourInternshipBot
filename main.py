#!/usr/bin/env python3
# -*- coding: utf-8 -*-

API_TOKEN = '5438532763:AAERw6gERRol9iAfWbF7FLOFz9-rZK-Pab0'

import telebot
from telebot import types
import pandas as pd

from get_int import get_internships


bot = telebot.TeleBot(API_TOKEN)

field = ''
degree = ''
region = ''
country = ''


@bot.message_handler(commands=["start"])
def start(message):
    if message.text.strip()=='Stop':
        return None
    bot.send_message(message.chat.id, 'Hi!\nThis bot is designed to help you find opportunities abroad')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1=types.KeyboardButton("Biomedical")
    item2=types.KeyboardButton("Computer Science")
    item3=types.KeyboardButton("Chemistry")
    item4=types.KeyboardButton("Schools etc")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, 'Choose field:',  reply_markup=markup)
    bot.register_next_step_handler(message, get_field)
    


@bot.message_handler(content_types=["text"])
def get_field(message):
    global field
    if message.text.strip() == 'Biomedical' :
        field = 'biomedical'
    elif message.text.strip() == 'Computer Science':
        field = 'cs'
    elif message.text.strip() == 'Chemistry':
        field = 'chemistry'
    elif message.text.strip() == "Schools etc":
        field = 'school'
    if field !='school':
        types.ReplyKeyboardRemove()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1=types.KeyboardButton("BSc")
        item2=types.KeyboardButton("MSc")
        item3=types.KeyboardButton("PHd")
        item4=types.KeyboardButton("Graduates")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, 'Choose degree:',  reply_markup=markup)
        bot.register_next_step_handler(message, get_degree)
    else:
        types.ReplyKeyboardRemove()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1=types.KeyboardButton("Show all")
        markup.add(item1)
        bot.send_message(message.chat.id, 'All programs will be shown:',  reply_markup=markup)
        bot.register_next_step_handler(message, get_country)

def get_degree(message):
    global degree
    if message.text.strip() == 'BSc' :
            degree = 'BS'
    elif message.text.strip() == 'MSc':
            degree = 'MS'
    elif message.text.strip() == 'PhD':
            degree = 'PhD'
    elif message.text.strip() == 'Graduates':
            degree = 'raduate'
    types.ReplyKeyboardRemove()
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1=types.KeyboardButton("Europe")
    item2=types.KeyboardButton("Middle East")
    item3=types.KeyboardButton("Asia")
    item4=types.KeyboardButton("America")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, 'Choose region:',  reply_markup=markup)
    bot.register_next_step_handler(message, get_country)

def get_country(message):
    global region
    global country
    if field !='school':
        if message.text.strip() == 'Europe' :
                region = 'Europe'
        elif message.text.strip() == 'Middle East':
                region = 'ME'
        elif message.text.strip() == 'Asia':
                region = 'Asia'
        elif message.text.strip() == 'America':
                region = 'America'
    
    bot.send_message(message.chat.id, 'Searching...')
    df_selected = get_internships(field, degree, region)
    df_selected = df_selected.reset_index()
    
    if len(df_selected) == 0:
        bot.send_message(message.chat.id, 'Im afraid I have no options for you\n\nPlease try another search')
    else:
        for i in range(len(df_selected)):
            if field=='school':
                bot.send_message(message.chat.id, '# ' + str(i+1) + str('\n*Name:*\n') + str(df_selected.loc[i, "name"]) + '\n*Link:*\n'  + str(df_selected.loc[i, "link"]) + '\n*Field:*\n' + str(df_selected.loc[i, "field"])+ '\n*Country:*\n' + str(df_selected.loc[i, "country"])+ '\n*Degree:*\n' + str(df_selected.loc[i, "degree"])+ '\n*Dates:*\n' + str(df_selected.loc[i, "begin"])+ '\n' + str(df_selected.loc[i, "end"])+ '\n*Allowance:*\n' + str(df_selected.loc[i, "allowance"])+ '\n*Deadline:*\n' + str(df_selected.loc[i, "deadline"]), parse_mode= 'Markdown')
            else:
                bot.send_message(message.chat.id, '# ' + str(i+1) + str('\n*Name:*\n') + str(df_selected.loc[i, "name"]) + '\n*Link:*\n'  + str(df_selected.loc[i, "link"]) + '\n*Country:*\n' + str(df_selected.loc[i, "country"])+ '\n*Dates:*\n' + str(df_selected.loc[i, "begin"])+ '\n' + str(df_selected.loc[i, "end"])+ '\n*Allowance:*\n' + str(df_selected.loc[i, "allowance"])+ '\n*Deadline:*\n' + str(df_selected.loc[i, "deadline"]), parse_mode= 'Markdown')
        bot.send_message(message.chat.id, 'Im afraid I have no more options for you\n\nThanks for using the bot!\nTo find out more about international internships, please examine the table compiled by Victoria Korzhova: \n https://docs.google.com/spreadsheets/d/1rY4nZmy6qcOxmH51qCw1TNtDxcbVhjEtIPEGFLEzDwc/edit#gid=1079784321\n\nHave a nice day 🌸')
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1=types.KeyboardButton("Start")
    item2=types.KeyboardButton("Stop")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Start again:',  reply_markup=markup)
    bot.register_next_step_handler(message, start)



bot.polling(none_stop=True, interval=0)






