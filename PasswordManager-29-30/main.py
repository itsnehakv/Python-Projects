from tkinter import *
from tkinter import messagebox #it is not a class, its a module within tkinter
import random
import json  #'''JSON is easy to search through.'''
import pyperclip   #not a built in module

NAVYBLUE= "#2B2A4C"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_list = []

    password_list+=[random.choice(letters) for letter in range(random.randint(3, 4))]
    password_list+=[random.choice(numbers) for number in range(random.randint(2, 4))]
    password_list+=[random.choice(symbols) for symbol in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password ="".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)      #automatically copies to clipboard



# ---------------------------- SAVE PASSWORD ------------------------------- #
def press_add():
    website_name = website_entry.get().title()
    email_name = email_entry.get()
    password_name = password_entry.get()

    information_dict={website_name:{
        "email":email_name,
        "password":password_name,
    }}

#***8**-------what i did-----------------**-
    # list_information=[]
    # website_information=[website_name,email_name,password_name]
    # list_information.extend(website_information)
    #    with open("my_passwords.txt","a") as my_passwords:
    #     my_passwords.write( " | ".join(list_information))
    #     my_passwords.write("\n")

    if len(password_name)==0 or len(email_name)==0 or len(website_name)==0:
        messagebox.showinfo(title="Error", message="Please do no leave any fields empty")
    else:
        is_ok=messagebox.askokcancel(title=f"{website_name}",message=f"Email/Username:{email_name}\nPassword:{password_name}\nIs it OK to save?")
        #returns boolean
        if is_ok:
            try:
                with open("my_passwords.json","r") as my_passwords:
                    #Reading old data
                    contents = json.load(my_passwords)  #.read() of json
            except FileNotFoundError:
                with open("my_passwords.json","w") as my_passwords:
                    json.dump(information_dict, my_passwords,indent=2)
            else:
                #Updating old information with new info
                contents.update(information_dict)  # updates json file contents....contents from line 61

                with open("my_passwords.json", "w") as my_passwords:
                    #Saving updated/new info
                    json.dump(contents, my_passwords, indent=2)  #.write() of json. Must be in dict format
                ''' json.dump(obj, file_where_object_is_to_be_dumped)'''
            finally:
                website_entry.delete(0,END)
                password_entry.delete(0,END )

#------------------------------SEARCH PASSWORD-------------------------#
def search_pass():
    website_name=website_entry.get().title()
    try:
        with open("my_passwords.json","r") as my_passwords:
            contents=json.load(my_passwords)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file is found")
    else:
        try:
            messagebox.showinfo(title=f"Information of {website_name}", message=f"Email:{contents[website_name]["email"]}\nPassword:{contents[website_name]["password"]}")
        except KeyError:
            messagebox.showinfo(title="Not found", message="No data was found")

        '''preferably an if-else must be used ^ 
        if website_name in contents:
        .........'''

# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=20,pady=50)
window.config(background=NAVYBLUE)

canvas=Canvas(width=300, height=300)
lock=PhotoImage(file="logo.png")
canvas.create_image(150,150,image=lock)
canvas.grid(column=1,row=0)
canvas.config(bg=NAVYBLUE, highlightthickness=0)

#----WEBSITE----
website=Label(text="Website:", font=("Tahoma",15), bg=NAVYBLUE)
website.grid(column=0,row=1)
website.config(padx=5,pady=5)

website_entry=Entry(width=47)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2,sticky="w")
#---SEARCH----
search_button=Button(text="Search", bg="grey",command=search_pass)
search_button.grid(column=2,row=1, sticky="ew")
#---EMAIL------
email=Label(text="Email/Username:", font=("Tahoma", 15), bg=NAVYBLUE)
email.grid(column=0, row=2)
email.config(padx=10, pady=5)

email_entry=Entry(width=25)
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
email_entry.insert(0, "neha@gmail.com")  #prepopulates the entry
#-----PASSWORD--------
password=Label(text="Password:", font=("Tahoma",15), bg=NAVYBLUE)
password.grid(column=0,row=3)
password.config(padx=10,pady=5)

password_entry=Entry(width=47)
password_entry.grid(column=1,row=3,sticky="w")
#-----GENERATE----
generate_button=Button(text="Generate Password",bg="grey",command=generate_password)
generate_button.grid(column=2,row=3,sticky="ew")
#------ADD-----
add_button=Button(text="Add",width=25,bg="grey",command=press_add)
add_button.grid(column=1,row=4,columnspan=2,sticky="ew")


window.mainloop()