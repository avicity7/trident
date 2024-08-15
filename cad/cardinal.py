from tkinter import *
import tkinter.messagebox
import requests
from dotenv import load_dotenv
load_dotenv() 
import os 

backend_uri = os.environ["BACKEND_URI"]

def ClearFrame():
  for w in frame.winfo_children():
    w.destroy()
  
def LinkDevice(username, cad_id):
  o = {"username": username, "cad_id": cad_id}
  r = requests.post(f'{backend_uri}/cad/link-device', json=o)
  r = r.json()
  

def DisplayMagician(username):
  ClearFrame()
  cad_id = StringVar()
  Label(frame, text=f'Welcome {username}!').grid(row=0)
  Label(frame, text='CAD ID').grid(row=1)
  Entry(frame, textvariable=cad_id).grid(row=1, column=1)
  Button(frame, text="Link CAD", command=lambda:LinkDevice(username, cad_id)).grid(row=2, column=1)

def Signup(username, password):
  o = {"username": username, "password": password}
  r = requests.post(f'{backend_uri}/magician/create-magician', json=o)
  r = r.json()
  if r['response'] == "OK":
    DisplayMagician(username)
  else:
    tkinter.messagebox.showwarning(title="Failure", message="Existing username!")

def Login(username, password):
  o = {"username": username, "password": password}
  r = requests.post(f'{backend_uri}/magician/login', json=o)
  r = r.json()
  if r['response'] == "OK":
    DisplayMagician(username)
  else:
    tkinter.messagebox.showwarning(title="Failure", message="Wrong username or password!")

def DisplayLogin():
  ClearFrame()
  username = StringVar()
  password = StringVar()
  Label(frame, text='Username').grid(row=0)
  Entry(frame, textvariable=username).grid(row=0, column=1)
  Label(frame, text='Password').grid(row=1)
  Entry(frame, textvariable=password).grid(row=1, column=1)

  Button(frame, text='Signup', command=lambda: Signup(username.get(), password.get())).grid(row=2, column=0)
  Button(frame, text='Login', command=lambda: Login(username.get(), password.get())).grid(row=2, column=1)

root = Tk()
root.title("Cardinal")
root.geometry("800x450")
frame = Frame(root)
frame.pack()

DisplayLogin()

root.mainloop()
