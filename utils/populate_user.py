import csv
import os
import sqlite3
from werkzeug.security import generate_password_hash
# basedir = os.path.abspath(os.path.dirname())
# change to 'sqlite:///your_filename.db'
# SQLALCHEMY_DATABASE_URI =os.path.join(basedir, 'app.db')
filepath='/home/aliz/Thriftshop_Nepal/app.db'
con = sqlite3.connect(filepath)
cur = con.cursor()
# use your column names here

with open('app/userdetails.csv', 'r') as fin:  # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    to_db = [(int(i["id"]), i["username"], i["firstname"], i["lastname"],i["email"],  generate_password_hash(i["password"]),
              i['user_type']
              ) for i in dr]
    print(dr)

cur.executemany(
    "INSERT INTO user (id, username, firstname, lastname, email, password_hash, user_type) VALUES (?,?,?, ?,?,?,?);", to_db)
con.commit()
con.close()
