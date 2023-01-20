# For me in future or anyone else going through this code. This is a game made by me, it can be optimised a lot for now. I will
# work on it further in future. I want to improve the hero hitbox and add more levels. Now let me explain the current code to you. 

# importing random mainly for picking random starting and ending coordinates for the enemy to spawn in, among other things
import random

# pygame modules are used to make this game
import pygame

# This statement is necessary for every pygame program
pygame.init()

# Window on which everything is drawn on. The values in tuple is the resolution of the window 
my_window = pygame.display.set_mode((685,486))

# The following lines from line 20 to line 27 contain the image resources. The "walkRight", "walkLeft" and "bg" are a list. For now,
# the purpose of multiple images is to create an animation.
walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'), pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'), pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'), pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'), pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]
bg = [pygame.image.load('pics/bg.png') , pygame.image.load("pics/bg2.png"), pygame.image.load("pics/bg3.png")  ]
bullet_right = pygame.image.load('pics/bullet.png')
bullet_left = pygame.image.load('pics/bullet_left.png')
wind = pygame.image.load('pics/wind.png')
hit = pygame.image.load("pics/REHit.png")
hero_hit = pygame.image.load("pics/RHit.png")

# The following lines from line 32 to line 37 are the sound resources.
# The "hero_hurt" sound was too loud compared to the other sounds, so I had to turn it down
bullet_sound = pygame.mixer.Sound("sounds/fire.mp3")
jump_sound = pygame.mixer.Sound("sounds/jump.wav")
game_over = pygame.mixer.Sound("sounds/game_over.wav")
hero_hurt = pygame.mixer.Sound("sounds/hero_hurt.wav")
hero_hurt.set_volume(0.2)
zombie_death = pygame.mixer.Sound("sounds/zombie_death.wav")

# Putting the main background music. Again, main.mp3 was too loud so I had to turn it down. 
# The .play(-1) lets us loop the music on repeat while the game is running or unless stopped by me
music = pygame.mixer.music.load("sounds/main.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# This clock will help us set the framerate later in our code
clock = pygame.time.Clock()

# This class creates our main guy
class actor():
    
    
    def __init__(self, char_x, char_y):
        self.char_x = char_x # ===========================>        x axis coordinate of the hero 
        self.char_y = char_y # ===========================>        y axis coordinate of the hero
        self.speed = 0.5 # ===============================>        the rate by which the hero coordinates changes hence speed
        self.isJump = False # ============================>        checks if hero can jump, during a jump, hero cannot jump poor guy
        self.jumpCount = 6 # =============================>        decides how far up the hero goes during the jump
        self.left = False # ==============================>        direction the hero is facing, need it to animate the hero
        self.right = False # =============================>        direction the hero is facing, need it to animate the hero
        self.walkCount = 0 # =============================>        traverse through the walkLeft and walkRight list with these indices
        self.standing = 0 # ==============================>        Show the animation if hero is not standing, if standing show one 
        #                                                          pic based on the direction the hero is facing
        self.hitbox = ((self.char_x + 32), (self.char_y + 32)) #   hero hitbox coordinates, made it on the middle of the hero
        
        self.toDie = 0 # =================================>        Counts the number of times the enemy hitbox touches the hero hitbox
        
    # Draw the hero with this function, the walking lists are traversed 3 times. As they are of 9 images, 9 times 3 is 27, if my walk
    # count is more than 27, it resets to zero. To create a smooth animation, integer division of walkCount is used and that is the 
    # index of the walking list. If standing just show one pic of the array, if moving pick a pic from the array. No matter what happens
    # keep the hero hitbox updated. This is done with line 94.

    def draw(self,my_window):
        if self.walkCount + 1 >= 27: 
            self.walkCount = 0
        if not(self.standing):
            
            if self.left:
               
                my_window.blit(walkLeft[self.walkCount//3], (self.char_x, self.char_y))
                self.walkCount += 1
            elif self.right:
                
                my_window.blit(walkRight[self.walkCount//3], (self.char_x, self.char_y)) 
                self.walkCount += 1
        else:  
            if self.right:
                
                my_window.blit(walkRight[0], (self.char_x, self.char_y))
            else:
                
                my_window.blit(walkLeft[0], (self.char_x, self.char_y))
        self.hitbox = ((self.char_x + 32), (self.char_y + 32))            
        
    # This function is called when the hero comes in contact with the enemy.
    def hit(self):
        self.toDie += 1
        hero_hurt.play()
        
# hero is an object of the actor class. The x and y coordinates are initialized                                     
hero = actor(100,320)

# bullets is a list of objects of hero_attack class
bullets = []

# This class gives the blueprint of our bullets
class hero_attack():
    def __init__(self, char_x, char_y, facing):
        self.char_x = char_x # ==============================================> The x axis coordinate of the bullet
        self.char_y = char_y # ==============================================> The y axis coordinate of the bullet
        self.facing = facing # ==============================================> facing is 1 for right and -1 for left
        self.speed = 16 * facing # ==========================================> rate of change of coordinates of the bullet
    
    # This method draws the bullet based on the direction of the hero
    
    def draw(self, my_window):
        if self.facing == 1:
            my_window.blit(bullet_right , (self.char_x, self.char_y))
        else:
            my_window.blit(bullet_left, (self.char_x, self.char_y))

# This class make the enemies we see on the screen. Again has walkRight and walkLeft list following the same logic of animation  
# The lists have 11 images and they are traversed 3 times. 3 times 11 is 33 and hence the limit of walk count. 
# The stuff that are new are mentioned as comments     
class enemy():
    walkRight = [pygame.image.load("pics/R1E.png"), pygame.image.load("pics/R2E.png"), pygame.image.load("pics/R3E.png"), pygame.image.load("pics/R4E.png"), pygame.image.load("pics/R5E.png"), pygame.image.load("pics/R6E.png"), pygame.image.load("pics/R7E.png"), pygame.image.load("pics/R8E.png"), pygame.image.load("pics/R9E.png"), pygame.image.load("pics/R10E.png"), pygame.image.load("pics/R11E.png")]
    walkLeft = [pygame.image.load("pics/L1E.png"), pygame.image.load("pics/L2E.png"), pygame.image.load("pics/L3E.png"), pygame.image.load("pics/L4E.png"), pygame.image.load("pics/L5E.png"), pygame.image.load("pics/L6E.png"), pygame.image.load("pics/L7E.png"), pygame.image.load("pics/L8E.png"), pygame.image.load("pics/L9E.png"), pygame.image.load("pics/L10E.png"), pygame.image.load("pics/L11E.png")]
    def __init__(self, char_x, char_y, end):
        self.char_x = char_x
        self.char_y = char_y
        self.end = end
        self.walkCount = 0
        self.speed = 2
        self.path = [self.char_x , self.end]  # path of the enemy, limited to the x axis
        self.hitbox = ((self.char_x + 36), (self.char_y + 12)) # hitbox of the enemy
        self.toDie = 0


    def draw(self, my_window):
        self.move() # See this method below
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.speed > 0:
            my_window.blit(self.walkRight[self.walkCount//3], (self.char_x, self.char_y))
            self.walkCount += 1   
        else:
            my_window.blit(self.walkLeft[self.walkCount//3], (self.char_x, self.char_y))
            self.walkCount += 1   
        self.hitbox = ((self.char_x + 36), (self.char_y + 12))
         
        self.speed += 0.05 # as the game goes on the enemy move faster and faster hence making the game harder with time

    # This method makes the enemy move
    def move(self):
        # speed is positive, the enemy is moving right
        if self.speed > 0:
            if self.char_x + self.speed < self.path[1]: # self.path[1] is the ending x coordinate of the enemy
                self.char_x += self.speed
            else:
                self.speed = self.speed * -1   # when the enemy reaches the end coordinate, go to opposite direction and reset walkcount
                self.walkCount = 0    
        # speed is negative, the enemy is moving left
        else:
            if self.char_x - self.speed > self.path[0]: # self.path[0] is the x coordinate of the enemy
                self.char_x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
    def hit(self):
        self.toDie += 1
                   
    # in case someone prints the enemy class object
    def __str__(self):
        print(f"{self.char_x} {self.char_y}, {self.end}")            

# bads is the list of objects of class enemy
bads = []

# name and icon of my game window
pygame.display.set_caption("Night Knight")
icon = pygame.image.load("pics/bullet.png")
pygame.display.set_icon(icon)

# draw the objects present in bads[] list with this method
def make_enemy():
   
    enemy.draw(my_window)

score = 0 # shows the count of the enemies killed by the hero

# I recommend reading the while loop below before coming and reading this draw_again function. 
def draw_again():
    global score 
    end_font = pygame.font.SysFont("Comic Sans", 85, True) # simple fonts used
    score_font = pygame.font.SysFont("Comic Sans", 17, True )
    time1 = pygame.time.get_ticks() # counting the seconds passed to animate my background.
    time1 = time1//1000 # for every even second, use 2nd pic in bg list and put wind.png in a coordinate
    if time1%2 == 0: # the elif and else blocks follow the same logic
            my_window.blit(bg[1], (0,0))
            my_window.blit(wind, (5,5))
                

    elif time1%3 == 0:
            my_window.blit(bg[2], (0,0))
            my_window.blit(wind, (10,5))    
    else:
            my_window.blit(bg[0], (0,0)) 
            my_window.blit(wind, (0,5)) 
    
    time2 = pygame.time.get_ticks() # this is to count the seconds to display game name and my name, also to spawn enemies
    time2 = time2 //1000 # after a certain time. Enemies cannot hurt the hero before the intro is over
    if time2 < 5:
        main_text = welcome_font.render("Night Knight", 1, (221,221,221))
        my_window.blit(main_text, (0,0))
    elif time2 > 5 and time2 < 8:
        name = name_font.render("By Ayush :)", 1, (221,221,221))
        my_window.blit(name, (100, 20))
        
    # draw the bullet instances
    for bullet in bullets:
        bullet.draw(my_window)    
    
    
    # do not have more than 3 enemies visible
    if len(bads) < 3:
            # the starting, ending and lane coordinates are randomised, enemies can spawn anywhere hehe
             bad_start_x = random.choice([0, 20, 50, 100, 400, 500, 600]) 
             bad_start_y = random.choice([325, 348, 336])
             bad_end = random.randint(bad_start_x,600)
             # if im starting at a bigger coordinate than my ending one then making ending one negative so i can come back
             if bad_start_x > bad_end:
                 bad_end = (-1) * bad_end
             # this if statement prevents small paths     
             if (bad_start_x - bad_end) **2 < 10_000:   
                 bad_end = bad_end + 100 
             bads.append(enemy(bad_start_x, bad_start_y, bad_end)) # add the object to bads[] list

    # if 8 seconds have passed then start spawning the enemies    
    if time2 > 9:
        for bad in bads:
            bad.draw(my_window)
    
    # this nested for loop is for the collision detection between the bullet and the enemy
    # the enemy spawns in 3 lanes. y axis coordinates 337, 348 and 360. For every lanes, the coordinates of bullet and enemy hitbox
    # are checked to be in range. The values of coordinates here are picked with hit and trial.
    for bullet in bullets:
        for bad in bads:
            
            if bad.hitbox[1] == 337:
                if (bullet.char_y) in range (334 - 17, 339 - 17):
                    if int(bad.char_x) in range(bullet.char_x, (bullet.char_x + 17)): # bullet png on x axis spans 16 pixel
                        bad.hit()
                        my_window.blit(hit, (bad.char_x, bad.char_y)) # draw the hit enemy "red" image
                        # enemy dies in 3 bullet collisions
                        if bad.toDie == 3:
                            zombie_death.play()
                            bads.pop(bads.index(bad)) # remove this enemy object from bads[] list
                            score += 1
                            zombie_death.play()
                
                        
            # the elif and else blocks follow the same logic       
            elif bad.hitbox[1] == 348:
                if (bullet.char_y) in range (345 - 20, 350 - 17):
                    if int(bad.char_x) in range(bullet.char_x, (bullet.char_x + 17)):
                        bad.hit()
                        my_window.blit(hit, (bad.char_x, bad.char_y))
                        if bad.toDie == 3:
                            zombie_death.play()
                            bads.pop(bads.index(bad))
                            score +=1
                            zombie_death.play()
                
            elif bad.hitbox[1] == 360:
                if (bullet.char_y) in range (357 - 17, 362 - 17):
                   if int(bad.char_x) in range(bullet.char_x, (bullet.char_x + 17)):
                        bad.hit()
                        my_window.blit(hit, (bad.char_x, bad.char_y))
                        if bad.toDie == 3:
                            zombie_death.play()
                            bads.pop(bads.index(bad))
                            score += 1
                            zombie_death.play()
                

        # if the bullet is inside my window, fire the bullet hell yea
        if bullet.char_x < 685 and bullet.char_x > 0:
            bullet.char_x += bullet.speed
           
        else:
            bullets.pop(bullets.index(bullet))  # else remove this hero_attack object from bullets[] list
    
    # draw the hero on the screen 
    hero.draw(my_window)
    

    # this for loop is for hero and enemy collision, works similar to enemy and bullet collision
    # time2 > 8 so the enemy can not hit the hero before the intro sequence is over
    for bad in bads:
        if bad.hitbox[1] == 337:
            if (hero.hitbox[1]) in range(349, 353):
                
                if (int(bad.hitbox[0])) in range((hero.char_x - 17), (hero.char_x + 17)) and time2 > 8:
                        hero.hit()
                        my_window.blit(hero_hit, (hero.char_x, hero.char_y))
        elif bad.hitbox[1] == 348:
            if (hero.hitbox[1]) in range(358, 366):
                
                if (int(bad.hitbox[0])) in range((hero.char_x - 17), (hero.char_x + 17)) and time2 > 8:
                    hero.hit()
                    my_window.blit(hero_hit, (hero.char_x, hero.char_y))
        elif bad.hitbox[1] == 360:
            if (hero.hitbox[1]) in range(372, 376):
                if (int(bad.hitbox[0])) in range((hero.char_x - 17), (hero.char_x + 17)) and time2 > 8:
                    hero.hit()
                    my_window.blit(hero_hit, (hero.char_x, hero.char_y))
    
     
    if keys[pygame.K_LSHIFT]:
        bullet_sound.play()
        # change the bullet direction based on the direction the hero is facing 
        if hero.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 1: # only one bullet at a time on the screen
            bullets.append(hero_attack(hero.char_x, hero.char_y, facing))


    # if hero takes 20 "hits"
    if hero.toDie > 20:  
            end_text = end_font.render("Game Over", 1, (235, 95, 65))
            my_window.blit(end_text, (100,20))
            pygame.mixer.music.stop() # stop my main music
            game_over.play() # play the game ending music

            # These bunch of lines are necessary for a pause of 3 seconds, without making my game lag
            pygame.display.flip()
            pygame.event.pump()
            pygame.time.delay(3 * 1000)
            pygame.quit()

    
    # display my score on top right
    score_displayed = score_font.render(f"Score : {score}", 1, (221,221,221))
    my_window.blit(score_displayed, (580, 15))

    # most important statement, nothing is there on screen without this one
    pygame.display.update()


# main while loop bool variable
running = True

while running:
    welcome_font = pygame.font.SysFont("Comic Sans", 85, True)
    name_font = pygame.font.SysFont("Comic Sans", 60, True)
    
    # setting my framerate to 33
    clock.tick(33) 

    # if player presses the cross on top right, the program closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # The pressed key is stored here
    keys = pygame.key.get_pressed()
    
    # these if statements are easy to understand, the range functions allows me to keep the hero on the road
    if keys[pygame.K_s] and hero.char_y in range(310, 340):
       
        hero.char_y +=3
    if hero.char_y > 350:
        hero.char_y -=3  # if hero is going off the road, bring him back upwards
    if keys[pygame.K_w] and hero.char_y in range(320, 350):
        hero.char_y -=3 
    if keys[pygame.K_a] and hero.char_x > 25: # hero should be restricted to the window
        hero.char_x -=3

        #these variables help me animate the hero in a particular direction
        hero.right = False
        hero.left = True    
        hero.standing = False
    elif keys[pygame.K_d] and hero.char_x < (685 - 25): # hero should be restricted to the window
        hero.char_x +=3
        hero.right = True
        hero.left = False
        hero.standing = False
    else:
        hero.standing = True
        hero.walkCount = 0  # the hero is standing and now the walk count is reset to 0 so he can walk again and complete the animation

    if not(hero.isJump): # hero can only jump when he is not in middle of a jump
        if hero.char_y in range(309, 360): # Jump should not make him come out of the road in either top or bottom
            if keys[pygame.K_SPACE]:
                jump_sound.play()
                hero.isJump = True
            elif hero.char_y > 320 and keys[pygame.K_w]: # if by chance after the jump he came off the road, pressing "w" should bring
                # him up
                hero.char_y -=3                    
    else: # now the hero can jump
        if hero.jumpCount >= -6: # extent of the jump
            
            make_negative = 1 # make the hero change direction when the jumpCount is 0 ie at the top most point
            if hero.jumpCount < 0: # hero is coming down
                make_negative = -1
            
            hero.char_y -= make_negative*0.5*(hero.jumpCount**2)   # quadratic formula to make the hero take the parabolic path               
            hero.jumpCount -= 1 
        else: # hero is back on ground and can jump again
            hero.isJump = False 
            hero.jumpCount = 6 # reset the jumpCount   
     
        if hero.char_y > 360: # if the hero is off the screen, bring him 6 pixels up
            hero.char_y -= 6    

    draw_again() # call the draw_again function to do the most important drawings

pygame.quit() 

        

        