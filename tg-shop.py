import time, datetime
from peewee import *
import telebot
from telebot import types
from model import Client, Order, Product, create_products, db, get_client, get_client_status, new_client
# from operator import add

REQUEST_NAME = 1
REQUEST_ADDRESS = 2
REQUEST_PHONE = 3

bot = telebot.TeleBot("1871011212:AAElCnNTa4bisSn7DA45jpIgWeX-A1A63aY")

db.connect()
db.create_tables([Product, Client, Order])

category_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
category_markup.add('Шампуни').add( 'Средства для ухода').add('Средства для мытья посуды')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    c = get_client(message)
    if c:
        bot.reply_to(message, "C возвращением в наш магазин!")
        bot.send_message(message.chat.id, 'Посмотрите на наш ассортимент', reply_markup=category_markup)
    else:
        bot.reply_to(message, "Приветствую, я бот-магазин экопродуктов.")
        
        new_client(message.chat.id)

        bot.send_message(message.chat.id, 'Напишите ФИО')


@bot.message_handler(commands=['orders'])
def list_orders(message):
    if message.chat.id == 62144137:
        orders = Order.select()
        msg = ''
        for order in orders:
            client = Client.get_by_id(order.client_id)
            product = Product.get_by_id(order.product_id)
            msg += f'{order.id}: {client.name} {client.address} {client.phone} -- {product.name}:{product.price}' + '\n'
        
        bot.send_message(message.chat.id, msg)
    else:
        print('Nothing')

@bot.message_handler(commands=['create'])
def list_orders(message):
    if message.chat.id == 62144137:
        create_products()


@bot.message_handler(func = lambda message: get_client_status(message) == REQUEST_NAME)
def request_name(message):
    c = get_client(message)
    if c:
        c.name = message.text
        c.state = 2
        c.save()
        bot.send_message(message.chat.id, 'Напишите адрес')
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден. нажмите /start')

@bot.message_handler(func = lambda message: get_client_status(message) == REQUEST_ADDRESS)
def request_address(message):
    c = get_client(message)
    if c:
        c.address = message.text
        c.state = 3
        c.save()
        bot.send_message(message.chat.id, 'Напишите Телефон')

    else:
        bot.send_message(message.chat.id, 'Пользователь не найден. нажмите /start')

@bot.message_handler(func = lambda message: get_client_status(message) == REQUEST_PHONE)
def request_address(message):
    c = get_client(message)
    if c:
        c.phone = message.text
        c.state = 0
        c.save()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Нажмите список продуктов.', reply_markup=category_markup)
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден. нажмите /start')

@bot.message_handler(func = lambda message: get_client_status(message) == 0)
def show_category(message):
    products = Product.select().where(Product.category == message.text)
    for product in products:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Купить', callback_data="id:" + str(product.id))
        markup.add(btn)
        with open(product.img, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f'{product.name} - {product.price}Р', reply_markup=markup)
        time.sleep(2)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # print(call.message.chat.id)
    order = Order(
        product_id = call.data.split(':')[1],
        client_id = Client.get(Client.chat_id == call.message.chat.id),
        date = datetime.datetime.now()
    )
    order.save()
    bot.answer_callback_query(call.id, f'Ваш заказ №{order.id} принят')
    bot.send_message(call.message.chat.id, f'Ваш заказ №{order.id} принят')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()