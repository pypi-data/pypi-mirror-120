import requests
from tkinter import *     
from PIL import Image, ImageTk 
import os
import subprocess
from subprocess import check_output
from subprocess import Popen, PIPE
from threading import Thread
def cape(username):
    try:
        image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

        view = image['frontImageUrl']
        with open('pic1.png', 'wb') as handle:
            response = requests.get(view + ".png", stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        viewimageonscreen()
    except:
        print(f"no cape found on player {username}")
def dowloadcape(username, file_pach: None):
    try:
        str(file_pach)
        str(username)
        if(file_pach == None):
            print("no file pach")
            exit()
        if("." in file_pach):
            print("file pach only. no files like /coolcape.png")
            exit()
        else:
            
            image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

            view = image['frontImageUrl']
            if(str(file_pach).endswith("/") == False):
                file_pach = str(file_pach) + "/"
            with open(f'{file_pach}cape.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        print(f"saved in '{file_pach}cape.png'")
    except:
        print(f"no cape found on player {username}")


def dowloadfullcape(username, file_pach: None):
    try:
        str(file_pach)
        str(username)
        if(file_pach == None):
            print("no file pach")
            exit()
        if("." in file_pach):
            print("file pach only. no files like /coolcape.png")
            exit()
        else:
            
            image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

            view = image['imageUrl']
            if(str(file_pach).endswith("/") == False):
                file_pach = str(file_pach) + "/"
            with open(f'{file_pach}full_cape.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        print(f"saved in '{file_pach}full_cape.png'")
    except:
        print(f"no cape found on player {username}")



 
# # Opens a image in RGB mode
# im = Image.open("pic1.png")
 
# # Size of the image in pixels (size of original image)
# # (This is not mandatory)
# width, height = im.size
 
# # Setting the points for cropped image
# left = 5
# top = height / 4
# right = 164
# bottom = 3 * height / 4
 
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))




# #Import the required Libraries

# #Create an instance of tkinter frame
# win = Tk()

# #Set the geometry of tkinter frame
# win.geometry("194x290")

# #Create a canvas
# canvas= Canvas(win, width= 200, height= 279)
# canvas.pack()

# #Load an image in the script
# img= (Image.open("pic1.png"))

# #Resize the Image using resize method
# resized_image= img.resize((174,278), Image.ANTIALIAS)
# new_image= ImageTk.PhotoImage(resized_image)

# #Add image to the Canvas Items
# canvas.create_image(10,1, anchor=NW, image=new_image)

#win.mainloop()
def sing():
    # Opens a image in RGB mode
    im = Image.open("pic1.png")
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    
    # Setting the points for cropped image
    left = 5
    top = height / 4
    right = 164
    bottom = 3 * height / 4
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))




    #Import the required Libraries

    #Create an instance of tkinter frame
    win = Tk()

    #Set the geometry of tkinter frame
    win.geometry("194x290")

    #Create a canvas
    canvas= Canvas(win, width= 200, height= 279)
    canvas.pack()

    #Load an image in the script
    img= (Image.open("pic1.png"))

    #Resize the Image using resize method
    resized_image= img.resize((174,278), Image.ANTIALIAS)
    new_image= ImageTk.PhotoImage(resized_image)

    #Add image to the Canvas Items
    canvas.create_image(10,1, anchor=NW, image=new_image)
    win.mainloop()
    os.remove("pic1.png")


def viewimageonscreen():
    thread = Thread(target=sing)
    thread.start()