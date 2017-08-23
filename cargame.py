import pygame, random, schedule,time

displayWidth = 800
displayHeight = 600

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), )

pygame.display.set_caption("Racecar")

car_img = pygame.image.load("car.jpg")

carWidth = 50
carLength = 50
car_img = pygame.transform.scale(car_img , (carWidth, carLength))

green = (0,255,0)
red = (255, 0, 0)
black = (0, 0, 0)

pygame.font.init()
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text, xpos, ypos, size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((xpos),(ypos))
    gameDisplay.blit(TextSurf, TextRect)

class Car:
    car_x_pos = displayWidth/2
    car_y_pos = 500
    scoreAdd = 1        #this varibale is helpfull in the Pause function

    '''Initializing Car. Step is the change in x. carSpeed is speed at which the car moves sideways'''
    def __init__(self):
        self.step = 0           #the x position of the car
        self.carSpeed = 10      #the change in x position of the car
        self.running = False    #Checks if car is running. It is false when the car crahses and during the startscreen and true when enter is pressed
        self.isCarCrashed = False       #Checks if car is crashed or not. Used when pressing c to continue the game and to keep track of score
        self.score = 0           #keeps tacks of score. It is resetted after presssing C once the car crashes
        self.totalBonus = 0      #keeps track of the total bonus points the player earns.(Check the obstacle class code)
        self.score_add = self.scoreAdd       #Keeps track of how much to add to the score. It depends on the levels. It is also ressetted after presssing C.
        self.carHitRightBound = False   #checks to see if the car hits the right wall
        self.carHitLeftBound = False    #checks to see if the car hits the left wall
        self.isCarPaused = False        #checks to see if the game is paused or not

    def reset(self):
        self.car_x_pos = displayWidth/2     #sets the x position of car
        self.running = True     #it becomes True, so that the loop can reset everything
        self.isCarCrashed = False   #it becomes false to allow the car loop to operate. the car is no longer in crashed state after everything has ben resetted
        self.isCarPaused = False
        self.score = 0      #resets the score
        self.score_add = 1  #resets the score step
        self.totalBonus = 0 #resets the total bonus points to 0
        self.carHitLeftBound = False    #resets the boolean, The car is not hitting the left wall
        self.carHitRightBound = False   #resets the boolean, The car is not hitting the right wall

    '''movement function allows keys to function. It also has the display update function and the clock.tick function to set the fps'''
    def movement(self):

        if self.car_x_pos < 0 or self.car_x_pos > displayWidth - 50:
            self.step = 0   #sets up the boundaries to not allow the car to move any farther

        if self.car_x_pos <= carWidth:
            self.carHitLeftBound = True #When car hits the left wall

        if self.car_x_pos >= displayWidth - carWidth:
            self.carHitRightBound = True    # When car hits the right wall

        if self.car_x_pos >= carWidth:
            self.carHitLeftBound = False    #When car is not htting the left wall

        if self.car_x_pos <= displayWidth - carWidth:
            self.carHitRightBound = False   #When car is not hitting the right wall

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.carHitRightBound == False:
                    self.step = self.carSpeed

                if event.key == pygame.K_LEFT and self.carHitLeftBound == False :
                    self.step = -self.carSpeed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if self.isCarCrashed == True:
                    if event.key == pygame.K_c:
                        self.reset()

                if event.key == pygame.K_p:
                    self.isCarPaused = True
                if self.isCarPaused == True:
                    if event.key == pygame.K_RETURN:
                        self.isCarPaused = False

            # This allows the action to take place while the key is pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.step = 0

        self.car_x_pos += self.step

        if self.running == True:
            gameDisplay.blit(car_img, (self.car_x_pos, self.car_y_pos))
            # pygame.draw.line(gameDisplay, red, (self.car_x_pos - 50, 550), (self.car_x_pos + 100, 550), 10)
            message_display("score: " + str(self.score), 725, 50, 25)
            message_display("bonus: " + str(self.totalBonus), 725, 75, 25)  #displays the total bonus points
            pygame.display.update()
            clock.tick(60)      #This is like the fps of the game

###                         ###
###      car variable       ###
### initiates the car class ###
###                         ###
car = Car()

def scoreUP():
    if car.running == True and car.isCarPaused == False:
        car.score += car.score_add

def readHighScore():
    if car.isCarCrashed == True:        #This function only works when the car is crashed
        readGameHighScore = open("High_Score.txt", "r")     #opens the .txt file in which all the scores are saved
        readLines = readGameHighScore.readlines()       #reads all the lines in the .txt file and stores them as a list
        High_Score_List = []        #A list in which the highscores on each line are stored
        for each in range(0,len(readLines)):
            lineLength = len(readLines[each])       #stores the length of each line.
            lineLength = lineLength - 1         #subtracts one to account for the '\n'. This accounts for the number of digits in the scores
            readLineScore = readLines[each][11:lineLength]  #It reads 'each' line from the 'readLines' list and then reads the charachters from 11 to linelength
            readLineScore = int(readLineScore)      #converts it into an integer
            High_Score_List.append(readLineScore)   #appends each integer into the 'High_Score_List'
        GameHighScore = max(High_Score_List)    #gets the maximum integer from the list
        readGameHighScore.close()       #closes the text file
        return GameHighScore

###         Pause and Menu          ###
class PauseMenu(Car):       #argument is "Car" to access variables from that class
    def __init__(self, classCar):
        self.menuRunning = True     #checks to see if menu is running
        classCar.running = False    #checks to see if the Car class is running. Menu only runs when the Car class is not running
    def gameStart(self, classCar):
        gameDisplay.fill((255,255,255))
        message_display("Welcome to Race Car", displayWidth/2, displayHeight/2, 25)
        message_display("Press 'enter' to start", displayWidth/2, displayHeight/2 + 30, 25)
        message_display("Use arrow keys to navigate your vehicle", displayWidth/2, displayHeight/2 + 60, 25)
        message_display("Press 'p' to pause and 'enter' to unpause", displayWidth/2, displayHeight/2 + 90, 25)
        message_display("Press 'Esc' to exit ", displayWidth/2, displayHeight/2 + 120, 25)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    classCar.running = True     #starts the Car class loop

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


'''This class sets up obstacles that move down. It uses the 'car_x_pos' variable from the 'Car' obstacle to calculate distance between the car and the obstacle
it also has the crash function'''
class obstacle:        
    ###    These variables are shared by all instances of the class    ###
    obsWidth = 50
    obsLength = 50
    crashed = False  # checks to see if the car has crashed into the obstacle or not
    obs_xpos = random.randrange(0, displayWidth)  # generates random values for the x position of the obstacle
    
    ###    These variables are shared only by the instance      ###
    def __init__(self, color = green):
        self.obs_ypos = random.randrange(-600, -50)             #generates random values for the y position of the obstacle
        self.obsMaxspeed = 20  # sets the maximum speed of the obstacle
        self.obsMinspeed = 10  # sets the minimum speed of the obstacle
        self.obsSpeed = random.randrange(self.obsMinspeed,self.obsMaxspeed) #generates random values for the speed of the obstacle
        self.bonusScore = 5
        self.color = color

    def loop(self, car_class):      #car_class uses the 'Car' class to call the x position of the car by accessing the 'car_x_pos' variable
        if car_class.running == True:
            self.Carypos = car_class.car_y_pos
            self.Carxpos = car_class.car_x_pos  #assigns the car_x_pos variable from the "Car" class to the variable
            self.obs_ypos += self.obsSpeed

            pygame.draw.rect(gameDisplay, self.color, (self.obs_xpos,self.obs_ypos,self.obsWidth,self.obsLength))

            if car_class.isCarPaused == True:     #pauses the game
                message_display("Game Paused. Press 'Enter' to continue.", displayWidth/2, displayHeight/2, 25)
                car_class.carSpeed = 0
                self.obsSpeed = 0
                car_class.score_add = 0

            if car_class.isCarPaused == False:   #unpauses the game
                car_class.carSpeed = 10
                self.obsSpeed = random.randrange(self.obsMinspeed,self.obsMaxspeed)
                car_class.score_add = car_class.scoreAdd

            if self.obs_ypos > displayHeight:       #resets the obstacle above the display screen
                self.obsSpeed = random.randrange(self.obsMinspeed,self.obsMaxspeed)
                self.obs_ypos = -100        #sets the y position of the obstacle above the screen to give some time to react
                self.obs_xpos = random.randrange(0, displayWidth)       #generates random values for the x position of the obstacle

            self.ydist = abs(self.obs_ypos - self.Carypos)       #calculates the distance between y pos of car and y pos of obstacle
            self.xdist = abs(self.obs_xpos - self.Carxpos)       #calculates the distance between x pos of car and x pos of obstacle
            self.xdistFromMid = (self.xdist+carWidth)/2          #calculates the x distance from the middle of the car to the middle of the obstacle

            if self.xdistFromMid < 75 and 500<self.obs_ypos<550 :   #gives bonus points if a player does a near miss
                if car_class.isCarPaused == False and self.xdistFromMid >50:
##                    print("bonus " + str(self.xdistFromMid))
                    car_class.totalBonus += self.bonusScore
                    car_class.score += self.bonusScore        #add bonus points to the score

            ### This is the Car crashing code   ###
            if self.xdist < self.obsWidth and self.obs_ypos > Car.car_y_pos and self.obs_ypos < Car.car_y_pos + self.obsLength :
                time.sleep(1)
                car_class.isCarCrashed = True   #when car crashes, it becomes true
                self.crashed = True     # this boolean is used in running the "gameLevels" the function
                car_class.running = False #when the car crashes, it sets it false to stop the car function loop

                gameHighScore = open("High_Score.txt", "a")
                gameHighScore.write("HighScore: ")
                gameHighScore.write(str(car.score) + '\n')
                gameHighScore.close()

                self.HighScore = readHighScore()        #aaves the max score. readHighScore() returns the max score

                message_display("You Crashed. Game Over." , displayWidth/2, displayHeight/2, 50)
                message_display("Press 'c' to try again", displayWidth/2, displayHeight/2 + 55, 35)
                message_display("Your Score is: " + str(car.score), displayWidth/2, 400,25)
                message_display("Bonus points: " + str(car.totalBonus), displayWidth/2,450, 25)
                message_display("High Score: " + str(self.HighScore), displayWidth/2, 500, 25)
                pygame.display.update()

obs_1 = obstacle(green) #initiates the obstacles to be used in levels
obs_2 = obstacle(green)
obs_3 = obstacle(red)

def gameLevels():
    global score_add

    if obs_1.crashed == True or obs_2.crashed == True or obs_3.crashed == True:

        #When the player continues after crashing, the y positoin of all the obstacles should be reset to -100, not just the one the [layer crashed into
        #If the y positions are reset in the obstacle class, then only the obstacle in which the player crashed gets resetted, while the others
        #continue from their previous y positions. Thus the player might crash into them instantly without seeing them.
        obs_1.obs_ypos = -100   # sets the y position of each obstacle to -100 so that the player doesnt crash into another obstacle once he continues
        obs_2.obs_ypos = -100
        obs_3.obs_ypos = -200

        obs_1.crashed = False   #once the values have been resetted, the crashed boolean of each obstacle is set to False again so that the game continues
        obs_2.crashed = False
        obs_3.crashed = False

    if car.score > 0:
        obs_1.loop(car)
        car.score_add = 1
    if car.score > 50:  # the second level starts after the player crosses 25 points
        obs_2.loop(car)
        car.score_add = 2   #2 points are add in level 2
    if car.score > 200:
        obs_3.obsMinspeed = 15  #the minimum speed of the third obstacle is inceased so that moves fast
        obs_3.loop(car)
        obs_3.bonusScore = 15
        car.score_add = 5       #5 points are add after level 5

schedule.every(0.5).seconds.do(scoreUP)     #adds points after every 0.5 seconds

Menu = PauseMenu(car)

if __name__ == "__main__":
    while car.running == False and Menu.menuRunning == True:
        Menu.gameStart(car)

    while car.running == True or car.isCarCrashed == True:
        schedule.run_pending()          #runs the schedule code
        gameDisplay.fill((255,255,255))     #fills the display with white
        gameLevels()
        car.movement()
