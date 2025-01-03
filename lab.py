import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import database

def show_main_app():
    login_window.destroy()
    main_app()

CREDENTIALS_FILE = "users.txt"

def load_credentials():
    credentials = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            lines = file.readlines()
            username = None
            for line in lines:
                line = line.strip()
                if line.startswith("Username:"):
                    username = line.split(": ", 1)[1]
                elif line.startswith("Password:") and username:
                    password = line.split(": ", 1)[1]
                    credentials[username] = password
                    username = None  
    return credentials

def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "a") as file:
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")
        file.write("---------------\n")  

user_credentials = load_credentials()

def login_user():
    username = login_username.get()
    password = login_password.get()
    if username in user_credentials and user_credentials[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        show_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def signup_user():
    username = signup_username.get()
    password = signup_password.get()
    confirm_password = signup_confirm_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
    elif username in user_credentials:
        messagebox.showerror("Error", "Username already exists!")
    else:
        save_credentials(username, password)  
        user_credentials[username] = password  
        messagebox.showinfo("Success", "Account Created Successfully! Please log in.")
        switch_to_login()

def switch_to_signup():
    login_frame.pack_forget()
    signup_frame.pack()

def switch_to_login():
    signup_frame.pack_forget()
    login_frame.pack()

login_window = customtkinter.CTk()
login_window.title("Login / Sign Up")
login_window.geometry("400x400")
login_window.config(bg='#1A1A2E')
login_window.resizable(False, False)

font1 = ('Helvetica', 20, 'bold')
font2 = ('Arial', 14, 'bold')


login_frame = Frame(login_window, bg='#1A1A2E')
login_frame.pack(fill='both', expand=True)

customtkinter.CTkLabel(login_frame, text="Login", font=font1, text_color='#ffffff', bg_color='#1A1A2E').pack(pady=20)

customtkinter.CTkLabel(login_frame, text="Username:", text_color='#ffffff', font=font2, bg_color='#1A1A2E').pack(pady=5)
login_username = customtkinter.CTkEntry(login_frame, width=200)
login_username.pack()

customtkinter.CTkLabel(login_frame, text="Password:", text_color='#ffffff', font=font2, bg_color='#1A1A2E').pack(pady=5)
login_password = customtkinter.CTkEntry(login_frame, show="*", width=200)
login_password.pack()

customtkinter.CTkButton(login_frame, text="Login", command=login_user, fg_color='#6D9E3F', hover_color='#5B7E32').pack(pady=10)
customtkinter.CTkButton(login_frame, text="Create Account", command=switch_to_signup, fg_color='#E05D17', hover_color='#A63E00').pack(pady=5)


signup_frame = Frame(login_window, bg='#1A1A2E')

customtkinter.CTkLabel(signup_frame, text="Sign Up", font=font1, text_color='#ffffff', bg_color='#1A1A2E').pack(pady=20)

customtkinter.CTkLabel(signup_frame, text="Username:", text_color='#ffffff', font=font2, bg_color='#1A1A2E').pack(pady=5)
signup_username = customtkinter.CTkEntry(signup_frame, width=200)
signup_username.pack()

customtkinter.CTkLabel(signup_frame, text="Password:", text_color='#ffffff', font=font2, bg_color='#1A1A2E').pack(pady=5)
signup_password = customtkinter.CTkEntry(signup_frame, show="*", width=200)
signup_password.pack()

customtkinter.CTkLabel(signup_frame, text="Confirm Password:", text_color='#ffffff', font=font2, bg_color='#1A1A2E').pack(pady=5)
signup_confirm_password = customtkinter.CTkEntry(signup_frame, show="*", width=200)
signup_confirm_password.pack()

customtkinter.CTkButton(signup_frame, text="Sign Up", command=signup_user, fg_color='#6D9E3F', hover_color='#5B7E32').pack(pady=10)
customtkinter.CTkButton(signup_frame, text="Back to Login", command=switch_to_login, fg_color='#E05D17', hover_color='#A63E00').pack(pady=5)


def main_app():
    app = customtkinter.CTk()
    app.title('Inventory Management System')
    app.geometry('680x480')
    app.config(bg='#1A1A2E')
    app.resizable(False, False)

    font1 = ('Helvetica', 25, 'bold')
    font2 = ('Arial', 18, 'bold')
    font3 = ('Arial', 13, 'bold')

    def display_data(event):
        selected_item = tree.focus()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()
            id_entry.insert(0, row[0])
            name_entry.insert(0, row[1])
            stock_entry.insert(0, row[2])

    def add_to_treeview():
        products = database.fetch_products()
        tree.delete(*tree.get_children())
        for product in products:
            tree.insert('', END, value=product)

    def clear(*clicked):
        if clicked:
            tree.selection_remove(tree.focus())
            tree.focus('')
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        stock_entry.delete(0, END)

    def delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a product to delete.')
        else:
            id = id_entry.get()
            database.delete_product(id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Data has been deleted.')

    def update():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Select a product to update.')
            return
        id = id_entry.get()
        name = name_entry.get()
        stock = stock_entry.get()
        if not (id and name and stock):
            messagebox.showerror('Error', 'Enter all fields.')
        else:
            try:
                stock_value = int(stock)
                database.update_product(name, stock, id)
                add_to_treeview()
                clear()
                messagebox.showinfo('Success', 'Data has been updated.')
            except ValueError:
                messagebox.showinfo('Error', 'Stock should be an integer.')

    def insert():
        id = id_entry.get()
        name = name_entry.get()
        stock = stock_entry.get()
        if not (id and name and stock):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exist(id):
            messagebox.showerror('Error', 'ID Already exist')
        else:
            try:
                stock_value = int(stock)
                database.insert_product(id, name, stock_value)
                add_to_treeview()
                clear()
                messagebox.showinfo('Success', 'Data has been inserted.')
            except ValueError:
                messagebox.showinfo('Error', 'Stock should be an integer.')

    title_label = customtkinter.CTkLabel(app,font=font1,text='Product Details',text_color='#ffffff',bg_color='#1A1A2E')  
    title_label.place(x=35,y=15)

    frame = customtkinter.CTkFrame(app,bg_color='#1A1A2E',fg_color='#272A43',corner_radius=10,border_width=2,border_color='#ffffff',width=200,height=370)  
    frame.place(x=25,y=45)

    image1 = Image.open('shop.png')  
    image1_resized = image1.resize((75, 75))  
    image1 = ImageTk.PhotoImage(image1_resized)

    image1_label = Label(frame, image=image1, bg='#1B1B21')
    image1_label.place(x=85,y=10)

    id_label = customtkinter.CTkLabel(frame,font=font2,text='Product ID:',text_color='#ffffff',bg_color='#272A43')  
    id_label.place(x=60,y=75)

    id_entry = customtkinter.CTkEntry(frame,font=font2,text_color='#000000',fg_color='#F0F0F0',border_color='#B2016C',border_width=2,width=160)  
    id_entry.place(x=20,y=105)

    name_label = customtkinter.CTkLabel(frame,font=font2,text='Product Name:',text_color='#ffffff',bg_color='#272A43')  
    name_label.place(x=40,y=140)

    name_entry = customtkinter.CTkEntry(frame,font=font2,text_color='#000000',fg_color='#F0F0F0',border_color='#B2016C',border_width=2,width=160)  
    name_entry.place(x=20,y=175)

    stock_label = customtkinter.CTkLabel(frame,font=font2,text='In Stock:',text_color='#ffffff',bg_color='#272A43')  
    stock_label.place(x=60,y=205)

    stock_entry = customtkinter.CTkEntry(frame,font=font2,text_color='#000000',fg_color='#F0F0F0',border_color='#B2016C',border_width=2,width=160)  
    stock_entry.place(x=20,y=240)

    add_button = customtkinter.CTkButton(frame,command=insert,font=font2,text_color='#ffffff',text='Add',fg_color='#6D9E3F',hover_color='#5B7E32',bg_color='#272A43',cursor='hand2',corner_radius=8,width=80)  
    add_button.place(x=15,y=280)

    clear_button = customtkinter.CTkButton(frame,command=lambda:clear(True),font=font2,text_color='#ffffff',text='New',fg_color='#E05D17',hover_color='#A63E00',bg_color='#272A43',cursor='hand2',corner_radius=8,width=80) 
    clear_button.place(x=108,y=280)

    update_button = customtkinter.CTkButton(frame,command=update,font=font2,text_color='#ffffff',text='Update',fg_color='#E05D17',hover_color='#A63E00',bg_color='#272A43',cursor='hand2',corner_radius=8,width=80)  
    update_button.place(x=15,y=320)

    delete_button = customtkinter.CTkButton(frame,command=delete,font=font2,text_color='#ffffff',text='Delete',fg_color='#D22C02',hover_color='#8A0800',bg_color='#272A43',cursor='hand2',corner_radius=8,width=80)  
    delete_button.place(x=108,y=320)

    style = ttk.Style(app)

    style.theme_use('clam')
    style.configure('Treeview',font=font3,foreground='#ffffff',background='#1A1A2E',fieldbackground='#272A43')  
    style.map('Treeview',background=[('selected', '#AA04A7')])

    tree = ttk.Treeview(app,height=21)

    tree['columns'] = ('ID', 'Name', 'In Stock')

    tree.column('#0',width=0,stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=170)
    tree.column('Name',anchor=tk.CENTER,width=170)
    tree.column('In Stock',anchor=tk.CENTER,width=170)

    tree.heading('ID',text='ID')
    tree.heading('Name',text='Name')
    tree.heading('In Stock',text='In Stock')

    tree.place(x=300,y=60)
    tree.bind('<ButtonRelease>', display_data)

    add_to_treeview()
    
    app.mainloop()
    
login_window.mainloop()