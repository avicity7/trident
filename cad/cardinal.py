from tkinter import ttk
import tkinter.messagebox
import requests
from dotenv import load_dotenv
load_dotenv() 
import os 
import sv_ttk

backend_uri = os.environ["BACKEND_URI"]

def ClearFrame():
  for w in frame.winfo_children():
    w.destroy()
  
def LinkDevice(username, cad_id):
  o = {"username": username, "cad_id": cad_id}
  r = requests.post(f'{backend_uri}/cad/link-device', json=o)
  r = r.json()
  if r['response'] == "OK":
    DisplayMagician(username, cad_id)

def DisplayHistory(username):
  o = {"username": username}
  r = requests.post(f'{backend_uri}/cad/link-device', json=o)
  r = r.json()
  
  

def DisplayMagician(username, r):
  ClearFrame()
  cad_id = tkinter.StringVar()
  ttk.Label(frame, text=f'Welcome {username}!').grid(row=0, pady=20)
  if r == "OK":
    ttk.Label(frame, text='CAD ID').grid(row=1)
    ttk.Entry(frame, textvariable=cad_id).grid(row=1, column=1)
    ttk.Button(frame, text="Link CAD", command=lambda:LinkDevice(username, cad_id.get())).grid(row=2, column=1, pady=20)
  else:
    ttk.Label(frame, text=f"CAD_ID: {r}").grid(row=1)

def Signup(username, password):
  o = {"username": username, "password": password}
  r = requests.post(f'{backend_uri}/magician/create-magician', json=o)
  r = r.json()
  if r['response'] == "OK":
    DisplayMagician(username, r['response'])
  else:
    tkinter.messagebox.showwarning(title="Failure", message="Existing username!")

def Login(username, password):
  o = {"username": username, "password": password}
  r = requests.post(f'{backend_uri}/magician/login', json=o)
  r = r.json()
  if r['response'] != "WRONG PASSWORD":
    DisplayMagician(username, r['response'])
  else:
    tkinter.messagebox.showwarning(title="Failure", message="Wrong username or password!")

def DisplayLogin():
  ClearFrame()
  username = tkinter.StringVar()
  password = tkinter.StringVar()
  ttk.Label(frame, text='Username').grid(row=0)
  ttk.Entry(frame, textvariable=username).grid(row=0, column=1)
  ttk.Label(frame, text='Password').grid(row=1)
  ttk.Entry(frame, textvariable=password).grid(row=1, column=1)

  ttk.Button(frame, text='Signup', command=lambda: Signup(username.get(), password.get())).grid(row=2, column=0, pady=20)
  ttk.Button(frame, text='Login', command=lambda: Login(username.get(), password.get())).grid(row=2, column=1, pady=20)

root = tkinter.Tk()
root.title("Cardinal")
root.geometry("800x450")
frame = ttk.Frame(root)
frame.pack()
frame.grid(pady=40, padx=40)

DisplayLogin()

sv_ttk.set_theme("dark")
root.mainloop()
