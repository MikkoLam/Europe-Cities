# -*- coding: utf-8 -*-
# Europe Cities.py
# Mikko Lampinen, Tampere
# May, 2021
# The program asks Cities of Europe to locate them in the map, by clicking as near the right location
# and as quickly you can.

from tkinter import *
import math
import random
from time import time
import codecs

#           F U N C T I O N S   I N   A L P H A B E T I C A L   O R D E R

def ask_city():
    global have_tried
    global t1
    global index
    global taken
    global latitude
    global longitude
    global total_pts

    if index < 10:                          # asks 10 cities
        ask_btn.config(state=DISABLED)      # cant accidentally ask another city before answered previous one
        city_asked = False                  # false default, if true, city has been asked before
        town = 0
        details = []
        this_town = random.randint(1, 105)
        with codecs.open("eu_cities.csv", "r", "utf8") as townfile:
            for row in townfile:
                if town == this_town:
                    details = row.split(",")    # sets only 1 town details
                town += 1
        for j in range(0, 10):
            if taken[j] == this_town:           # dont ask same city twice
                city_asked = True

        if not city_asked:
            taken[index] = this_town                # marks the town, so it wont be asked again
            header2_txt = str(index+1) + ". " + details[2]
            header2.config(text=header2_txt)
            latitude = float(details[0])
            longitude = float(details[1])
            t1 = time()
            delay = 0
            while delay < 2:
                delay = delta_t()
            have_tried = False
            index += 1
            t1 = time()
        else:
            ask_city()

# AFTER 10 CITIES ASKED DISPLAYS BEST SCORES AND NAMES AND CHECK IF CURRENT SCORE IS TOP 5

    else:
        best = []
        player_name = name.get()
        if len(player_name) > 10:
            player_name = player_name[:10]
        header2_txt = "Top 5 scores! (your score:" + str(total_pts) + ")"
        with codecs.open("best_of_europe.csv", "r", "utf8") as bestfile:
            for row in bestfile:
                best = row.split(";")   # MAKE A LIST OF TOP 5
        for i in range(0, 16, 2):       # best[0] = 1.score, best[1] = 1.name, best[2] = 2.score, best[3] = 2.name, etc.
            best_pts = int(best[i])
            if total_pts > best_pts and total_pts > 0:
                best.insert(i, str(total_pts))      # insert total points into top 5 to index i
                best.insert(i + 1, player_name)     # e.g. 950,Mikko,945,Lotta,930,Liina,etc.
                total_pts = -1                      # points down, so it dont insert points twice,
                                                    # total_points = -1 is also a "sign" to save top 5

# DISPLAY TOP 5
        label1_txt = "1. " + best[0] + (17 - 2*len(best[0])) * " " + best[1]
        label2_txt = "2. " + best[2] + (17 - 2*len(best[2])) * " " + best[3]
        label3_txt = "3. " + best[4] + (17 - 2*len(best[4])) * " " + best[5]
        label4_txt = "4. " + best[6] + (17 - 2*len(best[6])) * " " + best[7]
        label5_txt = "5. " + best[8] + (17 - 2*len(best[8])) * " " + best[9]
        header2.config(text=header2_txt)
        label1.config(text=label1_txt)
        label2.config(text=label2_txt)
        label3.config(text=label3_txt)
        label4.config(text=label4_txt)
        label5.config(text=label5_txt)

# SAVING NEW TOP 5 ????
        if total_pts == -1:         # total points has been in top 5
            txt2save = ""
            for item in best:
                txt2save += item + ";"
            with codecs.open("best_of_europe.csv", "w", "utf8") as writefile:   # write new top 5
                writefile.write(txt2save)
# PREPARE NEW GAME
        taken = [0,0,0,0,0,0,0,0,0,0,0,0]
        index = 0
        total_pts = 0
        new_map()


def canvas_click(event):
    global have_tried
    global label1
    global label3
    global label5
    global total_pts
    ask_btn.config(state=NORMAL)    # can ask new city from now on
    if not have_tried:              # can answer only once
        have_tried = True
        x1 = event.x
        y1 = event.y
        seconds = delta_t()         # MEASURES ANSWERING TIME
        y = convert_y(latitude)
        x = convert_x(latitude, longitude)
        xx = x1 + 10                # xx and yy are for pinpoint line
        yy = y1 - 15
        canvas.create_line(x1, y1, xx, yy)
        canvas.create_oval((xx - 2, yy - 3, xx + 3, yy + 2), fill="blue")   # pinpoints the mouse click
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")          # points the right location with red circle
        lat_click = (height - y1) / pplatitude + min_latitude               # converts y click to latitude
        pplongitude = pplatitude * math.cos(latitude * math.pi / squash_north)       # pixels per longitude (if degrees 180, it squashes too much from north)
        long_click = (x1 - canvas_center) / pplongitude + mid_longitude     # converts x click to longitude
        kmy = (latitude - lat_click) * 10000 / 90                              # distance y and x component
        kmx = (longitude - long_click) * 10000 / 90 * math.cos((latitude+lat_click)/2 * math.pi / 180)
        distance = math.sqrt ((kmy * kmy) + (kmx * kmx))                    # pythagoras
        distance = int(distance)
        s = int(100 * seconds) / 100
        pts = int(150 - distance - int(10 * s))
        if pts < 0:
            pts = 0
        total_pts += pts

# DISPLAYING THE CALCULATION AND POINTS
        label2_txt = "-" + str(distance) + " pts (distance " + str(distance) + " km)    "
        label3_txt = "-" + str(int(10 * s)) + " pts (time " + str(s) + " s)    "
        label5_txt = str(pts) + " pts, total " + str(total_pts) + " pts       "
        label1.config(text="150 pts (max)")
        label2.config(text=label2_txt)
        label3.config(text=label3_txt)
        label4.config(text="________________")
        label5.config(text=label5_txt)


def convert_y(lat):
    return (min_latitude - lat) * pplatitude + height


def convert_x(lat,long):
    pplongitude = pplatitude * math.cos(lat * math.pi / squash_north)  # pixels per longitude
    return (long - mid_longitude) * pplongitude + canvas_center


def delta_t():
    t2 = time()
    dt = t2 - t1
    return dt


def draw(filename):
    points = []
    with open(filename + ".csv", "r") as map_data:
        for row in map_data:
            details = row.split(",")
            if details[0] != "draw":
                latitude = float(details[0])
                longitude = float(details[1])
                y = convert_y(latitude)
                x = convert_x(latitude, longitude)
                points.append(x)
                points.append(y)
            else:                               # if row begins with "draw"
                if details[2] == "polygon":
                    canvas.create_polygon((points), fill=details[1])
                if details[2] == "line":
                    canvas.create_line((points), fill=details[1])
                points.clear()


def new_map():
    canvas.create_rectangle(5, 5, width-5, height-5, fill="cyan")
    draw("europe1")
    draw("islands")
    draw("borders")
    draw("rivers")
    draw("lakes")


# M A I N   P R O G R A M_________________________________________________

root = Tk()
root.title("Europe cities")
width = 1150
height = 800
root.geometry("1580x810")

index = 0
total_pts = 0
taken = [0,0,0,0,0,0,0,0,0,0,0,0,0]
min_latitude = 33   # latitude at canvas bottom
mid_longitude = 16  # longitude 16 east is
canvas_center = 560 # at 560px at canvas
pplatitude = 21     # pixels per one latitude degree
have_tried = True   # cant answer before asked
squash_north = 210  # if 180 degrees (the right value) then squashes north too much. If 250deg, then skandinavia too big

canvas = Canvas(root,width=width, height=height,bg="yellow")
ask_btn = Button(root, text="Ask new city",command=ask_city)
enter_name = Label(root, font=("Helvetica",12),text="Enter your name below:")
name = Entry(root, text="Mikko")
name.insert(0,"Mikko")
header1 = Label(root, font=("Helvetica",22),text="Cities of Europe")
header2 = Label(root, font=("Helvetica",18),text=".")
label1 = Label(root,font=("Helvetica",16),text=".")
label2 = Label(root,font=("Helvetica",16),text=".")
label3 = Label(root,font=("Helvetica",16),text=".")
label4 = Label(root,font=("Helvetica",16),text=".")
label5 = Label(root,font=("Helvetica",16),text=".")

canvas.grid(row=0, column=0, rowspan=18)
ask_btn.grid(row=3, column=0, padx=20, sticky="NW")
enter_name.grid(row=1, column=1, sticky="NW", padx=10, pady=10)
name.grid(row=2,column=1,sticky="NW", padx=10, pady=0)
header1.grid(row=0,column=1,sticky="NW", padx=10, pady=10)
header2.grid(row=3,column=1,sticky="NW", padx=10, pady=10)
label1.grid(row=4,column=1,sticky="NW", padx=10, pady=5)
label2.grid(row=5,column=1,sticky="NW", padx=10, pady=5)
label3.grid(row=6,column=1,sticky="NW", padx=10, pady=5)
label4.grid(row=7,column=1,sticky="NW", padx=10, pady=5)
label5.grid(row=8,column=1,sticky="NW", padx=10, pady=5)

new_map()

canvas.bind("<Button-1>",canvas_click)

root.mainloop()