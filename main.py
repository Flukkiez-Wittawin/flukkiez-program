import tkinter
import requests
from tkinter import messagebox
from typing import Optional, Tuple, Union
import customtkinter as ctk
from pymongo import MongoClient
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser


ctk.set_appearance_mode("Dark")
icon = 'file/icon/icon.ico'


client = MongoClient(
    f"") # ใส่ MongoDB 
db = client["mydb"]
collection = db["users"]
collection_project = db['project']


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('FlukKieZ start lanucher')
        self.geometry('200x100')
        self.resizable(False, False)
        self.iconbitmap(f'{icon}')

        def gomain2():

            self.destroy()
            main = Login_Page()
            main.mainloop()

        start_button = ctk.CTkButton(self, text=f'START', command=gomain2)
        start_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def on_closing():
            print("Window is closing.")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_closing)


class Login_Page(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('LOGIN')
        self.geometry('500x400')
        self.resizable(False, False)
        self.iconbitmap(f'{icon}')

        def login():
            username = username_entry.get()
            password = password_entry.get()

            print(f'{username}:{password}')
            if not username or not password:
                messagebox.showerror(
                    "Error", "Username and Password are required.")
                return

            user = collection.find_one(
                {"username": username, "password": password})
            if user:
                self.destroy()
                messagebox.showinfo("Success", "Login successful!")
                home = Hompage(username)
                home.mainloop()

            else:
                messagebox.showerror("Error", "Invalid username or password.")
                return

        def register():

            self.destroy()
            main = Register_Page()
            main.mainloop()

        user_label = ctk.CTkLabel(self, text=f'Username : ')
        password_label = ctk.CTkLabel(self, text=f'Password : ')
        username_entry = ctk.CTkEntry(self)
        password_entry = ctk.CTkEntry(self, show='*')
        user_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        username_entry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        password_label.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)
        password_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        start_button = ctk.CTkButton(self, text=f'Login', command=login)
        start_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        register_button = ctk.CTkButton(
            self, text=f'Register', command=register)
        register_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        def on_closing():
            print("Window is closing.")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_closing)


class Register_Page(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Register')
        self.geometry('500x400')
        self.resizable(False, False)
        self.iconbitmap(f'{icon}')

        def register():
            username = username_entry.get()
            password = password_entry.get()
            confirmpassword = confirmpassword_entry.get()

            if not username or not password or not confirmpassword:
                messagebox.showerror('FlukkieZ System', 'กรุณากรอกให้ครบ')
                return

            if password != confirmpassword:
                messagebox.showerror('FlukkieZ System', 'รหัสผ่านไม่ตรงกัน')
                return
            else:
                if collection.find_one({"username": username}):
                    messagebox.showerror("Error", "Username already exists.")
                else:
                    collection.insert_one(
                        {"username": username, "password": password})
                    messagebox.showinfo("Success", "Registration successful!")

        def login():

            self.destroy()
            main = Login_Page()
            main.mainloop()

        user_label = ctk.CTkLabel(self, text=f'Username : ')
        password_label = ctk.CTkLabel(self, text=f'Password : ')
        confirmpassword_label = ctk.CTkLabel(self, text=f'Confirm Password : ')
        username_entry = ctk.CTkEntry(self)
        password_entry = ctk.CTkEntry(self, show='*')
        confirmpassword_entry = ctk.CTkEntry(self, show='*')
        user_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
        username_entry.place(relx=0.5, rely=0.22, anchor=tkinter.CENTER)
        password_label.place(relx=0.5, rely=0.29, anchor=tkinter.CENTER)
        password_entry.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)
        confirmpassword_label.place(relx=0.5, rely=0.43, anchor=tkinter.CENTER)
        confirmpassword_entry.place(relx=0.5, rely=0.50, anchor=tkinter.CENTER)

        back_button = ctk.CTkButton(self, text=f'Register', command=register)
        back_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        start_button = ctk.CTkButton(self, text=f'Login', command=login)
        start_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def on_closing():
            print("Window is closing.")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_closing)


class Hompage(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title(f'Homepage')
        self.geometry(f'700x600')
        self.iconbitmap(f'{icon}')
        self.resizable(False, False)
        # NAVBAR
        frame2 = ctk.CTkFrame(master=self, width=200)
        frame2.pack(pady=5,
                    padx=5,
                    side='right',
                    expand=True,
                    fill='both'
                    )
        # Homepage

        homepage_frame = ctk.CTkFrame(master=self, width=500)
        homepage_frame.pack(pady=5,
                            padx=5,
                            side='right',
                            expand=True,
                            fill='both'
                            )
        
        Name = ctk.CTkLabel(homepage_frame, text=f'''
                            Name : Wittawin Chadasin\n
                            Age : 18 | Birthday : 18/09/2005\n
                            KKW : 6/3
                            ''', font=('Sarabun',18))
        Name.place(relx=0.35, rely=0.6, anchor=tkinter.CENTER)
        def project_page_func():
           
            self.destroy()
            messagebox.showinfo('flukkiez', f'กำลังโหลดข้อมูล')
            project_page = Project(username)
            project_page.mainloop()

        def homepage_func():
            messagebox.showinfo(f'flukkiez', f'อยู่หน้า Homepage แล้ว')

        welcome_label = ctk.CTkLabel(frame2, text=f'Name : {username}')
        homepage_button = ctk.CTkButton(
            frame2, text=f'HOMEPAGE', command=homepage_func)
        project_page = ctk.CTkButton(
            frame2, text=f'PROJECT', command=project_page_func)

        my_image_label = ctk.CTkLabel(
            homepage_frame, text=f'FlukKieZ', font=('Sarabun', 30))
        my_image_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

        welcome_label.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)
        homepage_button.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        project_page.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        response = requests.get(
            'https://media.discordapp.net/attachments/1042762590411038791/1170215906119532544/skill.jpg')
        image_data1 = response.content
        open_image1 = Image.open(BytesIO(image_data1))

        skill_image = ctk.CTkImage(dark_image=open_image1, size=(300, 200))
        skill_label = ctk.CTkLabel(
            homepage_frame, text=f'My Skill', font=('Sarabun', 20))
        skill_image_label = ctk.CTkLabel(
            homepage_frame, image=skill_image, text=f'')
        skill_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        skill_image_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        my_image_label = ctk.CTkLabel(
            homepage_frame, text=f'FlukKieZ', font=('Sarabun', 30))
        my_image_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

        def on_closing():
            print("Window is closing.")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_closing)


class Project(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title(f'Homepage')
        self.geometry(f'700x600')
        self.resizable(False, False)
        self.iconbitmap(f'{icon}')
        # NAVBAR
        frame2 = ctk.CTkFrame(master=self, width=200)
        frame2.pack(pady=5,
                    padx=5,
                    side='right',
                    expand=True,
                    fill='both'
                    )
        # Homepage

        # project_frame = ctk.CTkFrame(master=self, width=500)
        scrollbar = ctk.CTkScrollableFrame(
            master=self, width=500, corner_radius=5)

        scrollbar.pack(pady=5,
                       padx=5,
                       side='right',
                       expand=True,
                       fill='both'
                       )

        def homepage_func():
            self.destroy()
            home = Hompage(username)
            home.mainloop()

        def project_page_func():
            messagebox.showinfo(f'flukkiez', f'อยู่หน้า Project แล้ว')

        welcome_label = ctk.CTkLabel(frame2, text=f'Name : {username}')
        homepage_button = ctk.CTkButton(
            frame2, text=f'HOMEPAGE', command=homepage_func)
        project_page = ctk.CTkButton(
            frame2, text=f'PROJECT', command=project_page_func)

        my_image_label = ctk.CTkLabel(
            scrollbar, text=f'FlukKieZ', font=('Sarabun', 30))
        my_image_label.pack(anchor=tkinter.CENTER)

        welcome_label.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)
        homepage_button.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        project_page.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
        img_link = collection_project.find()

        for document in img_link:
            if 'name' in document and 'link' in document:
                label_gap = 20
                label_gap2 = 5
                response = requests.get(document['link'])
                label_text = ctk.CTkLabel(
                    master=scrollbar, text=f'{document["name"]}', font=('Sarabun', 20))

                image_data = response.content
                img = Image.open(BytesIO(image_data))
                img = img.resize((400, 200))
                img = ImageTk.PhotoImage(img)

                label = ctk.CTkLabel(
                    scrollbar, image=img, text=f'')
                label.image = img  # Keep a reference to prevent garbage collection
                label_text.pack(padx=label_gap2, pady=label_gap2)
                label.pack(padx=label_gap, pady=label_gap-10)

        def on_closing():
            print("Window is closing.")
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", on_closing)



main = Main()
main.mainloop()
