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


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from invoice import sales_inv
from invoice import get_inv_list
from datetime import datetime

#Actions of our buttons: 

#Get selection from the treeview
def inv_selection(treeview):
    model,treeiter=treeview.get_selected()
    if treeiter is not None:
        return sales_inv(tuple(model[treeiter]))
        
    
    

#Display add window.
def add_clicked(self,store):
    inv=sales_inv()
    _display_edit_win(store,inv)

#Display edit window.
def edit_clicked(self,store,selection):
    inv=inv_selection(selection)
    _display_edit_win(store,inv)

#Display confirm delete window.
def remove_clicked(self,store,selection):
    inv=inv_selection(selection)
    print(inv)
    _display_confirm_win(store,inv)

#Toggles between sales in purchases
def sales_toggled(self):
    print("Hello World!")

#Close window 
def close(self,window):
    window.destroy()

#Display confirm window to delete entry
def _display_confirm_win(store,inv):
    builder=Gtk.Builder()
    builder.add_from_file("./glade/remove.glade")
    confirm_win=builder.get_object("confirm_win")
    c_text=builder.get_object("confirm_text")
    c_text.set_text("Are you sure you want to delete : \n{}".format(inv))
    close_button=builder.get_object("cancel")
    close_button.connect("clicked",close,confirm_win)
    ok_button=builder.get_object("confirm")
    ok_button.connect("clicked",remove_inv,store,inv,confirm_win)
    confirm_win.show_all()


#Display warning, error passed as str.
def _display_warning(error="An error has occured"):
    builder=Gtk.Builder()
    builder.add_from_file("./glade/error.glade")
    warning_win=builder.get_object("error_box")
    close_button=builder.get_object("close_button")
    close_button.connect("clicked",close,warning_win)
    warning_text=builder.get_object("error_label")
    warning_text.set_text(error)
    warning_win.show_all()

#remove entry from db and update the store
def remove_inv(self,store,inv,win):
    inv.remove_from_db()
    _build_list_store(store)
    win.destroy()

#Save entry or display warning if input data invalid.
#Precondition : builder as the gtk builder for the edit window
def save_entry(self,builder,store):
    invoice= sales_inv()
    for key in invoice:
        try :
            entry=builder.get_object(key)
            invoice[key]=entry.get_text()
        except AttributeError:
            entry=builder.get_object("id_label")
            if entry.get_text()=="None":
                invoice["id"]=None
            else:
                invoice["id"]=int(entry.get_text())
    try:
        invoice.c_and_c()
        invoice.save_in_db()
        builder.get_object("edit_sales_window").destroy()
        _build_list_store(store)
    except ValueError:
        _display_warning("One or more entries are not valid. Please check and try again.")

#Build and display windows :

#Build and display the edit window, also used as the add window.
def _display_edit_win(store,inv):
    #Build window from glade file
    builder=Gtk.Builder()
    builder.add_from_file("./glade/edit_sales_window.glade")
    edit_win=builder.get_object("edit_sales_window")
    #Setup text field
    for key in inv:
        try :
            entry=builder.get_object(key)
            entry.set_text(str(inv[key]))
        except AttributeError:
            entry=builder.get_object("id_label")
            entry.set_text(str(inv["id"]))
    #Connect buttons
    cancel_button=builder.get_object("cancel")
    cancel_button.connect("clicked",close,edit_win)
    input_box=builder.get_object("input_box") 
    save_button=builder.get_object("saved")
    save_button.connect("clicked",save_entry,builder,store)
    #Display window
    edit_win.show_all()

def _build_list_store(store):
    inv_list=get_inv_list()
    store.clear()
    for inv in inv_list:
        inv["inv_date"]=datetime.strftime(datetime.strptime(inv["inv_date"],"%Y-%m-%d"),"%d-%m-%y")
        store.append([inv["id"],inv["inv_number"],inv["inv_date"],inv["inv_name"],inv["inv_amount"],inv["inv_taxes"],inv["inv_perc_taxes"]])

#Build and display the main window.
def display_main_window():
    #Build window from glade file.
    builder=Gtk.Builder()
    builder.add_from_file("./glade/main_window.glade")
    window=builder.get_object("main_window")
    window.connect("destroy",Gtk.main_quit)
    #connect list_store to data
    store=builder.get_object("inv_list")
    _build_list_store(store)
    #Get selection from treeview
    selection=builder.get_object("tree_selected")
    #Connects buttons.
    add_button=builder.get_object("add")
    edit_button=builder.get_object("edit")
    add_button.connect("clicked",add_clicked,store)
    edit_button.connect("clicked",edit_clicked,store,selection)
    remove_button=builder.get_object("remove")
    remove_button.connect("clicked",remove_clicked,store,selection)
    #display_main_window.
    window.show_all()
    Gtk.main()

