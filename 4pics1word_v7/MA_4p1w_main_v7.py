import random as rm
import winsound as ws
import os
import time

import sys
if "Tkinter" not in sys.modules:
    from tkinter import *


def openPicFile():
    picList = []
    try:
        readFile = open('picList.txt', 'r')
    except IOError:
        print('Error!\nFile not found.')
    else:
        picData = readFile.readlines()
        for x in picData:
            xData = x.strip().split(';')
            picList.append(xData)
        return picList


def saveProgress(a,b,c): #progress:(a)level-number__(b)coin-amount__(c)current-picture.textfile
    playerProgfile = open('Progress.txt', 'a+')
    addText = f'{a};{b};{c}\n'
    playerProgfile.write(addText)
    playerProgfile.close()


def loadProgress(picList):
    try:
        openFile = open('Progress.txt', 'r')
    except IOError:
        #overwrite-picList-txt
        rm.shuffle(picList)
        updateFile = open('picList.txt', 'w+')
        for i in range(len(picList)):
            val=(f'''{i+1};{picList[i][1]}\n''')
            updateFile.write(val)
        
        #values
        picNum = 1
        picPng = f'''{picList[0][1]}'''
        addCoins = 100
        progressVal = False
        pass
    else:
        for line in openFile:
            continue
        lastLine = line
        picNum,addCoins,picPng = lastLine.split(';')
        picNum = int(picNum)
        progressVal = True
    return picNum,addCoins,picPng,progressVal

def createDict(pList):
    picDict = {}
    count=1
    for y in pList:
        picDict[count]=y[1]
        count+=1
    return picDict

#--Class--
class Game(Tk):
    def __init__(self):
        global picNum
        super().__init__()
        
        self.title('4 pics 1 word')
        self.geometry('400x660')
        self.configure(bg='#141d26')

        self.coins = int(addCoins)
        self.save_level = IntVar()
        self.save_coin = IntVar()

        self.empty_text = ''
        self.input_vars = []
        
        self.buttonsList = [] #display-buttons-list
        
        self.buttonTexts = [''] * len(picDict[picNum])#answers-in-a-list
        
        self.lettersList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        
        

    def create_start_window(self):
        self.bg_frame = Frame(self,name='bg_frame',bg='#141d26',width=365,height=625)
        self.bg_frame.place(x=20,y=0)

        self.logo = PhotoImage(file='additional\\face.png')
        self.logo_resized = self.logo.subsample(2,3)
        self.logo_disp = Label(self.bg_frame,name='logo_disp',image=self.logo_resized,bg='#141d26')
        self.logo_disp.place(x=0,y=105)

        self.welcome_label = Label(self)
        
        if progressVal == False:
            start_continue_text = 'Start'
        else:
            start_continue_text = 'Continue'

        self.sc_button = PhotoImage(file='additional\\start-continue.png')
        self.sc_button_resized = self.sc_button.subsample(7,7)
        self.start_button = Button(self,text=start_continue_text,image=self.sc_button_resized,
                                   width=225,height=67,compound=CENTER,bd=0,
                                   font=('System 28 bold',25,'bold'),bg='#141d26',activebackground='#141d26',
                                   command=lambda:[self.start_game(),
                                                                self.logo_disp.place_forget()])
        #self.start_button.pack()
        self.start_button.place(x=78,y=420)

    def start_game(self):
        ws.Beep(300,25) #Play-Sound

        self.welcome_label.destroy()
        self.start_button.destroy()
        self.logo_disp.forget()
        
        self.topFrame()
        self.midFrame()

        #4-Pics-1-Word_images
        self.save_pic = StringVar()
        try:
            self.pics = PhotoImage(file=f'''{picDict[picNum]}.png''')
        except TypeError:
            print('An error has occured. Kindly refresh the program.')
        except TclError:
            print('Something went wrong. Image not found.')
        else:
            self.lblpic = Label(self,image=self.pics)
            self.lblpic.grid(row=2,column=0,columnspan=2)

        #Pass-Button
        try:
            self.passIcon = PhotoImage(file='additional\\pass-icon.png')
            self.passIcon_resized = self.passIcon.subsample(4,4)
        except TclError:
            print('Something went wrong. Image not found.')
        else:
            self.passButton = Button(self,image=self.passIcon_resized,
                                command=self.passLevel,borderwidth=0,relief=RAISED,bg="#141d26",
                                     activebackground="#141d26")
            self.passButton.place(x = 240, y = 580)
    
        #Submit-Button
        try:
            self.submitIcon = PhotoImage(file='additional\\submit-icon.png')
            self.submitIcon_resized = self.submitIcon.subsample(3,3)
        except TclError:
            print('Something went wrong. Image not found.')
        else:
            self.submitButton = Button(self,image=self.submitIcon_resized,
                                   command=self.submitLevel,borderwidth=0,relief=RAISED,bg="#141d26",activebackground="#141d26")
            self.submitButton.place(x = 160, y = 580)

        #Hint-Button
        try:
            self.hintIcon = PhotoImage(file='additional\\hint-icon.png')
            self.hintIcon_resized = self.hintIcon.subsample(4,4)
        except TclError:
            print('Something went wrong. Image not found.')
        else:
            self.hintButton = Button(self,image=self.hintIcon_resized,
                                command=self.showHint,borderwidth=0,relief=RAISED,bg="#141d26",activebackground="#141d26")
            self.hintButton.place(x = 90, y = 580)

    def closingWindow(self): #Completed-the-game

        #winsound.PlaySound(self.end_music_file,winsound.SND_FILENAME | winsound.SND_ASYNC)    
        self.closingFrame = Frame(self, name= "closingFrame",bg="#152238",width=500,height=700)
        self.closingFrame.place(x=0,y=0)

        ws.PlaySound('additional\\congrats.wav',ws.SND_FILENAME|ws.SND_ASYNC) #Play-Sound
        #time.sleep(5)
        #ws.PlaySound(None,ws.SND_PURGE)

        
        closing_label0 = Label(self.closingFrame,name="closing_label0",
                              text="created by: ANDOSAY, ARGONZA, DANO, SUPEDA",font="System 16 bold",
                              bg="#152238",fg = 'orange').place(x=200,y=645,anchor=CENTER)
        
        self.closing_label = Label(self.closingFrame,name="closing_label",
                              text="Congratulations!",font="System 28 bold",
                              bg="#152238",fg = 'Yellow').place(x=200,y=90,anchor=CENTER)
        closing_label2 = Label(self.closingFrame,name="closing_label2",
                               text="You have finished \n4 Pics 1 Word!",
                               font="System 20 bold",bg="#152238",
                               fg = 'White').place(x=200,y=160,anchor=CENTER)
        self.trophy = PhotoImage(file=r"additional\\trophy.png")
        self.trophy_resized = self.trophy.subsample(2,2)
        self.trophy_display = Label(self.closingFrame,name="trophy_display",
                                    image=self.trophy_resized)
        self.trophy_display.pack()
        self.trophy_display.place(x=100,y=220)

        levelPassed_text = f"Levels Passed: {picNum}"
        level_label = Label(self.closingFrame,name="level_label",
                            text=levelPassed_text,font="System 18 bold",
                            bg="#152238",fg = 'violet').place(x=200,y=470,anchor=CENTER)

        coins_text = f"Coins Earned: {self.coins}"
        coins_earned = Label(self.closingFrame, name="coins_earned",
                             text=coins_text,font="System 18 bold",
                             bg="#152238",fg = 'violet').place(x=200,y=508,anchor=CENTER)
        
        quit_button = Button(self.closingFrame,name="quit_button",
                             command=self.quit,text="BYE",font="MSSansSerif 24 bold",
                             bg="red",fg="white").place(x=200,y=575,anchor=CENTER)
        os.remove('Progress.txt')
    def quit(self):
        sys.exit()

    def topFrame(self):
        global picNum
        self.top_frame = Frame(self,name='top_frame',width=400, height=50,bg='#243447')
        self.top_frame.grid(row=1,column=0,columnspan=2,pady=10)

        #level_label
        self.level_label = Label(self.top_frame,name='top_frame_label',bg='#243447',
                                text=f'''Level {picNum}''',font=('System 18 bold',20),fg='#ffffff')
        self.level_label.place(x=10,y=5)

        #coins_label
        self.coins_label = Label(self.top_frame, name='coins_label', bg='#243447',
                            text=f'{self.coins}',font=('System 18 bold',20, 'bold'),fg='#ffffff')
        self.coins_label.place(x=340,y=6)


        try: #display-coin-image
            self.coin_pic = PhotoImage(file='additional\\coin.png')
        except IOError:
            print('Error!\nImage not found.')
        except TclError:
            print('Something went wrong.\nImage failed to load.')
        else:
            self.coin_pic_resized = self.coin_pic.subsample(7,7)
            self.coinpiclbl = LabelFrame(self,highlightcolor='#243447')
            self.coinpiclbl = Label(self.top_frame,name='coin_pic',image=self.coin_pic_resized,
                                    width=56,height=41,bg="#243447",activebackground="#243447")
            self.coinpiclbl.place(x=283,y=3)


    def midFrame(self):
        global picNum
        self.midFrame = Frame(self,bg='#ffffff',bd=0)
        self.midFrame.grid(row=4,column=0,columnspan=2)

        #empty-space-for-the-letters
        self.empty_space = Frame(self,width=100,height=50,borderwidth=5,
                                 bg='#141d26',bd=3)
        self.empty_space.grid(row=3,column=0,columnspan=2,pady=15)

        #display-buttons
        self.showInput(self.buttonTexts)

        #empty-label-display-for-clicked-letters
        self.letterLabel = Label(self,font=('Comic sans ms',0,'bold'))

        #shuffle-letterList
        rm.shuffle(self.lettersList)
        self.keyboard(self.lettersList)

    def keyboard(self,l_list):
        letters = ''.join([n for n in l_list])
        random_letters = rm.sample(letters, 12 - len(picDict[picNum]))

        #add-letters-to-random letters
        mixed_letters = list(picDict[picNum].upper()) + random_letters
        rm.shuffle(mixed_letters)

        #add-picture-to-key-tile
        self.alphatile_pic = PhotoImage(file='additional\\key_tile.png')

        #grid-of-buttons-for-letters
        self.alpha_buttons = []  # add this to store buttons
        for row in range(2):
            for col in range(6):
                index = row * 6 + col
                letter = mixed_letters[index]
                
                alpha_button = Button(self.midFrame,text=letter,fg='#ffffff',
                    font=("Comic Sans MS", 15, "bold"),width=50,height=45,
                    command=lambda letter=letter: self.buttonClick(letter),
                    image=self.alphatile_pic,bd=5,bg='#C04000',compound=CENTER)
                alpha_button.grid(row=row,column=col)#,padx=3,pady=4)
                self.alpha_buttons.append(alpha_button)  # add button to list

    def changeImage(self): #change-the-4pics-image
        global picNum
        picNum+=1
        if picNum == 51:
            self.closingWindow()
        self.pics.config(file=f'''{picDict[picNum]}.png''')
        self.level_label.config(text=f'''Level {picNum}''')

    def showInput(self,nlist): #displays-the-chosen-letter
        button_width = max(len(char) for char in nlist)
        
        if button_width == 0: #para-lang-di-mabago-size-ng-button_width
            button_width = 1

        #add-picture-to-key-tile
        self.displaytile_pic = PhotoImage(file='additional\\display_tile.png')
        
        #empty-buttons-for-input-letters
        count=0
        for text in nlist:
            count+=1
            self.emptyButton = Button(self.empty_space,font=('Comic sans ms',14),fg='black',
                                      width=button_width+30,text=text,bg='#243447',activebackground="#243447",
                                      image=self.displaytile_pic,compound=CENTER,
                                      height=40)
            self.emptyButton.config(command=lambda btn=self.emptyButton: self.remove_empty_letter(btn),
                                    state='normal')
            self.emptyButton.grid(row=0,column=count,padx=3)
            self.buttonsList.append(self.emptyButton)

    def remove_empty_letter(self,btn): #removes-and-changes-the-clicked-button-into-empty
        self.removeLetter(btn)
        self.emptyLetter(btn)
        
        ws.Beep(200,25) #Play-Sound

    def removeLetter(self,btn):
        btn.config(text='')

    def emptyLetter(self, btn):
        btnIndex = btn.grid_info()['column']-1
        letter = self.buttonTexts[btnIndex]
        self.buttonTexts[btnIndex] = ''
        for alpha_button in self.alpha_buttons:
            if alpha_button.cget('text') == letter:
                alpha_button.config(state='normal')
                break
        btn.config(text='', state='normal')

    def emptyDisplay(self): #only-for-submit-and-pass-button
        self.buttonTexts = [''] * len(picDict[picNum])#answers-in-a-list

    def buttonClick(self,letter): #Append-clicked-letter-to-label-text

        self.correct = picDict[picNum]
        self.answerList = list(self.correct)

        self.current_text = self.letterLabel.cget("text")
        ws.Beep(200,25) #Play-Sound
        count=0
        while len(picDict[picNum]) != count:
            if self.buttonTexts[count] != '':
                count+=1 
            elif self.buttonTexts[count] == '':
                self.buttonTexts[count] = self.current_text+letter
                self.showInput(self.buttonTexts)

                # disable the button that was clicked
                for alpha_button in self.alpha_buttons:
                    if alpha_button.cget('text') == letter:
                        alpha_button.config(state='disabled')
                        break
                
                break
        else:
            print('The boxes are full!')#checking lang

    def checkingAnswers(self):
        answer = ''.join(self.buttonTexts)
        if answer.lower() == picDict[picNum]:
            ws.PlaySound('additional\\correct-sound.wav',ws.SND_FILENAME|ws.SND_ASYNC) #Play-Sound
            time.sleep(0.5)
            ws.PlaySound(None,ws.SND_PURGE)
            
            print('Correct Answer!\n+10\n')
            self.emptyDisplay()
            return True
        else:
            ws.PlaySound('additional\\fail-sound.wav',ws.SND_FILENAME|ws.SND_ASYNC) #Play-Sound
            time.sleep(0.5)
            ws.PlaySound(None,ws.SND_PURGE)

            print('Incorrect Answer!')
            self.emptyDisplay()
            return False
        
    def passLevel(self): #subtract-10-coins
        if self.coins != 0:
            ws.PlaySound('additional\\pass-sound.wav',ws.SND_FILENAME) #Play-Sound
            time.sleep(0.2)
            ws.PlaySound(None,ws.SND_PURGE)
            print('Skip Level.\n-10\n')
            self.coins -= 10
            self.coins_label.config(text=f'{self.coins}')
            self.letterLabel.config(text="")
            self.changeImage()

            #Save-Progress
            self.save_level.set(picNum)
            self.save_coin.set(self.coins)
            self.save_pic.set(f'''{picDict[picNum]}.png''')

            saveProgress(self.save_level.get(),self.save_coin.get(),self.save_pic.get())

            self.emptyDisplay() 

            self.deleteKeyboard() #deletes-keyboard-buttons
            self.deleteButtons() #deletes-dosplay-buttons
            
        elif self.coins == 0:
            print('No more coins left.')

        
    def submitLevel(self): #add-10-coins
        value = self.checkingAnswers() #validation-if-tama-sagot
        if value == True:
            self.coins += 10
            self.coins_label.config(text=f'{self.coins}')
            self.changeImage()

            #Save-Progress
            self.save_level.set(picNum)
            self.save_coin.set(self.coins)
            self.save_pic.set(f'''{picDict[picNum]}.png''')
        
            saveProgress(self.save_level.get(),self.save_coin.get(),self.save_pic.get())

            self.deleteKeyboard() #deletes-keyboard-buttons

        else:
            #enable the disabled letters
            for alpha_button in self.alpha_buttons:
                if alpha_button.cget('state') == 'disabled':
                    alpha_button.config(state='normal')

        
        self.deleteButtons() #deletes-display-buttons

            
    def deleteKeyboard(self): #delete-keyboard-buttons
        #Reset-keyboard-and-mix-the-letters-again
        for keys in self.midFrame.winfo_children():
            keys.config(state="normal", text='')
        self.keyboard(self.lettersList)

    def deleteButtons(self):#delete-display-buttons
        #changes-the-length-of-buttons
        self.buttonTexts = [''] * len(picDict[picNum]) 
        for button in self.empty_space.winfo_children():
            button.destroy()
        self.showInput(self.buttonTexts)

    def showHint(self):#For-hint-button
        if self.coins <= 1:
            print('Not enough coins.')
            return
        
        
        try: #determine-if-the-list-exists
            if isinstance(self.empty_indices,list):
                print('Bought hint.\n-2')
        except AttributeError:
            self.correct = picDict[picNum]
            self.answerList = list(self.correct)
            self.empty_indices = [i for i, label in enumerate(self.buttonTexts)]
        else:
            pass

        
        if 0 <= len(self.empty_indices) <= 1: #check if list is empty
            return


        while True:
            self.hint_index = rm.choice(self.empty_indices)
            if self.buttonTexts[self.hint_index] != '':
                self.hint_index = rm.choice(self.empty_indices)
            else:
                break
        
        newText,btnIndex = self.getnewText(hint_random) #call-def-function
        
        #minus-2-coins
        self.coins -= 2
        self.coins_label.config(text=f'{self.coins}')

        #display-random-hint
        count=0
        for button in self.buttonsList:
            btn_text_val = button.cget('text')
            if btn_text_val == '':
                if self.empty_indices[count] == self.hint_index:
                    if newText.lower() == self.answerList[self.hint_index]: #hahanapin kung saang button si letter
                        self.buttonTexts[self.hint_index] = newText #add-letter-to-list
                        button.config(text=newText)#add-letter-to-button

                        self.buttonsList.remove(button)
                        self.empty_indices.remove(self.hint_index)
                        break

                else:
                    count+=1
            else:
                count+=1

        # disable the button that was clicked
        for alpha_button in self.alpha_buttons:
            if alpha_button.cget('text') == self.buttonTexts[self.hint_index]:
                alpha_button.config(state='disabled')
                break


    def getnewText(self,hint_random):#get-value-of-random-letter-in-display-button
        btnIndex = self.emptyButton.grid_info()['column']-1
        newText = hint_random.upper()
        return newText,btnIndex


#Start-Of-Code
picList = openPicFile() #dictionary-ito
picNum,addCoins,picPng,progressVal = loadProgress(picList)
picDict = createDict(picList)

window = Game()

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the size of the window
window_width = 400
window_height = 660
window.geometry(f"{window_width}x{window_height}")

# Calculate the x and y coordinates of the top-left corner of the window to center it on the screen
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window's position
window.geometry("+{}+{}".format(x, y))

window.create_start_window()


window.mainloop()

