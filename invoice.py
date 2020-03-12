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

from datetime import date
from datetime import datetime
import database

class sales_inv(dict):
    def __init__(self,list_inv=(None,"0",datetime.strftime(date.today(),"%d-%m-%y"),"Client's Name",0.0,0.0,0.0)):
        dict.__init__(self)
        self["id"]=list_inv[0]
        self["inv_number"]=list_inv[1]
        self["inv_date"]=list_inv[2]
        self["inv_name"]=list_inv[3]
        self["inv_amount"]=list_inv[4]
        self["inv_taxes"]=list_inv[5]
        self["inv_perc_taxes"]=list_inv[6]

    def c_and_c(self):
        self["inv_date"]=datetime.strptime(self["inv_date"],"%d-%m-%y").date()
        self["inv_amount"]=float(self["inv_amount"])
        self["inv_perc_taxes"]=float(self["inv_perc_taxes"])
        self["inv_taxes"]=float(self["inv_taxes"])

    def save_in_db(self):
        if self["id"]!=None:
            self.remove_from_db()
        database.commit_to_db(tuple(self.values()))
    
    def remove_from_db(self):
        database.delete_from_db((self["id"],))

    
    def __repr__(self):
      return "ID : {} |Invoice : {}|Date : {}|Client : {}|HTVA : {}|TVA : {}|Taux TVA : {}%".format(self["id"],self["inv_number"],self["inv_date"],self["inv_name"],self["inv_amount"],self["inv_taxes"],self["inv_perc_taxes"])

def get_inv_list():
    inv_list=database.import_db()
    return (sales_inv(x) for x in inv_list)
