#! /usr/bin/env python

import sqlite3

def insert(time, sony, time_booked):
	with sqlite3.connect('data/db.sqlite3') as conn:
		with conn.cursor() as cur:
			cur.execute('INSERT INTO ps_time (time_started, sony, time_booked) values (?, ?, ?);', (time, sony, time_booked))

def food_and_drinks(time, sony, drink): # TODO
	with sqlite3.connect('data/db.sqlite3') as conn:
		with conn.cursor() as cur:
			cur.execute('INSERT INTO;') 

def storno_sony():
	with sqlite3.connect('data/db.sqlite3') as conn:
		with conn.cursor() as cur: 
			cur.execute('DELETE FROM ps_time WHERE id = (SELECT MAX(id) FROM notes);')

def storno_food_and_drinks(): # TODO
	with sqlite3.connect('data/db.sqlite3') as conn:
		with conn.cursor() as cur: 
			cur.execute('DELETE FROM ')