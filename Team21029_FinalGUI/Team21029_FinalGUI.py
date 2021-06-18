import tkinter as tk #import each of these dependencies as seen in the User Manual
import os # some are inherent to basic Python libraries, others need to be imported
import subprocess #
import sys #
from tkinter import BOTH, PhotoImage, filedialog #
from tkinter.ttk import Frame, Button, Label, Style #
from PIL import Image, ImageTk #
from tkinter import * #
from threading import Thread #
from threading import Event #
from svgwrite.extensions import Inkscape #
import time #
import datetime #
import threading #
import csv #
import svgwrite #
import webbrowser #
import pygetwindow #
from pyglet import font #

#font.add_file('C:/Users/Ryan/Desktop/ryanfont.otf') used for testing, can remove

threadCheck = [] #declarations for global variables
threadCheckFont = [] #declarations for global variables
class Example(Frame): #beginning of class for the GUI frame and setup

    def __init__(self): #initialiazation
        super().__init__()
        self.initUI()

    def open_ink(self): #Function for opening Inkscape
        self.clear_order1() #reinitializes GUI
        inkplace = r'C:\Program Files\Inkscape\bin\inkscape.exe' #CHANGE: Path for where Inkscape is on computer
        if (len(threadCheck) > 0): #Checks to see if an Inkscape thread has been opened already in the GUI
            threadCheck[0].join() #Joins the current thread of Inkscape
            try: #If minimized, Inkscape is restored and moved back to original postion
                if (self.win.isMinimized):
                    self.win.restore()
                self.win.activate()
                self.win.moveTo(119,31) #if Inkscape dimensions need to be changed, you can change them here
            except:
                self.ink_thread(inkplace)
        else: #opens Inkscape if thread doesn't exist
            self.ink_thread(inkplace)

    def ink_thread(self, inkplace): #Inkscape opens into a new thread in the background
        self.inkthread = threading.Thread(target=lambda: os.system('"%s"' % inkplace)) #Starts thread
        threadCheck.append(self.inkthread) #Adds thread to array
        self.inkthread.start() #Starts thread/opens inkscape
        time.sleep(6) #Waits 6 seconds for Inkscape to open, allowing the GUI to recognize window names
        self.win = pygetwindow.getWindowsWithTitle('New document 1 - Inkscape')[0] #CHANGE: Initial window name for when Inkscape is opened, can be changed to whatever it is on your computer. Allows for window manipulation with unminimizing and resizing into window area
        self.win.size = (1800, 1010) #Resize window
        self.win.moveTo(119,31) #Moves window
        win2 = pygetwindow.getWindowsWithTitle('C:\WINDOWS\system32\cmd.exe')[0] #When os.system is used to open these programs, another black terminal window is opened first, we use this to close it automatically. If the window is a different name on your end, change it here.
        win2.close() #Closes window above

    def font_thread(self, fontplace): #Nealry identical to ink_thread function above but for FontCreator, reference comments above
        self.fontthread = threading.Thread(target=lambda: os.system('"%s"' % fontplace))
        threadCheckFont.append(self.fontthread)
        self.fontthread.start()
        time.sleep(6)
        self.fontWin = pygetwindow.getWindowsWithTitle('FontCreator 13.0 (UNREGISTERED)')[0]
        self.fontWin.size = (1800, 1010)
        self.fontWin.moveTo(119,31)
        win2 = pygetwindow.getWindowsWithTitle('C:\WINDOWS\system32\cmd.exe')[0]
        win2.close()

    def open_font(self): #Identical to open_ink above but for FontCreator, reference those comments
        self.clear_order1()
        fontplace = r'C:\Program Files\High-Logic FontCreator\FontCreator.exe';
        if (len(threadCheckFont) > 0):
            threadCheckFont[0].join()
            try:
                if (self.fontWin.isMinimized):
                    self.fontWin.restore()
                self.fontWin.activate()
                self.fontWin.moveTo(119,31)
            except:
                self.font_thread(fontplace)
        else:
            self.font_thread(fontplace)


    def choose_create(self): #Function used to open and load screen on GUI for Create/Send Orders
        self.clear_order1() #reinitializes GUI
        makeCSV = tk.Button(self, text="Create New CSV File", compound="top", anchor='center', command = lambda: self.remove_button1(makeCSV, loadCSV, sendSVG), bg = "light blue") #Create new CSV button, when clicked a function that removes the buttons first runs, then the CSV creation screen loads
        makeCSV.config(height=8, width=40) #Dimensions of buttons
        makeCSV.rowconfigure(0, weight=1) #Row configuration
        makeCSV.grid(row=0, column = 3, columnspan = 2, rowspan = 2) #Place on GUI grid on screen
        loadCSV = tk.Button(self, text="Load CSV File", compound="top", anchor='center', command = lambda: self.remove_button2(makeCSV, loadCSV, sendSVG), bg = "light blue") #Load CSV file, when clicked buttons are removed and the load CSV screen appears
        loadCSV.config(height=8, width=40)
        loadCSV.rowconfigure(0, weight=1)
        loadCSV.grid(row=1, column = 3, columnspan = 2, rowspan = 2)
        sendSVG = tk.Button(self, text="Send SVG File", compound="top", anchor='center', command = lambda: self.remove_button3(makeCSV, loadCSV, sendSVG), bg = "light blue") #Send SVG file to robot, when clicked buttons are removed and you are taken to the SVG sending screen
        sendSVG.config(height=8, width=40)
        sendSVG.rowconfigure(0, weight=1)
        sendSVG.grid(row=2, column = 3, columnspan = 2, rowspan = 2)

    def create_order(self): #Function to load the Create CSV screen
        self.labelText=StringVar()
        self.labelText.set("Enter the comma-seperated rows.\nExample:\n'''John Doe, Tucson, 123-456-7890\nJane Doe, Tucson, 123-456-7890'''") #Header label with instructions
        self.labelDir=Label(self, textvariable=self.labelText, height=4, bg = "light blue") #
        self.labelDir.grid(row=0,column=3, columnspan=1, rowspan = 2)#
        self.name = Text(self, height=1, width=10)#Text to type file name
        self.labelTextFile=StringVar()
        self.labelTextFile.set("Enter file name:") #File name label
        self.labelFile=Label(self, textvariable=self.labelTextFile, height=1, bg = "light blue") #
        self.T = Text(self, height=20, width=80) #Text where to type file contents
        self.labelFile.grid(column = 2, row = 0, columnspan = 2, rowspan = 1)
        self.name.grid(column = 3, row = 0, columnspan = 2, rowspan = 1)
        self.T.grid(column = 3, row = 1, columnspan = 1, rowspan = 2)
        self.b = Button(self, text='Submit', command=self.writeToFile, bg = "light blue") #Submit button, when pressed the GUI creates the file with the specified name and contents
        self.b.grid(column= 2, row = 2, columnspan = 3, rowspan=3)
        self.b.config(height = 3, width = 20)

    def svgship(self): #Function for when send SVG is clicked
        self.sendSVGname = filedialog.askopenfilename(initialdir="C:/Users/ewink/appdata/roaming/spb_data/mu_code", title="SVG File", filetypes = (("svg files", "*.svg"), ("all files", "*.*"))) #CHANGE: Opens file dialog looking for SVG files, would change this to wherever you send the created SVG files on your device
        self.labelTextIP=StringVar()
        self.labelTextIP.set("Enter IP address:") #IP address label
        self.labelDirIP=Label(self, textvariable=self.labelTextIP, height=4, bg = "light blue")
        self.labelDirIP.grid(row=1,column=2, columnspan=3, rowspan = 1)
        self.nameIP = Text(self, height=1, width=10) #Text space to enter file name
        self.nameIP.grid(row=1,column=3, columnspan=3, rowspan = 1)
        self.but = Button(self, text='Submit', command=self.send_final, bg = "light blue") #Submit button, sends to function that sends the SVG to the robot on the same network with that IP address
        self.but.grid(column= 3, row = 1, columnspan = 2, rowspan=2)
        self.but.config(height = 3, width = 20)

    def statusCheck(self, IPname): #Function that, after extablishing connection with robot, recieves JSON array with necessary error and device information
        confirmation = False #value where computer stops looking for updates
        while (confirmation == False):
            subprocess.run(["scp", "pi@" + IPname + ":~/status/status.JSON", "confirm.JSON"]) #Recieves JSON file from robot
            confirmJSON = open("confirm.JSON", "r") #Opens and copies info from JSON array
            arrayJSON = json.load(confirmJSON)
            print(arrayJSON['current_status'] + " " + str(arrayJSON['last_updated'])) #Currently prints JSON array to console, can be used for error notifications
            if (arrayJSON['current_status'] == "complete"): #When robot sends to GUI that order is done, thread stops looking
                confirmation = True
            confirmJSON.close()
            time.sleep(5) #Checks every 5 seconds
        #show comfirmation notification on this line

    def send_final(self): #Function that sends the chosen SVG to the inserted IP address
        subprocess.run(["scp", self.sendSVGname, "pi@" + self.nameIP.get("1.0",'end-1c') + ":~/print-files/print.svg"]) #Subprocess send ssh connection to robot
        textIP = open("hostIP.txt", "w") #Opens hostIP text file
        myIP = textIP.write(socket.gethostbyname(socket.getfqdn())); #Recieves current IP address of computer sending the IP address for robot to use
        textIP.close() #Closes text file
        subprocess.run(["scp", "hostIP.txt", "pi@" + self.nameIP.get("1.0",'end-1c') + ":~/config/hostIP.txt"]) #Sends IP address to robot
        dummy = self.nameIP.get("1.0",'end-1c') #Makes dummy variable with robot IP
        self.clear_order1() #Reinitializes GUI
        self.statusThread = threading.Thread(target=self.statusCheck, args=(dummy,)) #Starts status check thread for recieving notification JSON array from robot
        self.statusThread.start()

    def mail_merge(self): #Used to initilize button to open CSV file for SVG creation
        self.my_btn = Button(self, text="Open File", command=self.open_file, borderwidth = 0)
        img2 = PhotoImage(file="choosefilebutton.png").subsample(1,1)
        img2.image = img2
        self.my_btn.config(image=img2)
        self.my_btn.grid(row = 0, column = 3, columnspan = 2)

    def open_file(self): #Opens CSV file for SVG creation
        self.filename = filedialog.askopenfilename(initialdir="C:/Users/ewink/appdata/roaming/spb_data/mu_code", title="Select A CSV", filetypes = (("csv files", "*.csv"), ("all files", "*.*"))) #CHANGE: Starts file dialog for CSV files, please change intialdir to path where you save your CSV files
        self.clear_order1()
        self.variable_use()

    def open_fontfile(self): #Looks for custom OTF font file
        self.fontfilename = filedialog.askopenfilename(initialdir="C:/Users/ewink/Desktop", title="Select A Font File", filetypes = (("otf files", "*.otf"), ("all files", "*.*"))) #CHANGE: Starts file dialog for OTF files, please change intialdir to path where you save your OTF font files
        self.clear_order1() #Reinitializes GUI
        self.create_svg() #Function to create SVG file

    def variable_use(self): #Function that initilizes Load CSV screen where SVG is created
        self.open_csv = open(self.filename, 'r') #Opens specified CSV files
        self.reader = csv.reader(self.open_csv) #Reads and copies CSV
        list = [] #Creates 2D list for CSV headers and values
        for row in self.reader:
            test = []
            for col in row:
                if col != "":
                    test.append(col)
            list.append(test)
        self.open_csv.close()
        newString = "To use header items, insert the appropriate variable -> | " #Instructions start
        for i in range(len(list[0])): #Inserts variable header names based on how many headers there are
            if list[0][i] != "":
                newString += list[0][i] + ' = var' + str(i) + " | "
        self.come_together(newString, list) #Function that brings this information and puts it on screen

    def come_together(self, header, csvfile): #Function loads screen for SVG file creation
        self.clear_order1() #Reinitializes screen
        self.labelText1=StringVar()
        self.labelText1.set(header + '\n\nUse "%n" to go to next line (ONLY ONE WORKS RIGHT NOW)')
        #self.labelTextInd=StringVar()
        #self.labelTextInd.set('\nUse "%n" for an indent (ONLY ONE INDENT WORKS RIGHT NOW)')
        #self.labelTextInd1 = Label(self, textvariable=self.labelTextInd, height=1, bg = "light blue")
        #self.labelTextInd1.grid(row=0, rowspan=2, column=2, columnspan=3)
        self.svglabeltext=StringVar()
        self.svglabeltext.set("Enter desired svg file name:") #SVG file name label
        self.svglabel = Label(self, textvariable=self.svglabeltext, height=1, bg = "light blue")
        self.svgname = Text(self, height=1, width=10) #SVG file name text
        self.labelDir1=Label(self, textvariable=self.labelText1, height=5, bg = "light blue") #Loads header contents from last function (variable_use)
        self.labelDir1.grid(row=0,column=2, columnspan=3)
        self.Tl = Text(self, height=20, width=80) #Text box for message
        self.csv = csvfile #Loads csv contents copied before
        self.v = IntVar() #Value for Radio buttons
        self.v.set(1)
        self.layout1 = tk.Radiobutton(self, #Radio button to choose A7 letter layout
               text="A7",
               padx = 10,
               variable=self.v,
               value=1,
               bg="light blue")
        self.layout2  = tk.Radiobutton(self, #Radio button to choose 5x7 lettter layout
               text="5x7",
               padx = 10,
               variable=self.v,
               value=2,
               bg="light blue")
        self.inv = IntVar() #Value for inversion box
        self.inv.set(0)
        self.invert = tk.Checkbutton(self, text = "Invert", variable = self.inv, onvalue = 1, offvalue = 0, bg="light blue") #Checkbox for inverting/uninverting
        self.invert.grid(column = 3,columnspan = 2, row = 2, rowspan = 2) #Layout
        self.layout1.grid(column = 4, columnspan = 1, row = 2, rowspan = 2) #Layout
        self.layout2.grid(column = 4, columnspan = 2, row = 2, rowspan = 2) #Layout
        self.svglabel.grid(column = 2, row = 0, columnspan = 2, rowspan = 2) #Layout
        self.svgname.grid(column = 3, row = 0, columnspan = 2, rowspan = 2) #Layout
        self.Tl.grid(column = 3, row = 1, columnspan = 1, rowspan = 2) #Layout
        self.svgfonttext=StringVar()
        self.svgfonttext.set("Enter font size: ") #FontSize label
        self.svgfont = Label(self, textvariable=self.svgfonttext, height=1, bg = "light blue")
        self.svgfontname = Text(self, height=1, width=3) #FontSize text input
        self.svgfont.grid(row = 2, rowspan = 2, column = 1, columnspan = 3)
        self.svgfontname.grid(row = 2, rowspan = 2, column = 2, columnspan = 2)
        self.svgfontwidtext=StringVar()
        self.svgfontwidtext.set("Enter font width: ") #Font width label
        self.svgfontwidth = Label(self, textvariable=self.svgfontwidtext, height=1, bg = "light blue")
        self.svgfontwid = Text(self, height=1, width=3) #FontSize width input
        self.svgfontwidth.grid(row = 2, rowspan = 2, column = 1, columnspan = 2)
        self.svgfontwid.grid(row = 2, rowspan = 2, column = 2, columnspan = 1)
        self.svgfontwidref=StringVar()
        self.svgfontwidref.set("FOR FONT WIDTH REFERENCE\nFor 14pt sans-serif:\nAbout 52 for A7\nAbout 88 for 5x7") #FontSize reference label
        self.svgfontwidinst = Label(self, textvariable=self.svgfontwidref, height=4, bg = "light blue")
        self.svgfontwidinst.grid(row = 1, rowspan = 3, column = 1, columnspan = 2)
        self.c = Button(self, text='Select Font File', command = self.create_svg,bg = "light blue") #Select Font File/Submit button, loads file dialog for choosing OTF file
        self.c.grid(column = 2, row = 3, columnspan = 3, rowspan=3)
        self.c.config(height = 3, width = 20)

    def create_svg(self): #This function is easily our most robust. It focuses on the format/creation of the SVG file
        self.fontfilename = filedialog.askopenfilename(initialdir="C:/Users/ewink/Desktop", title="Select A Font File", filetypes = (("otf files", "*.otf"), ("all files", "*.*")))#CHANGE: start file dialog, change initialdir to where you saved your font files files
        text = self.Tl.get("1.0",'end-1c').split()
        csvfile = self.csv#brings over saved CSV contents
        docuSize = None #Variable for document size based on radio buttons
        if self.v.get() == 1: #A7 selection settings
            docuSize = ('4.125in','2.9375in')
            width = -396
            height = -282
        if self.v.get() == 2: #5x7 selection settings
            docuSize = ('7in', '5in')
            width = -672
            height = -480
        dwg = svgwrite.Drawing(self.svgname.get("1.0",'end-1c') + ".svg", profile='full', size = docuSize) #Initialize empty SVG drawing file
        ink_layer = Inkscape(dwg) #Creates a layered SVG with Inkscape API
        for i in range(len(csvfile)): #For each row in the CSV file
            textCopy = text[:] #Array of words in the text field typed before
            example = None #Empty string for final string of words
            if i == 0:
                continue
            if len(csvfile[i]) != 0: #This statement focuses on replacing all {varX} with their appropriate values
                for j in range(len(textCopy)):
                    if '{var' in textCopy[j]: #If the {var beginning of a word is found
                        if len(textCopy[j]) <= 6: #If the {varX} has no characters after it
                            textCopy[j] = str(csvfile[i][int(textCopy[j][4])]) #Replace
                            textCopy[j] = textCopy[j].strip() #Add
                            example = ' '.join(textCopy) #
                        elif len(textCopy[j]) >= 7: #If the {varX} has characters after it, such as commas or %n
                            textCopy[j] = str(csvfile[i][int(textCopy[j][4])]) + str(textCopy[j][6:]) #Replace
                            textCopy[j] = textCopy[j].strip() #Add
                            example = ' '.join(textCopy) #
                    else: #If there are no variables found in the message
                        example = ' '.join(textCopy) #Add
                dwg.embed_font(name=self.fontfilename.split("/")[-1][:-4], filename=self.fontfilename) #This loads in the selected font name
                dwg.embed_stylesheet("""
                    .flower14 {
                        font-family: """ + self.fontfilename.split("/")[-1][:-4] + """;
                        font-size: """ + self.svgfontname.get("1.0",'end-1c') + """;
                    }
                    """)#Creates a CSS stylesheet that is recogized by the SVG and is used by adding a new font-family and font-size
                if (i == 1): #For first layer only
                    layer = ink_layer.layer(label=str(i), locked=False) #creates a layer in the drawing
                else: #After first layer
                    layer = ink_layer.layer(label="!" + str(i), locked=False) #creates a layer in the drawing with the ! point for robot team
                dwg.add(layer) #Add layer
                paragraph = layer.add(dwg.g(class_="flower14",)) #Add css stylesheet to layer
                lengthCounter = 0 #Initilize counter for length of message written so far
                j = 0 #Initilize loop variable for font width
                stringToAdd = "" #Initilize temporary string variable to add the complete message
                linecounter = 1 #Initilize counter for lines of text in SVG
                lastspace = None #Initilize variable for last space found in text
                babystring = "" #Initilize temporary string
                indented = 0 #Initilize variable for whether to line break or not
                indents = 0 #Initilize number of line breaks
                while lengthCounter+j <= len(example): #This loop focuses on using the font width input and making sure that the lines of text are formatted correctly by breaking up the message character by character to ensure words are intact and there is no overflow
                    if j + lengthCounter == len(example): #If we have reached the end of the message (length of example file)
                        addto = stringToAdd[lengthCounter:len(example)] #Add remainder of string
                        if self.inv.get() == 1: #If inverted, add upsidedown
                            paragraph.add(dwg.text(f'{addto}', insert=(width+10,height +linecounter*20), fill='blue', transform = "rotate(180,0,0)"))
                        else: #Not inverted, insert
                            paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                        #paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                        j+=1 #Increase j value to break loop
                        break
                    if indented == 1: #If the text needs to go to t he next line now
                        if (indents == 0): #Number of line breaks so far, could be used for including more line breaks in the future
                            addto = stringToAdd[lengthCounter:(j+lengthCounter-1)] #Add the string up to this point, minus the "%n"
                            if linecounter == 1: #If on first line
                                babystring = addto
                                stringToAdd = babystring #Add piece of message to final message variable
                            else: #If on second line or after
                                babystring += addto
                                stringToAdd = babystring #Add piece of message to final message variable
                            lengthCounter = lengthCounter+j #Update the length of the message gone through so far
                            if self.inv.get() == 1: #If inverted
                                paragraph.add(dwg.text(f'{addto}', insert=(width+10,height +linecounter*20), fill='blue', transform = "rotate(180,0,0)"))
                            else: #If not inverted
                                paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                            #paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                            j=0 #Reset loop counter
                            linecounter += 1 #increase number of lines
                            indented = 0 #Undo indented variable
                            indents += 1 #Add one to number of indents
                        else: #If this is not the first indents (THIS ELSE STATEMENT DOES NOT CURRENTLY WORK AS INTENDED)
                            addto = stringToAdd[(lengthCounter+1*(indents)):(j+lengthCounter-1*(indents))] #Tried to multiply by the number of indents to stay consistent with the changes
                            if linecounter == 1: #If first line
                                babystring = addto
                                stringToAdd = babystring #Add to big string
                            else: #Not first line
                                babystring += addto
                                stringToAdd = babystring #Add to big string
                            lengthCounter = lengthCounter+j #Update message character counter
                            if self.inv.get() == 1:# if Inverted
                                paragraph.add(dwg.text(f'{addto}', insert=(width+10,height +linecounter*20), fill='blue', transform = "rotate(180,0,0)"))
                            else: #if not Inverted
                                paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                            #paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                            j=0 #Reset loop counter
                            linecounter += 1 #increase number of lines
                            indented = 0 #Undo indented variable
                            indents += 1 #Add one to number of indents
                    if j == int(self.svgfontwid.get("1.0",'end-1c')): #If the end of the current line of text is reached
                        j = 0 #reset loop value
                        addto = stringToAdd[lengthCounter:(lastspace)] #Add text between beginning of line and last open space
                        if linecounter == 1: #If first line
                            babystring = addto
                            stringToAdd = babystring #Add to big string
                        else: #If after first line
                            babystring += addto
                            stringToAdd = babystring #Add to big string
                        lengthCounter = lastspace #Update character counter with where the last space left off
                        if self.inv.get() == 1: #If inverted
                            paragraph.add(dwg.text(f'{addto}', insert=(width+10,height +linecounter*20), fill='blue', transform = "rotate(180,0,0)"))
                        else: #If not inverted
                            paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                        #paragraph.add(dwg.text(f'{addto}', insert= (10, linecounter*20+int(self.svgfontname.get("1.0",'end-1c')) *.65), fill = 'blue'))
                        linecounter += 1 #Add to number of lines of text
                    if j < int(self.svgfontwid.get("1.0",'end-1c')) and j+lengthCounter < len(example): #If the line of text has not reached the limit yet
                        stringToAdd += example[j+lengthCounter]#Add character to line
                        j += 1 #Increment loop value
                        if j+lengthCounter < len(example): #If within the bounds of the message length
                            if example[j+lengthCounter] == " ": #If character is a space
                                lastspace = j+lengthCounter #Save as most recent space added
                            if example[j+lengthCounter] == "n": #If character is an "n"
                                if example[(j+lengthCounter)-1] == "%": #If character before the "n" is a "%"
                                    indented = 1 #Activate need for a line break

        dwg.save() #save ENTIRE drawing as SVG file
        self.clear_order1() #Reinitialize GUI


    def remove_button1(self, button1, button2, button3): #Remove button function for Create CSV
        button1.grid_forget()
        button2.grid_forget()
        button3.grid_forget()
        self.create_order() #Function for page to create CSV

    def remove_button2(self, button4, button5, button6): #Remove button function for Load CSV
        button4.grid_forget()
        button5.grid_forget()
        button6.grid_forget()
        self.mail_merge() #Function to start loading page to create SVG

    def remove_button3(self, button7, button8, button9): #Remove button function for Send SVG
        button7.grid_forget()
        button8.grid_forget()
        button9.grid_forget()
        self.svgship() #Function to start sending SVG to robot


    def clear_order1(self): #Function that destroys and reinitilizes GUI layout (main screen)
        self.destroy()
        self.__init__()

    def writeToFile(self): #Used to create CSV file, saves to where script is saved
        if (self.name.get("1.0",'end-1c') != ""): #If file name isnt empty
            with open(self.name.get("1.0",'end-1c') + ".csv", 'w', newline='') as f:
                w=csv.writer(f, quoting=csv.QUOTE_NONE, escapechar=",")
                w.writerow([self.T.get("1.0",END)])
        self.clear_order1()

    def web(self): #Function to open Calligraphr with button
        webbrowser.open_new("https://www.calligraphr.com/en/")

    def initUI(self): #OVERALL INITIALIZATION OF GUI HOMESCREEN

        self.master.title("Simply Noted") #Window title
        self.pack(fill=BOTH, expand=True)
        self["background"]="Azure2" #Background color

        style = Style() #Stylesheet
        style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '1')

        imageinkscape = PhotoImage(file="inkscape.png").subsample(1,1) #image definitions for left buttons
        imagefontcreator = PhotoImage(file="fontcreator.png").subsample(1,1) # If files are moved, change file value to path where pics are
        imageCreateOrder = PhotoImage(file="envelope.png").subsample(1,1) #
        imageCalligraphr = PhotoImage(file="calligraphr.png").subsample(1,1) #
        imageinkscape.image = imageinkscape #
        imagefontcreator.image = imagefontcreator #
        imageCreateOrder.image = imageCreateOrder #
        imageCalligraphr.image = imageCalligraphr #
        self.imageinkscape = imageinkscape #
        self.imagefontcreator = imagefontcreator #
        self.imageCreateOrder = imageCreateOrder #
        self.imageCalligraphr = imageCalligraphr #


        abtn = tk.Button(self, text="Font Creator", image = imagefontcreator, compound="top", anchor='center', command = self.open_font, bg = "light blue") #Font Creator button
        abtn.rowconfigure(0, weight=1)
        abtn.grid(row=0, column =0, sticky='nesw')
        #abtn.text.pack(side="bottom");

        cbtn = tk.Button(self, text="Inkscape", image=imageinkscape, compound="top", anchor='center', command= self.open_ink, bg = "light blue") #Inkscape button
        cbtn.rowconfigure(1, weight=1)
        cbtn.grid(row=1, column=0, sticky='nesw')

        hbtn = tk.Button(self, text="Calligraphr", image= imageCalligraphr,compound="top", anchor='center', command = self.web , bg = "light blue") #Calligraphr button
        hbtn.rowconfigure(2, weight=1)
        hbtn.grid(row=2, column=0, sticky='nesw')

        obtn = tk.Button(self, text="Create/Send Orders",image=imageCreateOrder, compound="top",anchor='center', command = self.choose_create, bg = "light blue") #Create/Send Orders button
        obtn.grid(row=3, column=0, sticky='nesw')

        #The GUI layout relies upon a grid system of rows and columns
        #These lines configure the number or rows/columns and their weights/sizes
        #To add more, copy these lines and add a new number
        self.grid_rowconfigure(0,weight=1, uniform ='row')
        self.grid_rowconfigure(1,weight=1, uniform ='row')
        self.grid_rowconfigure(2,weight=1, uniform ='row')
        self.grid_rowconfigure(3,weight=1, uniform ='row')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=50)
        self.grid_columnconfigure(2, weight=50)
        self.grid_columnconfigure(3, weight=50)
        self.grid_columnconfigure(4, weight=50)
        self.grid_columnconfigure(5, weight=50)
        self.grid_columnconfigure(6, weight=50)

def main(): #MAIN ROOT FUNCTION

    root = tk.Tk() #Create tk window
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #Fullscreen
    #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='SNlogo.png'))
    app = Example() #Application takes in example window from all functions above
    root.mainloop() #Run application

if __name__ == '__main__': #Run main
    main()