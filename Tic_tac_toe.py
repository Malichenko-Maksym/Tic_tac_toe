import pygame
import time
# This class contains information about matrix, sizes and initial values of variables
# "restart" method setting default values of variables, so we use it when starting or restarting our game
# "game_end" method stop our game, and enable to play cutscene (drawing line)
# "nullify_sums" method nullify all sums in matrix all lines, it also creates an array, which contain sums of all lines
#  we use it each time, before we start checking our matrix
class game_tools_and_variables():
    def __init__(self,width,height, margin):
        self.width = width
        self.height = height
        self.margin = margin
        self.restart()

    def restart(self):
        self.zero_turn=False
        self.continue_of_game=True
        self.free_place=9
        self.ending=False
        self.matrix=[[0]*3 for i in range(3)]
        self.win_line=None
        self.line_type=None

    def game_end(self):
        self.ending=True
        self.continue_of_game=False

    def nullify_sums(self):
        self.sum_in_row=0
        self.sum_in_column=0
        self.sum_diagonal=0
        self.sum_antidiagonal=0
        self.all_sums=[self.sum_in_row, self.sum_in_column, self.sum_diagonal, self.sum_antidiagonal]
# "draw_win_line" method allow us to draw winning line in appropriate place. 
# If there was no winner, line isn't drawn. Otherwise "line_type" variable give to us information what type of line the winning line is: 
# if "line_type"=0 then winning line is a row, if = 1 then is a column, 2 and 3 stands for diagonal and antidiagonal respectively
#-----------------------------------------------------------------------------------------------------------------------------------
# "win_line" variable let us to know ordinal number of the line of the corresponding type (first,second or third)
# We have only one diagonal and antidiagonal lines, so in that case "win_line" variable won't be used

    def draw_win_line(self):
        if self.line_type==None:
            return None
        else:
            if self.line_type==3:
                for i in range(305):
                    pygame.draw.circle(screen, (0,0,255), (19+i,323-i), 10)
                    screen_refresh()
            elif self.line_type==2:
                for i in range(305):
                    pygame.draw.circle(screen, (0,0,255), (19+i,17+i), 10)
                    screen_refresh()
            elif self.line_type==1:
                for i in range(305):
                    pygame.draw.circle(screen, (0,0,255), (self.win_line*self.width+(self.win_line+1)*self.margin+50,17+i), 10)
                    screen_refresh()
            else:
                for i in range(307):
                    pygame.draw.circle(screen, (0,0,255), (17+i,self.win_line*self.height+(self.win_line+1)*self.margin+50), 10)
                    screen_refresh()
# Function allows us to see all printed objects (with a small delay, to let us see, how they were drawed)  
def screen_refresh():
    pygame.display.update()
    time.sleep(0.001)
# Start parametrs, game initiation, texts and background
pygame.init()
window = (340,340)
screen = pygame.display.set_mode(window)
general_font= pygame.font.SysFont("calibri",40)
special_font= pygame.font.SysFont("calibri",32)
background_colour=(238,233,233)
caption_cross_won= general_font.render("Cross player won!",1,(3,52,212), (180,205,205))
caption_zero_won= general_font.render("Zero player won!",1,(3,52,212), (180,205,205))
caption_nobody_won= general_font.render("You are equal!",1,(3,52,212), (180,205,205))
caption_restart= special_font.render("Click here, to play again",1,(131,139,139), (202, 225, 255))
# Check if all necessary file exist, downloading photoes and scaling them to the right sizes, setting icon and title
try:
    pygame.display.set_caption("Tic-Tac-Toe")
    pygame.display.set_icon(pygame.image.load("Tic_tac_toe icon.png"))  
    cross = pygame.image.load(r'cross.png').convert_alpha()
    cross = pygame.transform.scale(cross, (100,100)).convert_alpha()
    zero = pygame.image.load(r'zero.png').convert_alpha()
    zero = pygame.transform.scale(zero, (100,100)).convert_alpha()
except:
    screen.fill(background_colour)
    screen.blit(special_font.render("Some files are missed!",1,(3,52,212), (180,205,205)),(30,150))
    screen_refresh()
    time.sleep(2)
    quit()

# Initializing audio player, and creating object of "game_tools_and_variables" class
pygame.mixer.init()
Game = game_tools_and_variables(100,100, 10)

# Starting game loop
while True:
# Inisializing eventlistener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
# Getting mouse coordinates 
            x_mouse, y_mouse = pygame.mouse.get_pos()
# Some playing field's areas are passive(don't work like buttons)
            if x_mouse%110>=10 and y_mouse%110>=10 :
# If player clicked button, we have to decide which one and change turn 
                Game.zero_turn= not Game.zero_turn
                determinated_column= x_mouse//(Game.margin+Game.width)
                determinated_row= y_mouse//(Game.margin+Game.height)
# If player clicke button which was activated before, we don't want to change turn
                if Game.matrix[determinated_row][determinated_column]!=0:
                    Game.zero_turn= not Game.zero_turn
                elif Game.continue_of_game:
# For zeros we use "-1", for crosses: "1"
# we need to decide, what should be in certain playarea, and decrement free_place varuable   
                    if Game.zero_turn:
                        Game.matrix[determinated_row][determinated_column]=1
                        Game.free_place-=1
                        try:
                            pygame.mixer.music.load("Cross sound.wav")
                            pygame.mixer.music.play()
                        except: 
                            pass
                    else:
                        Game.matrix[determinated_row][determinated_column]=-1
                        Game.free_place-=1
                        try:
                            pygame.mixer.music.load("Zero sound.wav")
                            pygame.mixer.music.play()
                        except: 
                            pass
            
#After game ended, we want to restart it, by clicking on the button,
#so we need to set matrix, sizes, initial values of variables again 
# Moreover, we have to stop music playing    
            if not Game.continue_of_game and  18<=x_mouse<321 and  240<=y_mouse<272:
                Game.restart()
                screen.fill((0,0,0))
                pygame.mixer.music.unload()   
#The main part        
    if Game.continue_of_game:
        for row in range(3):
# The main idea, is to calculate the sum in the corresponding rows
# If the absolute value = 3, the game ended. 
# Negative number: zero won , positive: cross won
            Game.nullify_sums()
            for column in range(3):
# Calculating coordinates, where picture should be painted
                x=column*Game.width+(column+1)*Game.margin
                y=row*Game.height+(row+1)*Game.margin
# Our screen is black, so we paint white squares, to show, that some areas are active
# We painting zeros and crosses on the areas, while game keep going
                if Game.matrix[row][column]== 1 :
                    screen.blit(cross, (x, y))
                elif Game.matrix[row][column]== -1 :
                    screen.blit(zero, (x, y))
                else:  
                    pygame.draw.rect(screen,(255,255,255),(x,y,Game.width, Game.height))
# While in the loop, we calculate sums in the each row and column
                Game.sum_in_row += Game.matrix[row][column]
                Game.sum_in_column += Game.matrix[column][row]
# We need to take into account the sums in diagonals
                Game.sum_diagonal += Game.matrix[column][column]
                Game.sum_antidiagonal += Game.matrix[2-column][column]
                Game.all_sums=[ Game.sum_in_row,  Game.sum_in_column,  Game.sum_diagonal,  Game.sum_antidiagonal]
# Here we checking if value of sum in any row is equall 3 or -3
# If so, we end our game, proclame winner and enable finall cutscene
#````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
# "win_line" variable working next way: if "sum_in_row" = 3, "win_line" say to us in which ROW (0,1 or 2) that occurred
# At the same time, if "sum_in_column" = 3, "win_line" say to us in which COLUMN (0,1 or 2) that occurred
#``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
# All sumes are registered in the "all_sums" variable in the appropriate order. 
# So "line_type" would just find where is "3" (or "-3") in that list. So, we would know what type the winning line is
                if 3 in Game.all_sums:
                    caption=caption_cross_won
                    Game.game_end()
                    Game.win_line=row
                    Game.line_type = Game.all_sums.index(3)
                elif -3 in Game.all_sums:
                    caption=caption_zero_won
                    Game.game_end()
                    Game.win_line=row
                    Game.line_type = Game.all_sums.index(-3)
# If we run out of free place and still nobody won, we proclame draw and end game 
# There is no winning line in that case, so "win_line" and "line_type" would stay None type
                elif Game.free_place==0 :
                    caption=caption_nobody_won
                    Game.game_end()
    else:
# Running cutscene
        if Game.ending:
            Game.draw_win_line()
            time.sleep(0.6)
# Running speciall music, while second screen is active
            try:
                pygame.mixer.music.load("Game_end sound.mp3")
                pygame.mixer.music.play(loops=-1)
            except: 
                pass
            Game.ending=False
# Creating anouther screen, using which we could restart game
# Our captions could have different widht, so we have to calculate it, to place caption in the center 
        screen.fill(background_colour)
        caption_width= caption.get_width()
        screen.blit(caption,((340-caption_width)//2,100))
        screen.blit(caption_restart,(18,240))
# To make all printed objects visible
    screen_refresh()
            
      