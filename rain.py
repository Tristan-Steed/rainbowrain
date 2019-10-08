import turtle 
import random
import time
from threading import Thread


bucketPosition=0
score=0
miss_count=0
bossHealth=100
is_active=False

class Raindrop:
    def __init__(self,startx,starty,speed_value):
        self.starty=starty
        self.startx=startx
        screenstore=turtle.screensize()
        screeny=screenstore[1]
        self.tspawn=turtle.Turtle()
        self.tspawn.hideturtle();
        self.tspawn.speed(speed_value)
        self.tspawn.tilt(90)
        self.tspawn.tilt(180)
        #print(str(tspawn.pos()))
        self.tspawn.color('red')
        self.tspawn.penup();
        self.tspawn.setpos(startx,starty);
        self.tspawn.showturtle()
        self.tspawn.speed(speed_value)
       # tspawn.setx(startx)
        #tspawn.sety(starty)
        #tspawn.pendown()
        self.tspawn.goto(startx,350)#starts the arrow off
        self.tspawn.goto(startx,-400)#returns the arrow
       

    def collidesWith(self,object):
        if object.pos()[0]==self.tspawn.pos()[0] and object.pos()[1]==self.tspawn.pos()[1]:
            return True
        return False

    def returnArrow(self):
        self.tspawn.tilt(180)
        self.tspawn.color('blue')
        self.tspawn.goto(self.startx,boss.ycor())
        #print(str(tspawn.pos()))
        self.dropPosition=self.tspawn.position()


    def destroy(self):
        self.tspawn.reset()

    def returnDropPosition(self):
        return self.dropPosition

screen=turtle.Screen()
screen.title("Red Rain Defender")
screen.setworldcoordinates(-700,-500,700,500)
turtle.bgcolor("black")


#screen.clear()
#turtle.color('deep pink')

character=turtle.Turtle()


boss=turtle.Turtle()
boss.shapesize(5,5,12)
boss.penup()
boss.speed(500)
boss.goto(272.00,400)
boss.speed(1000)
boss.shape("turtle")
boss.color("red")
boss.tilt(270)

        
            #self.character=turtle.Turtle();
character.penup()
character.speed(500)
character.goto(272.00,-400.00)
character.speed(100)
screen.addshape("boss.gif")
character.shape("boss.gif")
character.color("blue")

textbot=turtle.Turtle()
textbot.hideturtle()

'''TODO add switch case'''
def update_miss_count_txt():
    global miss_count
    global textbot
    textbot.reset()
    miss_star="* * * *"
    if(miss_count==1):
        miss_star="* * *"
    elif(miss_count==2):
        miss_star="* *"
    elif(miss_count==3):
        miss_star="*"
    elif(miss_count>3):
        miss_star="none"

    textbot.hideturtle()
    textbot.penup()
    textbot.goto(600,450)
    style = ('Courier', 15, 'bold')
    textbot.color("yellow")
    textbot.write("Lives \n"+miss_star, font=style, align='center')


screenwidth=screen.window_width()
spacing=screenwidth/10

playerInfo=turtle
playerInfo.hideturtle()


def updatePlayerHealth():
    
    global playerInfo

    miss_star=""
    if(miss_count==1):
        miss_star="*"
    elif(miss_count==2):
        miss_star="**"
    elif(miss_count>2):
        miss_star="***"

    style = ('Courier', 30, 'italic')
    playerInfo.speed(500)
    playerInfo.reset()
    playerInfo.penup()
    playerInfo.hideturtle()
    playerInfo.goto(0,character.ycor()-60)
    playerInfo.color('blue')



    #writer.write("Health: \n"+str(bossHealth)+"%"+'\n'+"   "+miss_star, font=style, align='center')
    playerInfo.write("MISSES: "+miss_star, font=style, align='center')


def createCoordinateMatrix():
    spawnCoordinates=[]
    startingvalue=-400
    for i in range(10):
        spawnCoordinates.append(startingvalue)
        startingvalue+=spacing
    return spawnCoordinates

coordMatrix=createCoordinateMatrix()

def k2():
    #boss.forward(spacing)
    if(character.xcor()>-600 and character.xcor()<600):
        character.forward(spacing)
    elif(character.xcor()<-600):
        character.goto(character.xcor()+spacing,character.ycor())
    elif(character.xcor()>600):
        character.goto(character.xcor()-spacing,character.ycor())     
    global bucketPosition 
    bucketPosition =character.xcor()



def k3():
    #boss.backward(spacing)
    if(character.xcor()>-600 and character.xcor()<600):
        character.backward(spacing)
    elif(character.xcor()<-600):
        character.goto(character.xcor()+spacing,character.ycor())
    elif(character.xcor()>600):
        character.goto(character.xcor()-spacing,character.ycor())
    
    global bucketPosition 
    bucketPosition =character.xcor()






"""
def spawnrow():
    startingvalue=-400
    for i in range(50):
        index=random.randint(0,len(coordMatrix)-1)
        tempdrop=Raindrop(coordMatrix[index],400)
    #turtle.write("The score is "+str(tempdrop.returnDropPosition)+"\n", font=style, align='center')
        print("The score is "+str(type(tempdrop.returnDropPosition()))
        if(index==bucketPosition):
            score=score+1
    #turtle.write("The score is "+str(score), font=style, align='center')

"""

writer=turtle
writer.hideturtle()





def updateHealth():
    global writer
    global score


    style = ('Courier', 30, 'italic')

    #writer.write("Health: \n"+str(bossHealth)+"%"+'\n'+"   "+miss_star, font=style, align='center')
    writer.speed(500)
    writer.reset()
    writer.penup()
    writer.hideturtle()
    writer.goto(boss.xcor(),boss.ycor()+30)
    writer.color('red')


    writer.write("Health: "+str(bossHealth)+"%"+'\n'+"   ", font=style, align='center')

    #writer.hideturtle()


def end_game():
    global writer
    global score
    writer.speed(500)
    writer.reset()
    writer.hideturtle()
    writer.color('red')
    style = ('Courier', 50, 'bold')
    writer.write("Game Over \nFinal score: "+str(score), font=style, align='center')
    #writer.hideturtle()

def spawnrow():
    global is_active
    is_active=True
    update_miss_count_txt()
    for i in range(50000):
        global score
        global miss_count
        global bossHealth
        miss_count_first=miss_count
        index=random.randint(0,len(coordMatrix)-1)
        ''' Gets raindrop position '''
        boss.goto(coordMatrix[index],300)
  
        if __name__ == '__main__':
            Thread(target = updateHealth).start()
            if(miss_count>miss_count_first):
                Thread(target = updatePlayerHealth).start()
        
        tempdrop=Raindrop(coordMatrix[index],350,4)
        #print("-----coordmat:"+str(coordMatrix[index])+"*****bucket:"+str(bucketPosition))

        if(tempdrop.collidesWith(character)):
            scorestore=score
            score+=1
            tempdrop.returnArrow()

            if(tempdrop.collidesWith(boss)):
                bossHealth-=1
                boss.color('blue')
                boss.right(180)
                time.sleep(0.25)
                boss.color('red')
                boss.right(180)
                
     
            tempdrop.destroy()

        else:
            miss_count+=1
            update_miss_count_txt()
            tempdrop.destroy()
            if(miss_count>3):
                is_active=False
                end_game()
                return 0
            print("Charater position: "+str(character.position())+"coordmatrix: "+str(coordMatrix[index])+"*****")
            print("\n "+str(miss_count)+'\n')
            print("Star added \n")
            print("The matrix: "+str(coordMatrix))
start_text=turtle

def launch():
    global is_active
    global start_text
    global bossHealth
    global miss_count
    if(is_active==False):
        score=0
        bossHealth=100
        miss_count=0
        startEasyGame()
        start_text.reset()
        start_text.destroy()

def startScreen():
    global character
    global is_active
    global start_text
    boss.hideturtle()
    character.hideturtle()
    start_text.color('red')
    style = ('Courier', 30, 'italic')
    start_text.write("Click the spacebar( |__________| ) to start game: \n"+'\n'+"   ", font=style, align='center')
    screen.listen()
    if(is_active==False):
        screen.onkey(launch,"space")

def startEasyGame():
    global character
    boss.showturtle()
    character.showturtle()
    screen.listen()
    #screen.ontimer(graphicalText,10)
    screen.ontimer(spawnrow,100)
    screen.onkey(k3, "Left")
    screen.onkey(k2, "Right")

startScreen()
#turtle.penup()
#turtle.goto(200,400)
#turtle.pendown()
#turtle.goto(200,200)
"""
drop=Raindrop(0,400)
drop2=Raindrop(100,400)
drop=Raindrop(200,400)

"""
#style = ('Courier', 30, 'italic')
#turtle.write("nothing", font=style, align='center')
#turtle.hideturtle()
screen.mainloop()

