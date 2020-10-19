'''
CPT Game: Moby's Sick
@author Anne Chung
@date 2016/06/16
@course ICS3U1
'''

#import pygame and random libraries 
import pygame
import random

#--- spritesheet class taken from ProgramArcadeGames.com, Chapter 13
#class takes a picture and converts it into a usable picture
class SpriteSheet(object):

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    #method takes and returns a certain part of an image based on the coordinates and measurements it is given 
    def get_image (self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

#--- class incorporates ideas from ProgramArcadeGames.com, Chapter 13
#class defines the whale (main character)
class Whale(pygame.sprite.Sprite):

    def __init__(self):
        #inherits the functions of the sprite class
        super(Whale, self).__init__()

        #pixels that the whale will move by 
        self.x_change = 0
        self.y_change = 0
        #this concept of switching in between images in a list to animate was taken from ProgramArcadeGames, Chapter 13
        #this concept was incorporated into all of my classes to animate them
        #--- ProgramArcadeGames work begins here
        
        #all of the different images of the whale are stored here
        self.walking_frames_l = []
        self.walking_frames_r = []
        #variable that determines which image in the list will be shown
        self.framechange = 0
        #direction the object is facing 
        self.direction = "R"

        #runs the spritesheet Moby.png through the SpriteSheet class
        sprite_sheet = SpriteSheet("Moby.png")
        #takes different parts/images of the spritesheet and adds them to the list, whale is facing left in these frames
        image = sprite_sheet.get_image(0, 30, 160, 130)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(160, 30, 160, 130)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(320, 50, 160, 85)
        self.walking_frames_l.append(image)

        #takes the same parts but flips them so that the whale is facing right in the images 
        image = sprite_sheet.get_image(0, 30, 160, 130)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(160, 30, 160, 130)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(320, 50, 160, 85)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_r.append(image)

        #sets the image of the object, whale starts facing right 
        self.image = self.walking_frames_r[0]
        #stores the coordinates of where the image of the whale is drawn on the screen
        self.rect = self.image.get_rect()

        # --- ProgramArcadeGames.com work ends here
        
    #method updates the movement of the whale and makes the x and y coordinates move according to the actions
    def update(self, loop, hp_level):
        #the changes are added to the coordinates of the whale's position to make it move across the screen
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        #if the whale is not dead, this code will run 
        if hp_level.length > 0:
            #this code will run if whale is facing right
            if self.direction == "R":
                self.image = self.walking_frames_r[self.framechange]
                #switches in between the different images in the list to make whale seem as if it is moving 
                if self.framechange == 0 and loop % 15 == 0:
                    self.framechange = 1
                elif self.framechange == 1 and loop % 15 == 0:
                    self.framechange = 0
            #this code will run if whale is not facing right (facing left)
            else:
                self.image = self.walking_frames_l[self.framechange]

                if self.framechange == 0 and loop % 15 == 0:
                    self.framechange = 1
                elif self.framechange == 1 and loop % 15 == 0:
                    self.framechange = 0

            #makes sure the whale does not go out of the water or off screen
            if self.rect.y <= 300 or self.rect.y >= 600:
                self.y_change = 0
            if self.rect.x <= 0 or self.rect.x >= 1200:
                self.x_change = 0

    #--- these methods were also taken from ProgramArcadeGames
    #makes whale move left
    def go_left(self):
        self.x_change = -6
        self.direction = "L"

    #method makes whale move right
    def go_right(self):
        self.x_change = 6
        self.direction = "R"

    #makes whale move up 
    def go_up(self):
        self.y_change = -3

    #makes whale move down
    def go_down(self):
        self.y_change = 3
    #--- original work begins again

    #stops the changes to the y coordinates to make the whale stop moving 
    def stop_up_down(self):
        self.y_change = 0

    #stops the changes to the x coordinates
    def stop_right_left(self):
        self.x_change = 0

    #makes whale sink
    def sink(self):
        self.y_change = 3
        #runs if whale is facing right
        if self.direction == "R":
            self.image = self.walking_frames_r[2]
        else:
            self.image = self.walking_frames_l[2]

#defines the enemies of the whale 
class Boat(pygame.sprite.Sprite):

    def __init__(self):
        super(Boat, self).__init__()

        #list of the different boat spritesheets
        boat_pics = ["Boat1.png", "Boat2.png", "Boat3.png", "boat4.png"]
        #randomly generated number determines how quickly boat will attack whale
        self.speed = random.randrange(20, 80, 10)
        #randomly generated number determines which boat_pic will be used
        self.pic_index = random.randint(0, 3)

        #uses same concept as the whale to switch in between images for animation
        self.walking_frames = []
        self.framechange = 0
        #determines how quickly the images will be switched 
        self.switch_speed = 20

        boat_sheet = SpriteSheet(boat_pics[self.pic_index])
        image = boat_sheet.get_image(0, 0, 160, 160)
        self.walking_frames.append(image)
        image = boat_sheet.get_image(160, 0, 160, 160)
        self.walking_frames.append(image)

        #sets the image that will be drawn onto the screen
        self.image = self.walking_frames[0]
        #stores the coordinates of where the image is drawn on the screen at all times 
        self.rect = self.image.get_rect()
        #makes the boat appear at a random spot 
        self.rect.x = random.randint(700, 10000)
        self.rect.y = random.randint(100, 150)

    #switches the images that are shown to animate the boat 
    def update(self, loop):
        self.image = self.walking_frames[self.framechange]

        if self.framechange == 0 and loop % self.switch_speed == 0:
            self.framechange = 1
        elif self.framechange == 1 and loop % self.switch_speed == 0:
            self.framechange = 0

#objects that inflict damage on the whale when they hit the whale
class Anchor(pygame.sprite.Sprite):

    def __init__(self, boat):
        super(Anchor, self).__init__()
        
        anchor_image = SpriteSheet("Anchor.png")
        self.image = anchor_image.get_image(0, 0, 32, 32)

        self.x_change = 0
        self.y_change = 6
        self.rect = self.image.get_rect()
        #image of anchor will be drawn at the center of each boat
        self.rect.x = boat.rect.center[0]
        self.rect.y = boat.rect.center[1]
        #stores the position of the whale on the screen 

    #makes changes to the x and y coordinates of each anchor to make it move across screen
    def update(self, moby):
        #depending on where the whale is compared to the boat, the anchor will move differently
        if -600 <= (moby.rect.x - self.rect.x) < 0:
            self.x_change = -8
        elif (moby.rect.x - self.rect.x) == 0:
            self.x_change = 0
        elif 0 < (moby.rect.x - self.rect.x) <= 600:
            self.x_change = 8

        self.rect.x += self.x_change
        self.rect.y += self.y_change

#objects that whale uses to hit boats
class Weapon_Can(pygame.sprite.Sprite):

    def __init__(self, moby):
        super(Weapon_Can, self).__init__()

        can_image = SpriteSheet("weaponcan.png")
        self.image = can_image.get_image(0, 0, 18, 29)
        self.x_change = 0
        self.y_change = -6
        self.rect = self.image.get_rect()
        #makes the coordinates at which object is drawn equal to the x and y coordinates of the center of the whale 
        self.rect.x = moby.rect.center[0]
        self.rect.y = moby.rect.center[1]

    #makes changes to the x and y coordinate of the can image
    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    #each of the next methods sets how many pixels the picture will move across the screen
    #for when can is sent to the right
    def go_right(self):
        self.x_change = 5

    #for when can is sent to the left
    def go_left(self):
        self.x_change = -5
        
    #for when can is sent upwards
    def go_up(self):
        self.x_change = 0

#objects that whale will eat to restore HP
class Fish(pygame.sprite.Sprite):

    def __init__(self):

        #inherits from sprite class
        super(Fish, self).__init__()

        fish_image = SpriteSheet("fish.png")
        self.image = fish_image.get_image(0, 0, 64, 30)
        self.rect = self.image.get_rect()
        #randomizes x and y coordinates of fish, to place them randomly all over the game
        self.rect.x = random.randint(500, 10000)
        self.rect.y = random.randint(350, 700)

#the health points of the whale; when the HP_level reaches 0, the whale will die
class HP_Level():

    def __init__(self):
        self.color = GREEN
        self.length = 100

    #draws the HP_level indicator to the screen
    def draw(self, screen):
        #draws the bar inside of the border
        pygame.draw.rect(screen, self.color, (1000, 50, self.length, 30), 0)
        #draws the border 
        pygame.draw.rect(screen, BLACK, (1000, 50, 100, 30), 3)

    #changes the length of the rectangle to show different HP_levels 
    def update(self, anchors_hit, fish_collected):
        #length will become shorter when whale is hit by an anchor, longer when it collects fish
        self.change = len(fish_collected)*10 - len(anchors_hit)*10
        self.length += self.change

        #makes 100 the highest possible number of health points to own
        if self.length > 100:
            self.length = 100
        #changes color of the hp indicator to red when at a low number of health points
        if self.length < 20:
            self.color = RED
        #makes 0 the minimum number of points
        if self.length < 0:
            self.length = 0

#draws the background of the game
#---Setting class taken from ProgramArcadeGames.com, Chapter 13
class Setting():

    def __init__(self):

        #sets the sky background
        self.sky_background = pygame.image.load("sky_background.png").convert()
        self.sky_background.set_colorkey(WHITE)
        #sets the water background
        self.water_background = pygame.image.load("water_background.png").convert()
        self.water_background.set_colorkey(WHITE)
        #sets the instruction image
        self.instructions = pygame.image.load("instructions.png").convert()
        self.instructions.set_colorkey(WHITE)
        #sets the start and end flag
        start_flag = SpriteSheet("startflag.png")
        self.start_flag = start_flag.get_image(0, 0, 320, 320)
        end_flag = SpriteSheet("endflag.png")
        self.end_flag = end_flag.get_image(0, 0, 320, 320)

        #the shift will determine how the background is moved as the player gets to the end of the screen 
        self.shift = 0
        #the x coordinate of where the game will end 
        self.limit = 10500

    #draws the water, start and end flags
    def draw_water(self, screen):
        #coordinates of the background moves with the shift 
        screen.blit(self.water_background, (self.shift, 0))
        screen.blit(self.water_background, (self.shift + 3150, 0))
        screen.blit(self.water_background, (self.shift + 6300, 0))
        screen.blit(self.water_background, (self.shift + 9450, 0))
        screen.blit(self.end_flag, (11000 + self.shift, 380))
        screen.blit(self.start_flag, (30 + self.shift, 380))

    #draws the sky, which will be behind the water 
    def draw_sky(self, screen):
        #shift is smaller, so that the sky background moves more slowly than the water
        screen.blit(self.sky_background, (self.shift // 3, 0))
        screen.blit(self.instructions, (50 + self.shift // 3, 20))

    #changes the x-coordinate of the background images as the main character moves 
    def update(self, shift):
        self.shift -= shift

#shows the player what their score and number of cans remaining is 
def Draw_Score(screen, score, weaponcan_number):
    #sets font and the text that will be blitted 
    font = pygame.font.SysFont('Calibri', 20, True, False)
    score_text = font.render("SCORE: " + str(score), True, BLACK)
    weapon_limit_text = font.render("CANS LEFT: " + str(weaponcan_number), True, BLACK)
    #blits the text
    screen.blit(score_text, [1000, 100])
    screen.blit(weapon_limit_text, [1000, 130])

#what shows up on the screen when player wins
def Game_Win(score, screen):
    font = pygame.font.SysFont('Calibri', 100, True, False)
    end_text = font.render("YOU WON", True, BLACK)
    score_text = font.render("SCORE:" + str(score), True, BLACK)
    screen.blit(end_text, [250, 250])
    screen.blit(score_text, [250, 500])

#what shows up on the screen when player loses
def Game_Lose(score, screen):
    font = pygame.font.SysFont('Calibri', 100, True, False)
    end_text = font.render("GAME OVER", True, BLACK)
    score_text = font.render("SCORE:" + str(score), True, BLACK)
    screen.blit(end_text, [250, 250])
    screen.blit(score_text, [250, 500])                 

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (132, 255, 0)
RED = (255, 0, 0)
screen_height = 700
screen_width = 1200

#main program
def main():

    #calls pygame
    pygame.init()

    #creates the screen based on the screen heigh and screen width variables
    screen = pygame.display.set_mode((screen_width, screen_height))

    #sets a variable to keep track of the number of times the program has looped 
    loop = 0
    #variable used to keep track of the score
    score = 0
    #the limit of cans that the player can shoot 
    weaponcan_number = 50

    #creates lists for all of the moving objects in the game
    player_list = pygame.sprite.Group()
    weaponcan_list = pygame.sprite.Group()
    boat_list = pygame.sprite.Group()
    anchor_list = pygame.sprite.Group()
    fish_list = pygame.sprite.Group()

    #creates the player
    moby = Whale()
    #the coordinates where the whale begins on the screen
    moby.rect.x = 70
    moby.rect.y = 530
    #creates a list for the player and adds the whale 
    player_list.add(moby)
        
    #will run 25 times
    for i in range (25):
        #creates boat
        boat = Boat()
        #adds boat to the sprite group 
        boat_list.add(boat)

    #creates 20 fish 
    for i in range(20):
        fish = Fish()
        #adds each fish to the sprite group
        fish_list.add(fish)

    #creates the hp_level 
    hp_level = HP_Level()
    #creates the setting that will be drawn using coordinates of the whale
    setting = Setting()
    
    done = False
    #creates an object to track the time
    clock = pygame.time.Clock()

    #MAIN PROGRAM LOOP

    #will run as long as done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            #will run if whale still has health points
            if hp_level.length != 0:
                #controls the movement of the player
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moby.go_left()
                    elif event.key == pygame.K_RIGHT:
                        moby.go_right()
                    elif event.key == pygame.K_UP:
                        moby.go_up()
                    elif event.key == pygame.K_DOWN:
                        moby.go_down()

                    #controls movement of the player's weapons
                    #will only run if weapon limit has not been reached
                    if weaponcan_number > 0:
                        if event.key == pygame.K_d:
                            weaponcan = Weapon_Can(moby)
                            weaponcan_list.add(weaponcan)
                            weaponcan.go_right()
                            #each time a weapon is created, 1 is subtracted from the number of available weapons
                            weaponcan_number -= 1
                        elif event.key == pygame.K_a:
                            weaponcan = Weapon_Can(moby)
                            weaponcan_list.add(weaponcan)
                            weaponcan.go_left()
                            weaponcan_number -= 1
                        elif event.key == pygame.K_w:
                            weaponcan = Weapon_Can(moby)
                            weaponcan_list.add(weaponcan)
                            weaponcan.go_up()
                            weaponcan_number -= 1

            #stops the movement of the player when key is released
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    moby.stop_right_left()
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    moby.stop_up_down()

        #runs if whale still has health points
        if hp_level.length > 0:
            #creates an anchor for every boat 
            for boat in boat_list:
                #runs every certain number of program loops (different for every boat)
                if loop % boat.speed == 0:
                    #only creates anchor if whale is 600 px away from boat 
                    if 0 < (moby.rect.x - boat.rect.x) < 600 or 0 < (boat.rect.x - moby.rect.x) < 600:
                        anchor = Anchor(boat)
                        anchor_list.add(anchor)
                        
        #remove anchor from the list if they reach the ground
        for anchor in anchor_list:
            if anchor.rect.y == 700:
                anchor_list.remove(anchor)

        #shifts the background left if the player nears the end of the screen
        #---concept of shifting the background was taken from ProgramArcadeGames, Chapter 13
        if moby.rect.right >= 800:
            #runs if end of the setting has been reached 
            if setting.shift < -setting.limit:
                shift = 0
            #runs if the end of the setting hasn't been reached 
            elif setting.shift > -setting.limit:
                shift = moby.rect.right - 800
                moby.rect.right = 800
        #--- original work begins again
            #shifts background
            setting.update(shift)
            #shifts all of the objects in the game with the screen
            for boat in boat_list:
                boat.rect.x -= shift
            for fish in fish_list:
                fish.rect.x -= shift
            for weaponcan in weaponcan_list:
                weaponcan.rect.x -= shift
            for anchor in anchor_list:
                anchor.rect.x -= shift

        #sees when an anchor and a whale collide, and removes the anchor when they collide
        anchors_hit = pygame.sprite.spritecollide(moby, anchor_list, True)

        #sees when fish and whale collide, and removes the fish when they collide
        fish_collected = pygame.sprite.spritecollide(moby, fish_list, True)

        #the score is added for each fish that collided with whale
        for fish in fish_collected:
            score += 10

        for can in weaponcan_list:
            boats_hit = pygame.sprite.spritecollide(can, boat_list, True)
            for boat in boats_hit:
                score += 50

        #the background is set as white
        screen.fill(WHITE)

        #the sky and water are drawn
        setting.draw_sky(screen)
        setting.draw_water(screen)
        #draws all of the sprites to the screen
        boat_list.draw(screen)
        anchor_list.draw(screen)
        player_list.draw(screen)
        weaponcan_list.draw(screen)
        fish_list.draw(screen)
        Draw_Score(screen, score, weaponcan_number)
        #draws the hp
        hp_level.draw(screen)

        #updates all of the sprites 
        boat_list.update(loop)
        anchor_list.update(moby) 
        player_list.update(loop, hp_level)
        weaponcan_list.update()
        #updates the hp 
        hp_level.update(anchors_hit, fish_collected)

        if setting.shift < -10500:
            moby.go_right()
            Game_Win(score, screen)

        #if the whale runs out of health points, whale will die
        if hp_level.length == 0:
            moby.sink()
            Game_Lose(score, screen)
            
        #adds 1 to loop variable each time the main program loop is run through
        loop += 1

        #limits the number of frames per program loop to 60
        clock.tick(60)

        #draws everything to the screen
        pygame.display.flip()

    #ends the program when player exits
    pygame.quit()

if __name__ == "__main__":
    main()
