import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style, ttk
import phonenumbers
from opencage.geocoder import OpenCageGeocode
from phonenumbers import geocoder, carrier
import folium
import pygame
import os
import webbrowser
from PIL import Image, ImageTk, ImageSequence
API_KEY = "a52c52f596aa4a9599c5f5e8569b0ffa"
geocoders = OpenCageGeocode(API_KEY)
RESULTED = "C:/result/"
try:
    init = pygame.mixer
    load = pygame.mixer.music
    play = load
    init.init()
    load.load("./pnlp/ext/bg.mp3")
    play.play(-1)
except:
    print("Error")
if not os.path.exists(RESULTED):
    os.makedirs(RESULTED)
def play_notification_sound_success():
    nss = pygame.mixer.Sound("./pnlp/ext/notification.mp3")
    nss.play()
def play_notification_sound_falid():
    nsf = pygame.mixer.Sound("./pnlp/ext/error.mp3")
    nsf.play()
def locate_number():
    number = phone_entry.get()
    try:
        check_number = phonenumbers.parse(number)
        number_location = geocoder.description_for_number(check_number, "en")
        server_provider = carrier.name_for_number(check_number, "en")
        
        query = str(number_location)
        result = geocoders.geocode(query)
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        
        map_location = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=number_location).add_to(map_location)
        map_path = os.path.join(RESULTED, "result.html")
        map_location.save(map_path)
        
        messagebox.showinfo(f"{play_notification_sound_success()}Info", f"Location: {number_location}\nProvider: {server_provider}\nLatitude: {lat}\nLongitude: {lng}")
        webbrowser.open("C:/result/result.html")
    except Exception as e:
        messagebox.showerror(f"{play_notification_sound_falid()}Error", f"An error occurred: {e}")
def reset_fields():
    try:
        phone_entry.delete(0, tk.END)
        os.remove("C:/result/result.html")
        
    except:
        print("error")
        init.init()
        load.load("./pnlp/ext/bg.mp3")
        play.play(-1)
def update_frame(frame_number):
    frame = frames[frame_number]
    frame_number = (frame_number + 1) % len(frames)
    background_label.config(image=frame)
    app.after(100, update_frame, frame_number)
def on_click_locate(event):
    init.init()
    load.load("./pnlp/ext/locate.mp3")
    play.play()
    locate_number()
    init.init()
    load.load("./pnlp/ext/bg.mp3")
    play.play(-1)
    
def on_click_reset(event):
    init.init()
    load.load("./pnlp/ext/delete.mp3")
    play.play()
    reset_fields()
    init.init()
    load.load("./pnlp/ext/bg.mp3")
    play.play(-1)
app = tk.Tk()
app.title("Phone Number Locator SAZOM")
app.geometry("382x397")
app.resizable(False,False)
style = Style(theme="cosmo")
gif_path = "./pnlp/ext/bg.gif"
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

background_label = tk.Label(app)
background_label.place(relwidth=1, relheight=1)

frame = ttk.Frame(app, padding="10")
frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = ttk.Label(frame, text="Phone Number Locator", font=("Helvetica", 16))
title_label.pack(pady=10)

phone_label = ttk.Label(frame, text="Enter Phone Number:")
phone_label.pack(pady=5)

phone_entry = ttk.Entry(frame, width=30)
phone_entry.pack(pady=5)
phone_entry.bind("<Return>",on_click_locate)
phone_entry.bind("<Delete>",on_click_reset)

button_frame = ttk.Frame(frame, padding="10")
button_frame.pack(pady=10)

locate_button = ttk.Button(button_frame, text="Locate", style="success.TButton", command=locate_number)
locate_button.pack(side="left", padx=5)
reset_button = ttk.Button(button_frame, text="Reset", style="danger.TButton", command=reset_fields)
reset_button.pack(side="left", padx=5)

app.after(0, update_frame, 0)
app.mainloop()
