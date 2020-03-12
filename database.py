#!/usr/bin/python3
# -*-coding:utf-8 -*-
""" Copyright 2020 Julien Gielen
    This file is part of the Simple Accounting Software.

    Simple Accounting Software is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Simple Accounting Software is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Simple Accounting Software.  If not, see <https://www.gnu.org/licenses/>."""

import sqlite3

def init_db():
    conn=sqlite3.connect("account.db")
    cur=conn.cursor()
    sql_create_tables="""
    CREATE TABLE sales ( 
        id INTEGER, 
        inv_number VARCHAR(31), 
        inv_date DATE, 
        inv_name CHAR(63), 
        inv_amount FLOAT,
        inv_taxes FLOAT,
        inv_perc_taxes FLOAT,
        PRIMARY KEY (id)
        );"""
    #cur.execute(sql_create_tables)
    conn.commit()
    conn.close()

def commit_to_db(inv):
    conn=sqlite3.connect("account.db")
    cur=conn.cursor()
    cur.execute("""
    INSERT INTO sales
    VALUES(?,?,?,?,?,?,?);""",
    inv)
    conn.commit()
    conn.close()

#connect to db and return a list of tuple
def import_db():
    conn=sqlite3.connect("account.db")
    cur=conn.cursor()
    db=[]
    for row in conn.execute("SELECT * FROM sales"):
        db.append(row)
    conn.close()
    return db

def delete_from_db(id_n):
    conn=sqlite3.connect("account.db")
    cur=conn.cursor()
    cur.execute("""
    DELETE FROM sales WHERE id=?;""",id_n)
    conn.commit()
    conn.close()