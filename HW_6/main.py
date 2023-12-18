"""Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц:
товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля:
id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API."""

import datetime
from pydantic import BaseModel, Field
from hashlib import sha256
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates

DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
database = Database(DATABASE_URL)
Base = declarative_base()
templates = Jinja2Templates(directory='templates')


# Модель FastAPI
class Product(BaseModel):
    id: int = Field(default=None, alias='prod_id')
    name: str = Field(max_length=20)
    description: str = Field(max_length=100)
    price: int = Field(default=None)


class User(BaseModel):
    id: int = Field(default=None, alias='user_id')
    name: str = Field(min_length=3, max_length=20)
    surname: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=10, max_length=100)
    password: str = Field(min_length=12, max_length=100)


class Order(BaseModel):
    id: int = Field(default=None, alias='order_id')
    user_id: int = Field(default=None, alias='user_id')
    prod_id: int = Field(default=None, alias='prod_id')
    order_date: datetime.date
    order_status: bool = Field(default=False)


# Модель SQL
class BdUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(100))
    password = Column(String(100))


class BdProd(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20))
    description = Column(String(100))
    price = Column(Integer, nullable=False)


class BdOrder(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prod_id = Column(Integer, ForeignKey('BdProd.id'), nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('BdUser.id'), nullable=False, autoincrement=True)
    order_date = Column(DateTime)
    order_status = Column(Boolean)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# Пользователи
@app.get('/users/', response_class=HTMLResponse)
async def read_users(request: Request):
    query = BdUser.__table__.select()
    users = await database.fetch_all(query)
    table = pd.DataFrame([user for user in users]).to_html()
    return templates.TemplateResponse('users.html', {'request': request, 'table': table})


@app.post('/users/', response_model=User)
async def create_user(user: User):
    user.password = sha256(user.password.encode(encoding='utf-8')).hexdigest()
    date = vars(user)
    del date['id']
    query = BdUser.__table__.insert().values(date)
    user.id = await database.execute(query)
    return user


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user: User):
    user.password = sha256(user.password.encode(encoding='utf-8')).hexdigest()
    date = vars(user)
    del date['id']
    query = BdUser.__table__.update().where(BdUser.id == user_id).values(date)
    user.id = await database.execute(query)
    return user


@app.delete('/users/{user_id}')
async def del_user(user_id: int):
    query = BdUser.__table__.delete().where(BdUser.id == user_id)
    await database.execute(query)
    return {'message': 'User was deleted'}


# Продукты
@app.get('/products/', response_class=HTMLResponse)
async def read_product(request: Request):
    query = BdProd.__table__.select()
    prod_s = await database.fetch_all(query)
    table = pd.DataFrame([prod for prod in prod_s]).to_html()
    return templates.TemplateResponse('products.html', {'request': request, 'table': table})


@app.post('/products/', response_model=Product)
async def create_product(prod: Product):
    date = vars(prod)
    del date['id']
    query = BdProd.__table__.insert().values(date)
    prod.id = await database.execute(query)
    return prod


@app.put('/products/{prod_id}', response_model=Product)
async def update_product(prod_id: int, prod: Product):
    date = vars(prod)
    del date['id']
    query = BdProd.__table__.update().where(BdProd.id == prod_id).values(date)
    prod.id = await database.execute(query)
    return prod


@app.delete('/products/{prod_id}')
async def del_product(prod_id: int):
    query = BdProd.__table__.delete().where(BdProd.id == prod_id)
    await database.execute(query)
    return {'message': 'Product was deleted'}


# Заказы
@app.get('/orders/', response_class=HTMLResponse)
async def read_order(request: Request):
    query = BdOrder.__table__.select()
    orders = await database.fetch_all(query)
    table = pd.DataFrame([order for order in orders]).to_html()
    return templates.TemplateResponse('orders.html', {'request': request, 'table': table})


@app.post('/orders/', response_model=Order)
async def create_order(order: Order):
    date = vars(order)
    del date['id']
    query = BdOrder.__table__.insert().values(date)
    order.id = await database.execute(query)
    return order


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(order_id: int, order: Order):
    date = vars(order)
    del date['id']
    query = BdOrder.__table__.update().where(BdOrder.id == order_id).values(date)
    order.id = await database.execute(query)
    return order


@app.delete('/orders/{order_id}')
async def del_order(order_id: int):
    query = BdOrder.__table__.delete().where(BdOrder.id == order_id)
    await database.execute(query)
    return {'message': 'Order was deleted'}
