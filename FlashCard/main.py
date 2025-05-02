from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
dict_fr_en={}
CURRENT_CARD={}

try:
    fr_en=pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_fr_en=pd.read_csv("data/french_words.csv")
    dict_fr_en=original_fr_en.to_dict(orient="records")
    print(dict_fr_en)
else:
    dict_fr_en=fr_en.to_dict(orient="records")

def next_card():
    global CURRENT_CARD, flip_timer
    window.after_cancel(flip_timer)  
    CURRENT_CARD=random.choice(dict_fr_en)
    canvas.itemconfig(language_title,text="French",fill="black")
    canvas.itemconfig(card_word, text=CURRENT_CARD["French"],fill="black")
    canvas.itemconfig(card_image, image=front_card)
    flip_timer=window.after(3000,flip_card)

def flip_card():
    canvas.itemconfig(language_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=CURRENT_CARD["English"], fill="white")
    canvas.itemconfig(card_image, image=back_card)

def they_know():
    dict_fr_en.remove(CURRENT_CARD)
    words_to_learn=pd.DataFrame(dict_fr_en) 
    words_to_learn.to_csv("data/words_to_learn.csv",index=False)
    next_card()

window=Tk()
window.title("Flash Card")
window.config(padx=50,pady=50)
window.config(background=BACKGROUND_COLOR)
flip_timer=window.after(3000,flip_card)  

canvas=Canvas(width=800, height=600,bg=BACKGROUND_COLOR, highlightthickness=0,borderwidth=0)
front_card=PhotoImage(file="images/card_front.png")
back_card=PhotoImage(file="images/card_back.png")
card_image=canvas.create_image(400,300, image=front_card)
canvas.grid(column=0,row=1,columnspan=2)

language_title=canvas.create_text(380,150,text="",font=("Garamond", 35,"underline"))
card_word=canvas.create_text(388,290,text="",width=750,justify="left",anchor=CENTER,font=("Gabriola", 90,"bold italic"))

yes_image=PhotoImage(file="images/right.png")
yes_button=Button(image=yes_image,highlightthickness=0,command=they_know)
yes_button.grid(column=1,row=2)

no_image=PhotoImage(file="images/wrong.png")
no_button=Button(image=no_image,command=next_card)
no_button.grid(column=0,row=2)

next_card()

window.mainloop()
