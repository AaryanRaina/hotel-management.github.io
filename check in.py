from tkinter import *
import sqlite3
from tkinter import messagebox
import os
global room
from datetime import date
room=open("rooms.txt", "r")


def submit_checkin():

    if os.stat("rooms.txt").st_size!=0:
        global no_guest_info
        name_info=name.get()
        phone_info=phone.get()
        address_info=address.get()
        no_guest_info=no_guest.get()
        room_type_info=room_type.get()
        date_info=date0.get()
        month_info=month.get()
        year_info=year.get()
        room=open("rooms.txt", "r")
        line1 = room.readline()
        output = []
        for line in room:
            if not line.startswith(line1):
                output.append(line)
        room.close()
        room = open("rooms.txt", 'w')
        room.writelines(output)
        room.close()
        conn= sqlite3.connect('guest.db')
        with conn:
            cursor=conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS guest (name_info TEXT,phone_info TEXT,date_info TEXT,month_info TEXT,year_info TEXT,address_info TEXT,no_guest_info TEXT,room TEXT,room_type_info TEXT)')
        cursor.execute('INSERT INTO guest (name_info,phone_info,date_info,month_info,year_info,address_info,no_guest_info,room,room_type_info) VALUES(?,?,?,?,?,?,?,?,?)',(name_info,phone_info,date_info,month_info,year_info,address_info,no_guest_info,line1,room_type_info,))
        conn.commit()
        c="YOU HAVE BEEN ALLOTED ROOM NO. "+ line1
        messagebox.showinfo("SHIKARA HOTEL",c)
    else:
        messagebox.showinfo("SHIKARA HOTEL","SORRY! NO  VACANCY")
    window1.destroy()
   

    
def check_in():
    global window1
    window1=Toplevel(window)
    window1.title("CHECK IN INTO SHIKARA HOTEL")
    window1.geometry("500x550")

    Label(window1,text="NAME :",font=("Calibiri",10)).pack()
    Entry(window1,textvariable = name).pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Label(window1,text="PHONE NUMBER : ",font=("Calibiri",10)).pack()
    Entry(window1,textvariable = phone).pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Label(window1,text="DATE: ",font=("Calibiri",10)).place(x=75,y=150)
    Entry(window1,textvariable = date0).place(x=120,y=150)
    Label(window1,text="MONTH: ",font=("Calibiri",10)).place(x=200,y=150)
    Entry(window1,textvariable = month).place(x=250,y=150)
    Label(window1,text="YEAR: ",font=("Calibiri",10)).place(x=300,y=150)
    Entry(window1,textvariable = year).place(x=350,y=150)
    Label(window1,text='').pack()
    Label(window1,text="ADDRESS : ",font=("Calibiri",10)).pack()
    Entry(window1,textvariable =address ).pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Label(window1,text="NO. OF GUEST : ",font=("Calibiri",10)).pack()
    Entry(window1,textvariable = no_guest).pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Label(window1,text="ROOM TYPE : ",font=("Calibiri",10)).pack()
    Radiobutton(window1,text="Deluxe",padx = 5, variable=room_type,value=1).pack()
    Radiobutton(window1,text="Presidential",padx = 5, variable=room_type,value=2).pack()
    Label(window1,text='').pack()
    Label(window1,text='').pack()
    Button(window1,text = "SUBMIT",width = 10,height=1,command=submit_checkin).pack()

def check_out():
    global window2
    window2=Toplevel(window)
    window2.title("CHECK OUT FROM SHIKARA HOTEL")
    window2.geometry("500x550")

    global name1,phone1,date1,month1,year1,payment_mode
    name1=StringVar()
    phone1=StringVar()
    date1=IntVar()
    month1=IntVar()
    year1=IntVar()
    payment_mode=IntVar()
    
    Label(window2,text="NAME :",font=("Calibiri",10)).pack()
    Entry(window2,textvariable = name1).pack()
    Label(window2,text='').pack()
    Label(window2,text='').pack()
    Label(window2,text="PHONE NUMBER : ",font=("Calibiri",10)).pack()
    Entry(window2,textvariable = phone1).pack()
    Label(window2,text='').pack()
    Label(window2,text='').pack()
    Label(window2,text="PAYMENT MODE : ",font=("Calibiri",10)).pack()
    Radiobutton(window2,text="CASH",padx = 5, variable= payment_mode,value=1).pack()
    Radiobutton(window2,text="CARD",padx = 5, variable=payment_mode,value=2).pack()
    Label(window2,text='').pack()
    Button(window2,text = "MAKE PAYMENT" ,width = 15,height=1,command=payment).pack()

def payment():
    global payment_mode_set
    payment_mode_set=""
    name1_info=name1.get()
    phone1_info=phone1.get()
    payment_mode_info=payment_mode.get()
    conn= sqlite3.connect('guest.db')
    with conn:
            cursor=conn.cursor()
    cursor.execute("select * from guest")
    conn.commit()
    var=cursor.fetchall()
    l1=[]
    for row in var :
        l1.append(row)
    if payment_mode_info==1:
        payment_mode_set="CASH"
    elif payment_mode_info==2:
        payment_mode_set="CARD"
    for i in range(len(l1)):
        if l1[i][0]==name1_info and l1[i][1]==phone1_info:
            if l1[i][8]=='2':
                d1 = date.today()
                d0 = date(int(l1[i][4]),int(l1[i][3]),int(l1[i][2]))
                delta = d1 - d0
                bill1 = delta.days*1500
                bill2 = delta.days*(int(l1[i][6])*100)
                final_bill=bill1+bill2
                c="YOUR STAY WAS FOR : "+ str(delta.days) + " DAYS AND " +"YOUR FINAL BILL IS : "+ str(final_bill)
                messagebox.showinfo("THANKS FOR YOUR STARY IS SHIKARA",c)
                conn= sqlite3.connect('guest.db')
                with conn:
                    cursor=conn.cursor()
                cursor.execute("DELETE FROM guest WHERE name_info = ? and phone_info= ?;",(name1_info,phone1_info,))
                conn.commit()
                room1=open("rooms.txt", "a")
                room1.write(l1[i][7])
                room1.close()
                conn= sqlite3.connect('totalCUSTOMERS.db')
                with conn:
                    cursor=conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS guest (name TEXT,phone TEXT,check_in DATE,check_out DATE,room_type TEXT,room_alloted TEXT,payment TEXT,payment_mode TEXT)')
                cursor.execute('INSERT INTO guest (name,phone,check_in,check_out,room_type,room_alloted,payment,payment_mode) VALUES(?,?,?,?,?,?,?,?)',(name1_info,phone1_info,d0,d1,l1[i][8],l1[i][7],final_bill,payment_mode_set,))
                conn.commit()
                window2.destroy()
            elif l1[i][8]=='1':
                d1 = date.today()
                d0 = date(int(l1[i][4]),int(l1[i][3]),int(l1[i][2]))
                delta = d1 - d0
                bill1 = delta.days*1100
                bill2 = delta.days*(int(l1[i][6])*80)
                final_bill=bill1+bill2
                c="YOUR STAY WAS FOR : "+ str(delta.days) + " DAYS AND " +"YOUR FINAL BILL IS : "+ str(final_bill)
                messagebox.showinfo("THANKS FOR YOUR STARY IS SHIKARA",c)
                conn= sqlite3.connect('guest.db')
                with conn:
                    cursor=conn.cursor()
                cursor.execute("DELETE FROM guest WHERE name_info = ? and phone_info= ?;",(name1_info,phone1_info,))
                conn.commit()
                room1=open("rooms.txt", "a")
                room1.write(l1[i][7])
                room1.close()
                conn= sqlite3.connect('totalCUSTOMERS.db')
                with conn:
                    cursor=conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS guest (name TEXT,phone TEXT,check_in DATE,check_out DATE,room_type TEXT,room_alloted TEXT,payment TEXT,payment_mode TEXT)')
                cursor.execute('INSERT INTO guest (name,phone,check_in,check_out,room_type,room_alloted,payment,payment_mode) VALUES(?,?,?,?,?,?,?,?)',(name1_info,phone1_info,d0,d1,l1[i][8],l1[i][7],final_bill,payment_mode_set,))
                conn.commit()
                window2.destroy()


def show_guest_list():
    global window3
    window3=Toplevel(window)
    window3.title("SHIKARA HOTEL GUEST LIST")
    window3.geometry("600x600")
    g=""
    h=""
    conn= sqlite3.connect('guest.db')
    with conn:
            cursor=conn.cursor()
    cursor.execute("select * from guest")
    conn.commit()
    var=cursor.fetchall()
    l2=[]
    for row in var :
        l2.append(row)
    for i in range(len(l2)):
        g = " Name: "+ l2[i][0]+" Phone: "+ l2[i][1]+" Check in: "+ str(l2[i][2])+"/"+str(l2[i][3])+"/"+str(l2[i][4])+" Room No.: "+str(l2[i][7])+"\n"
        h=h+g
    guests = StringVar()
    guests.set(h)
    Label(window3,text='').pack()
    Label(window3,text='').pack()
    l1 = Label(window3, textvariable=guests,font=("Calibiri",10)).pack()

def exit_shikara():

    window.destroy()
    
def total_customers():
    global window4
    window4=Toplevel(window)
    window4.title("SHIKARA HOTEL CUSTOMERS LIST")
    window4.geometry("800x700")
    g=""
    h=""
    conn= sqlite3.connect('totalCUSTOMERS.db')
    with conn:
            cursor=conn.cursor()
    cursor.execute("select * from guest")
    conn.commit()
    var=cursor.fetchall()
    l2=[]
    for row in var :
        l2.append(row)
    for i in range(len(l2)):
        g = " Name: "+ l2[i][0]+" Phone: "+ l2[i][1]+" Check in: "+ str(l2[i][2])+" Check out: "+ str(l2[i][3]) + " Alloted Room No.: "+str(l2[i][5])+ " Payment: "+str(l2[i][6])+ " Payment Mode: "+str(l2[i][7])+ "\n\n"
        h=h+g
    
    guests = StringVar()
    guests.set(h)
    Label(window4,text='').pack()
    Label(window4,text='').pack()
    l1 = Label(window4, textvariable=guests,font=("Calibiri",10)).pack()
        
        
def main_screen():
    global window
    window=Tk()
    window.geometry("1500x850")
    window.title("SHIKARA HOTEL")

    global name,phone,address,no_guest,room_type,date0,month,year
    name=StringVar()
    phone=StringVar()
    address=StringVar()
    no_guest=IntVar()
    room_type=IntVar()
    date0=IntVar()
    month=IntVar()
    year=IntVar()

    Label(text="Welcome to SHIKARA",bg = "grey",width="1000",height="2",font=("Calibiri",15)).pack()
    Label(text='').pack()
    icon=PhotoImage(file = "C:\\Users\\Aaryan\\Desktop\\python mini project\\xx1.png")
    label1=Label(window, image=icon)
    label1.pack()
    Label(text='').pack()
    Button(text="CHECK IN",height="2",width="100",command=check_in).pack()
    Label(text='').pack()
    Button(text="CHECK OUT",height="2",width="100",command=check_out).pack()
    Label(text='').pack()
    Button(text="SHOW GUEST LIST",height="2",width="100",command=show_guest_list).pack()
    Label(text='').pack()
    Button(text="SHOW TOTAL CUSTOMER LIST",height="2",width="100",command=total_customers).pack()
    Label(text='').pack()
    Button(text="EXIT",height="2",width="100",command=exit_shikara).pack()
    window.mainloop()
main_screen()

