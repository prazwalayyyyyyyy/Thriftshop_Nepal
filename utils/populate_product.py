import csv
import os
import random
import sqlite3
from werkzeug.security import generate_password_hash
# basedir = os.path.abspath(os.path.dirname())
# change to 'sqlite:///your_filename.db'
# SQLALCHEMY_DATABASE_URI =os.path.join(basedir, 'app.db')
filepath='/home/aliz/Thriftshop_Nepal/app.db'
con = sqlite3.connect(filepath)
cur = con.cursor()
# use your column names here


to_db = [(i,  "photo.png",f"product_name-{i}", random.choices([2,3,6])[0],
     random.choices([True, False])[0], 
     random.choices(["Male", "Female"])[0], 
     random.choices(["New", "Used Many times", "Good"])[0], random.randrange(200,2000), 2001,
              10
              ) for i in range(10001,10030)]
cur.executemany(
    "INSERT INTO goods (id, photo, name, seller, verifycheck, category, condition, buy_price, sell_price, profit) VALUES (?,?,?, ?,?,?,?,?,?,?);", to_db)
con.commit()
con.close()
