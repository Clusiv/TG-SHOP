from peewee import *

db = SqliteDatabase('shop.db')

class Product(Model):
    name = CharField()
    price = IntegerField()
    img = CharField()
    category = CharField()

    class Meta:
        database = db

class Client(Model):
    name = CharField()
    address = CharField()
    phone = CharField()
    chat_id = CharField()
    state = IntegerField()

    class Meta:
        database = db
    
class Order(Model):
    product_id = IntegerField()
    date = DateField()
    client_id = IntegerField()

    class Meta:
        database = db


def get_client(message):
    return Client.get_or_none(Client.chat_id == message.chat.id)

def get_client_status(message):
    c = Client.get_or_none(Client.chat_id == message.chat.id)
    if c:
        return c.state
    else:
        return -1

def new_client(chat_id):
    Client(name='', 
        address='', 
        phone='', 
        chat_id = chat_id,
        state = 1).save()

def create_products():
    Product(
        name = 'Шампунь Mi&Ko Cold Ice', 
        price = 740, 
        img = '1.jpeg', 
        category = 'Шампуни'
        ).save()
    Product(
        name = 'Эко сода', 
        price = 115, 
        img = '2.jpg', 
        category = 'Средства для мытья посуды'
        ).save()
    Product(
        name = 'Washing Pro', 
        price = 248, 
        img = '3.jpg', 
        category = 'Средства для мытья посуды'
        ).save()