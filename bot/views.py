from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Button, Text
import requests
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('994604539:AAGsEMWEDW93la7rQ5c0JYv62sHiVTu5X1g')


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


class GetList(APIView):
    def get(self, request):
        data = {'list': []}
        button = Button.objects.all()
        for i in button:
            data['list'].append({'name': i.button})
        return Response(data)


class ButtonText(APIView):
    def post(self, request):
        data = json.loads(request.body)
        try:
            get_button = Button.objects.get(button=data['text'])
            text = Text.objects.get(button=get_button)
            return Response({"text": text.text, "code": 200})
        except:
            return Response({"code": 401})


def button_def(message):
    # r = requests.get('https://wikishop.herokuapp.com/api/button')
    # data = json.loads(r.text)
    button_list = Button.objects.all()
    text = 'سلام {}'.format(message.from_user.first_name)
    key = ReplyKeyboardMarkup(True, False)

    # for i in range(len(data['list'])):
    #     button = KeyboardButton(data['list'][i]['name'])
    #     key.add(button)
    for i in range(button_list):
        # bot.send_message(message.chat.id, button)
        bot.send_message(message.chat.id, 'before key')
        key_button = KeyboardButton(b)
        # bot.send_message(message.chat.id, 'middle key')
        key.add(key_button)
        bot.send_message(message.chat.id, 'after key')
    bot.send_message(message.from_user.id, text, reply_markup=key)

'''
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    print("build_menu started")
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    print("after menu")
    if header_buttons:
        menu.insert(0, [header_buttons])
    print("before if footer")
    if footer_buttons:
        menu.append([footer_buttons])
    print("before return")
    return menu
'''

'''
@bot.message_handler(commands=['start'])
def start(message):
    button_def(message)

@bot.message_handler(content_types='text')
def send_message(message):
    link = 'https://wikishop.herokuapp.com/api/text'
    text = {"text":message.text}
    r = requests.post(link, data=json.dumps(text))
    data = json.loads(r.text)

    if data['code'] == 401:
        bot.send_message(message.from_user.id, 'sorry {} some tokhmi takhayoli problem'.format(message.from_user.first_name))
    else:
        wiki = data['text']
        bot.send_message(message.from_user.id, wiki)

# bot.polling()


'''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi {}'.format(message.from_user.first_name))
    user = User()
    user.user_id = message.chat.id
    user.save()
    print("before button_list")
    button_list = Button.objects.all()
    print("after button list")
    # for button in button_list:
    #     bot.send_message(message.chat.id, button)
    # button_def(message)
    # build_menu(button_list, 1)

    text = 'سلام {}'.format(message.from_user.first_name)
    key = ReplyKeyboardMarkup(True, False)
    bot.send_message(message.chat.id, "before for i")
    for i in range(len(button_list)):
        button = KeyboardButton(button_list[i])
        key.add(button)
    bot.send_message(message.from_user.id, text, reply_markup=key)


@bot.message_handler(commands=['هی'])
def hei(message):
    bot.send_message(message.chat.id, 'با هر ردیف کلمه /بعدی را تایپ کنید')


@bot.message_handler(content_types='text')
def send_Message(message):
    bot.send_message(message.chat.id, 'روی هی/ کلیک کنید')
