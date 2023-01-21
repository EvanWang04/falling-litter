from tkinter import *
from math import *
from time import *
from random import *

tk = Tk()
s = Canvas(tk, width=600, height=800, background="white")
s.pack()
s.update()

def imageImports(): #Imports all my images
    global recycle, trash, compost, recyclingBin, trashBin, greenBin
    global emptyWaterBottle, coke, styrofoam, plate, apple, banana
    global emptyHeart, fullHeart
    
    emptyWaterBottle=PhotoImage(file="EmptyWaterBottle.gif")
    emptyWaterBottle=emptyWaterBottle.subsample(5)
    
    coke=PhotoImage(file="cokeCan.gif")
    coke=coke.subsample(2)
    
    recycle=[emptyWaterBottle, coke]
    
    styrofoam=PhotoImage(file="styrofoam.gif")
    styrofoam=styrofoam.subsample(13)
    
    plate=PhotoImage(file="plate.gif")
    plate=plate.subsample(2)
    
    trash=[styrofoam, plate]
    
    apple=PhotoImage(file="apple.gif")
    apple=apple.subsample(8)
    
    banana=PhotoImage(file="banana.gif")
    banana=banana.subsample(8)
    
    compost=[apple, banana]

    recyclingBin=PhotoImage(file="recyclingBin.gif")
    recyclingBin=recyclingBin.subsample(11)

    trashBin=PhotoImage(file="trash.gif")
    trashBin=trashBin.subsample(7)

    greenBin=PhotoImage(file="greenBin.gif")
    greenBin=greenBin.subsample(4)

    fullHeart=PhotoImage(file="fullHeart.gif")
    fullHeart=fullHeart.subsample(17)
    
    emptyHeart=PhotoImage(file="emptyHeart.gif")
    emptyHeart=emptyHeart.subsample(17)
    
    
    
def keyPress(event): #key presses
    global binHolding, xSpeed, ySpeed, gameRunning, screen
    if event.keysym=="w" or event.keysym=="W": #Jumping (Removed)
        directions[0]=True
        
    if event.keysym=="a" or event.keysym=="A": #Left
        directions[1]=True
        
    if event.keysym=="d" or event.keysym=="D": #Right
        directions[2]=True
        
    if event.keysym=="space": #Sprint
        xSpeed=15
        
    if event.keysym=="j" or event.keysym=="J": #Compost
        binHolding=0
        
    if event.keysym=="k" or event.keysym=="K": #Recycle
        binHolding=1
        
    if event.keysym=="l" or event.keysym=="L": #Trash
        binHolding=2

    if event.keysym=="p" or event.keysym=="P" or event.keysym=="escape": #Pause
        if screen=="playing":
            gameRunning=False
            screen="pause"
            pause()
            
def keyRelease(event): #Checks for the key releasing
    global xSpeed, ySpeed
    if event.keysym=="w" or event.keysym=="W": #This was for a jump but I removed it
        directions[0]=False
        
    if event.keysym=="a" or event.keysym=="A": #Left
        directions[1]=False
        
    if event.keysym=="d" or event.keysym=="D": #Right
        directions[2]=False
        
    if event.keysym=="space": #Resets sprint to walk
        xSpeed=10
        ySpeed=10
        
def mouseClick(event): #Mouse click
    global gameRunning, screen, gameDifficulty
    
    mousex=event.x #the x location of the mouse when it was clicked
    mousey=event.y
    
    if screen=="menu": #If your on the menu screen
        if 200<mousex<400 and 100<mousey<300: #Checks if it's inside certain coordinates
            screen="difficulty"
            s.delete("all")
            difficulty()
            
        if 200<mousex<400 and 300<mousey<500:
            s.delete("all")
            howToPlay()
            
    elif screen=="gameOver": #If your on the game over screen
        if 200<mousex<400 and 300<mousey<500:
            gameRunning=True
            screen="playing"
            s.delete("all")
            setInitialValues()
            runGame()
            
        if 200<mousex<400 and 500<mousey<700:
            s.delete("all")
            menuScreen()
            
    elif screen=="howToPlay": #If your on the how to play screen
        if 200<mousex<400 and 600<mousey<800:
            s.delete("all")
            menuScreen()

    elif screen=="difficulty": #If your on the difficulty selection screen
        if 200<mousex<400:
            run=False
            if 100<mousey<300:
                gameDifficulty=1
                run=True
            if 300<mousey<500:
                gameDifficulty=2
                run=True
            if 500<mousey<600:
                gameDifficulty=3
                run=True
            if 650<mousey<800:
                s.delete("all")
                menuScreen()
            if run==True:
                s.delete("all")
                gameRunning=True
                screen="playing"
                runGame()

    elif screen=="pause": #If your on the pause screen
        if 200<mousex<400:
            run=False
            if 100<mousey<300:
                gameRunning=True
                screen="playing"
                s.delete(mainMenu, resume, box1, box2)
            if 300<mousey<500:
                s.delete("all")
                menuScreen()
                
    

                
def playingBackground(): #The background you get when you're playing
    s.create_rectangle(0, 0, 600, 800, fill="skyblue", outline="skyblue") #Skyscraper

    for i in range (9):
        for ii in range (6):
            s.create_rectangle(ii*100, 740-i*100, ii*100+100, 740-i*100+100)
            
    for i in range (maxHealth):
        s.create_image(i*60+50, 30, image=emptyHeart)
        
    s.create_rectangle(0, 0, 600, 60, fill="lightgreen")
    s.create_rectangle(0, 740, 700, 900, fill="beige")
    
    
def setInitialValues():
    global x, y, xSpeed,ySpeed, directions, jumpMomentum
    global jump, bins, binHolding, litterx, littery, litterType, amountFalling
    global litterDeleter, wantedAmountFalling
    global distanceBetweenLitter, fallingSpeed
    global health, score, runningNumber
    global maxHealth, mouth, legx, legx1, heartsDeleter
    global maxFallingSpeed
    
    runningNumber=0 #Manages how my legs move
    
    ###Health
    maxHealth=5
    health=maxHealth
    heartsDeleter=[]
    for i in range (maxHealth):
        heartsDeleter.append(0)
        
    #### Extra set up
    playingBackground()
    score=0
    ######## All the bins, movement, and speeds
    bins=["compost", "recycling", "trash"]
    binHolding=0
    x=300
    y=740
    directions=[False, False, False, False]
    xSpeed=10
    ySpeed=10
    #Legs running
    legx=x
    legx1=x
    #Falling litter
    fallingSpeed=3+gameDifficulty
    maxFallingSpeed=fallingSpeed+2
    amountFalling=0
    distanceBetweenLitter=200
    litterx=[]
    littery=[]
    litterType=[]
    litterDeleter=[]
    wantedAmountFalling=10
    
    for i in range (wantedAmountFalling):
        amountFalling+=1
        litterx.append(randint(20, 580))
        try:
            littery.append(littery[i-1]-randint(distanceBetweenLitter, distanceBetweenLitter+50))
        except:
            littery.append(-100)
        litterType.append(choice((compost[randint(0,1)], recycle[randint(0,1)], trash[randint(0,1)])))
        litterDeleter.append(0)

    #Character things
    mouth=[] #Mouth smile
    for i in range (11):
        mouth.append(0)

def scoreKeeper(): #Keeps the score and draws the score
    global tkScore
    scoreText="Score:", score
    tkScore=s.create_text(450, 30, text=scoreText, font="Arial 30")
    
def healthKeeper(): #Keeps the health and displays the health in hearts
    global  gameRunning, gameOverText
    for i in range (health): #Draws the hearts
        heartsDeleter[i]=s.create_image(i*60+50, 30, image=fullHeart)
    if health==0: #Ends the game if my health is 0
        s.delete("all")
        gameOver()
    
def howToPlay(): #How to play screen
    global screen
    screen="howToPlay"
    s.create_rectangle(0, 0, 600, 800, fill="lightblue")
    s.create_text(300, 100, text="Welcome to Falling Litter!!", font="Arial 20")
    
    txts=["In this game, your goal is to catch falling litter that people",
          "throw from skyscrapers using the",
          "corresponding bin. Use A and D to move left and right,",
          "and use space to sprint.", "To change between trash, compost, or recycling,",
          "use J for compost, K for recycling, and L for trash.", "Use P while playing to pause the game.",
          "Have Fun!"] #Array for my description
    
    for i in range (len(txts)): #Long description
        s.create_text(300, i*25+200, text=txts[i], font="Arial 15")
        
    s.create_text(300, 700, text="Back", font="Arial 50") #Back button
    
    s.create_text(100, 400, text="Compost", font="mincho   30") #What goes in the compost
    s.create_text(300, 400, text="Recycling", font="mincho   30")#What goes in the recycling
    s.create_text(500, 400, text="Trash", font="mincho   30")#What goes in the trash
    s.create_rectangle(0, 425, 200, 650) #Shows the images in a box
    s.create_image(75, 500, image=apple)
    s.create_image(125, 600, image=banana)
    
    s.create_rectangle(200, 425, 400, 650)
    s.create_image(300, 500, image=coke)
    s.create_image(325, 600, image=emptyWaterBottle)
    
    s.create_rectangle(400, 425, 600, 650)
    s.create_image(500, 500, image=styrofoam)
    s.create_image(520, 600, image=plate)
    
def gameOver(): #Game over screen
    global screen
    
    screen="gameOver"
    gameOverText="Total score:", score #Total score
    s.create_rectangle(0, 0, 600, 800, fill="lightgreen")
    s.create_text(300, 100, text="Game Over!", font="Arial 50")
    s.create_text(300, 250, text=gameOverText, font="Arial 50")
    s.create_text(300, 400, text="Play Again", font="Arial 50")
    s.create_text(300, 600, text="Menu", font="Arial 50")
    
def updateValues(): #updates my values ex. direction I'm going, my legs
    global x, y, legx1, legx
    if directions[0]:
        1==1
        
    if directions[1]:
        x-=xSpeed
        legx-=xSpeed
        legx1-=xSpeed
        
    if directions[2]:
        x+=xSpeed
        legx+=xSpeed
        legx1+=xSpeed
        
def delete(): #Deletes things that I've created
    global inHand
    
    s.delete(leg1, leg2, head)
    s.delete(inHand)
    for i in range (amountFalling):
        s.delete(litterDeleter[i])
        
    s.delete(tkScore)
    s.delete(shirt1, shirt2)
    s.delete(arm1, arm2)
    s.delete(eye1, eye2)
    for i in range (11):
        s.delete(mouth[i])
        
    s.delete(hat)
    
    for i in range (health):
        s.delete(heartsDeleter[i])
    
            
def boundaries(): #So I can't leave the map
    global x
    if x<15:
        x=15
        
    elif x>585:
        x=585
        
def draw(): #Draws most of my things like my body
    global inHand, leg1, leg2, head
    global runningNumber, legx, legx1
    global shirt1, shirt2, arm1, arm2
    global eye1, eye2, hat
    
    if directions[1]==True or directions[2]==True:
        runningNumber+=1
        if runningNumber%2==0:
            legx+=4
            legx1-=4
        elif runningNumber%1==0:
            legx=x
            legx1=x
            
    else:
        legx=x
        legx1=x
        
    if bins[binHolding]=="compost":
        inHand=s.create_image(x, y-80, image=greenBin)
        
    elif bins[binHolding]=="recycling":
        inHand=s.create_image(x, y-80, image=recyclingBin)
        
    else: #trash
        inHand=s.create_image(x, y-80, image=trashBin)
    
    head=s.create_oval(x-15, y-15, x+15, y-45, fill="#F1C27D") #My head
    hat=s.create_polygon(x, y-40, x+20, y-30, x, y-55, x-20, y-30, smooth=True, fill="orange") #My hat
    leg1=s.create_polygon(x, y, x+13, y+5, legx+5, y+40, smooth=True, fill="#F1C27D", outline="black") #My 1st leg
    leg2=s.create_polygon(x, y, x-13, y+5, legx1-5, y+40, smooth=True, fill="#F1C27D", outline="black") #My 2nd leg
    arm1=s.create_polygon(x+5, y, x+23, y-30, x+17, y-60, smooth=True, fill="#F1C27D", outline="black") #My 1st arm
    arm2=s.create_polygon(x-5, y, x-23, y-30, x-17, y-60, smooth=True, fill="#F1C27D", outline="black") #My 2nd arm
    shirt1=s.create_polygon(x-15, y-15, x+15, y-15, x+15, y+15, x-15, y+15, smooth=True, fill="blue", outline="blue") #My shirt
    shirt2=s.create_rectangle(x-15, y-5, x+15, y+16, fill="blue", outline="blue") #My 2nd shirt, this create the cut off bottom
    eye1=s.create_oval(x+6, y-34, x+4, y-36, fill="black") #My 1st eye
    eye2=s.create_oval(x-6, y-34, x-4, y-36, fill="black") #My 2nd eye
    
    for i in range(11): #Create a smile
        x1=x-5+i
        y1=y-25+i-0.096*i**2
        mouth[i]=s.create_oval(x1, y1, x1, y1, fill="black")

def menuScreen(): #The main menu screen
    global gameRunning, screen, f1
    imageImports()
    screen="menu"
    gameRunning=False
    s.create_rectangle(0, 600, 600, 800, fill="lightgreen")
    
    s.create_polygon(200, 100, 400, 100, 400, 300, 200, 300, fill="lightblue", smooth=True)
    s.create_polygon(100, 300, 500, 300, 500, 500, 100, 500, fill="lightblue", smooth=True)
    
    s.create_text(300, 200, text="Play", font="Arial 50")
    s.create_text(300, 400, text="How To Play", font="Arial 50")
    f1=0
    menuAnimation()
    
def menuAnimation(): #Creates a cool animation for my menu
    global f1, rBin, tBin, gBin
    while True:
        if screen=="menu":
            t1 = round(f1*0.06, 2 ) 
            s1= round(sin(t1), 4) #Uses sin
            
            gBin=s.create_image(100, 400-s1*300, image=greenBin)
            if f1>=20:
                t1 = round((f1-20)*0.06, 2 )
                s1= round(sin(t1), 4)
                rBin=s.create_image(300, 400-s1*300, image=recyclingBin)
            if f1>=40:
                t1 = round((f1-40)*0.06, 2 )
                s1= round(sin(t1), 4)
                tBin=s.create_image(500, 400-s1*300, image=trashBin)
            f1+=1

            s.update()
            sleep(0.03)
            s.delete(gBin)
            if f1>20:
                s.delete(rBin)
            if f1>40:
                s.delete(tBin)
        else:
            break
def caught(): #If I catch a piece of litter
    global amountFalling, score, health, msg
    global sendingMsg, currentF, message, textMade
    
    for i in range (amountFalling):
        if x-40<litterx[i]<x+40 and y-120<littery[i]<y-70:
            if apple==litterType[i] or banana==litterType[i]: #Assigns the piece of litter to a bin
                litterType1="compost"
                
            elif plate==litterType[i] or styrofoam==litterType[i]:
                litterType1="trash"
                
            elif coke==litterType[i] or emptyWaterBottle==litterType[i]:
                litterType1="recycling"
                
            if bins[binHolding]==litterType1: #If I'm using the correct bin
                score+=10
                del litterType[i]
                del litterx[i]
                del littery[i]
                amountFalling-=1
                del litterDeleter[i]
                return
            
            else: #If I'm using the wrong bin
                del litterType[i]
                del litterx[i]
                del littery[i]
                amountFalling-=1
                del litterDeleter[i]
                health-=1
                return    
            
def moreFalling(): #Once one piece of litter hits the ground, or I collect one make a new one
    global amountFalling
    
    if amountFalling!=wantedAmountFalling:
        amountFalling+=1
        litterx.append(randint(20, 580))
        littery.append(min(littery)-randint(distanceBetweenLitter, distanceBetweenLitter+50))
        litterType.append(choice((compost[randint(0,1)], recycle[randint(0,1)], trash[randint(0,1)])))
        litterDeleter.append(0)
        
def fallingTrash(): #Trash that's falling, makes it go down
    for i in range (amountFalling):
        litterDeleter[i]=s.create_image(litterx[i],littery[i], image = litterType[i])
        littery[i]+=fallingSpeed
        
def litterHitTheGround(): #If litter hits the ground
    global amountFalling, health
    
    for i in range (amountFalling):
        if littery[i]>800:
            del litterType[i]
            del litterx[i]
            del littery[i]
            amountFalling-=1
            del litterDeleter[i]
            health-=1
            return
        
def difficulty(): #Difficulty selection page
    s.create_rectangle(0, 0, 600, 800, fill="lightblue")
    s.create_text(300, 200, text="Easy", font="mincho 40")
    s.create_text(300, 400, text="Medium", font="mincho 40")
    s.create_text(300, 600, text="Hard", font="mincho 40")
    s.create_text(300, 700, text="Back", font="mincho 30")
    
def pause(): #Pause menu
    global resume, mainMenu, retry, box1, box2
    box1=s.create_rectangle(100, 100, 500, 300, fill="lightblue")
    box2=s.create_rectangle(100, 300, 500, 500, fill="lightblue")
    resume=s.create_text(300, 200, text="Resume", font="mincho 40")
    mainMenu=s.create_text(300, 400, text="Main Menu", font="mincho 40")
    
def runGame(): #Run game
    global f, distanceBetweenLitter, fallingSpeed
    f=0 #Frame counter
    setInitialValues()
    
    while True: #while True
        if gameRunning==True: #Only run if the game is supposed to be running
            if f%300==0 and f!=0 and fallingSpeed<maxFallingSpeed:
                fallingSpeed+=0.5
            draw()
            moreFalling()
            updateValues()
            caught()
            litterHitTheGround()
            fallingTrash()
            boundaries()
            scoreKeeper()
            healthKeeper()
            
        ########Update, Sleep
        s.update()
        sleep(0.03)
        ########Delete
        
        if gameRunning==True: #Only deletes things if the game is running 
            delete()
            f+=1 #Frame counter

tk.after(0, menuScreen)
s.bind( "<Key>", keyPress)
s.bind( "<KeyRelease>", keyRelease)
s.bind("<Button-1>", mouseClick)
s.pack()
s.focus_set()
tk.mainloop()
