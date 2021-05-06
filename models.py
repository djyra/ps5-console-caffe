#! /usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
	__tablename__ = 'product'

	id = Column('id', Integer, primary_key=True)
	name = Column('name', String, unique=True)
	price = Column('price', Integer)
	stock = Column('stock', Integer)

class Sale(Base):
	__tablename__ = 'sale'

	id = Column('id', Integer, primary_key=True)
	date_of_sale  = Column('date_of_sale', DateTime)
	total = Column('total', Integer)


class Sale_item(Base):
	__tablename__ = 'sale_item'

	id = Column('id', Integer, primary_key=True)
	quantity_sold = Column('quantity_sold', Integer)
	product_id = Column('product_id', ForeignKey(Product.id))
	sale_id = Column('sale_id', ForeignKey(Sale.id))
