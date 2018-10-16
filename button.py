import pygame

class Button:
    def __init__(self, text="", left=10, top=30, width=None, height=20, button_sprite=""):
        self.text = text
        self.left = left
        self.top = top
        self.height = height
        self.colour1 = (220, 220, 220)  # main
        self.colour2 = (100, 100, 100)  # border
        self.colour3 = (172, 220, 247)  # hover
        self.colour4 = (225, 243, 252)
        self.fontname = "Arial"
        self.fontsize = 12
        self.mouse_over = False
        self.mouse_down = False
        self.mouse = "off"
        self.clicked = False
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)
        self.text_width, self.text_height = pygame.font.Font.size(self.font, self.text)
        if width == None:
            self.width = self.text_width + 20
            self.width_type = "text"
        else:
            self.width = width
            self.width_type = "user"
        self.buttonUP = pygame.Surface((self.width, self.height))
        self.buttonDOWN = pygame.Surface((self.width, self.height))
        self.buttonHOVER = pygame.Surface((self.width, self.height))
        self.__update__()
        self.button_sprite = pygame.image.load(button_sprite)
        self.button_sprite = pygame.transform.scale(self.button_sprite, (self.width, self.height))

    def __update__(self):
        pass
        # up
        # r, g, b = self.colour1
        # self.buttonUP.fill(self.colour1)
        # pygame.draw.rect(self.buttonUP, (r+20, g+20, b+20), (0, 0, self.width, self.height/2), 0)
        # pygame.draw.line(self.buttonUP, self.colour2, (2, 0), (self.width-3, 0), 1)
        # pygame.draw.line(self.buttonUP, self.colour2, (2, self.height-1), (self.width-3, self.height-1), 1)
        # pygame.draw.line(self.buttonUP, self.colour2, (0, 2), (0, self.height-3), 1)
        # pygame.draw.line(self.buttonUP, self.colour2, (self.width-1, 2), (self.width-1, self.height-3), 1)
        # self.buttonUP.set_at((1, 1), self.colour2)
        # self.buttonUP.set_at((self.width-2, 1), self.colour2)
        # self.buttonUP.set_at((1, self.height-2), self.colour2)
        # self.buttonUP.set_at((self.width-2, self.height-2), self.colour2)
        # self.buttonUP.blit(self.font.render(self.text, False, (0, 0, 0)), ((self.width/2)-(self.text_width/2), (self.height/2)-(self.text_height/2)))
        # # hover
        # self.buttonHOVER.fill(self.colour3)
        # pygame.draw.rect(self.buttonHOVER, self.colour4, (0, 0, self.width, self.height/2), 0)
        # pygame.draw.line(self.buttonHOVER, self.colour2, (2, 0), (self.width-3, 0), 1)
        # pygame.draw.line(self.buttonHOVER, self.colour2, (2, self.height-1), (self.width-3, self.height-1), 1)
        # pygame.draw.line(self.buttonHOVER, self.colour4, (2, self.height-2), (self.width-3, self.height-2), 1)
        # pygame.draw.line(self.buttonHOVER, self.colour2, (0, 2), (0, self.height-3), 1)
        # pygame.draw.line(self.buttonHOVER, self.colour4, (1, 2), (1, self.height-3), 2)
        # pygame.draw.line(self.buttonHOVER, self.colour2, (self.width-1, 2), (self.width-1, self.height-3), 1)
        # self.buttonHOVER.set_at((1, 1), self.colour2)
        # self.buttonHOVER.set_at((self.width-2, 1), self.colour2)
        # self.buttonHOVER.set_at((1, self.height-2), self.colour2)
        # self.buttonHOVER.set_at((self.width-2, self.height-2), self.colour2)
        # self.buttonHOVER.blit(self.font.render(self.text, False, (0, 0, 0)), ((self.width/2)-(self.text_width/2), (self.height/2)-(self.text_height/2)))
        # # down
        # r, g, b = self.colour3
        # r2, g2, b2 = self.colour4
        # self.buttonDOWN.fill((r-20, g-20, b-10))
        # pygame.draw.rect(self.buttonDOWN, (r2-20, g2-20, b2-10), (0, 0, self.width, self.height/2), 0)
        # pygame.draw.line(self.buttonDOWN, self.colour2, (2, 0), (self.width-3, 0), 1)
        # pygame.draw.line(self.buttonDOWN, (r-20, g-20, b-10), (2, 1), (self.width-3, 1), 2)
        # pygame.draw.line(self.buttonDOWN, self.colour2, (2, self.height-1), (self.width-3, self.height-1), 1)
        # pygame.draw.line(self.buttonDOWN, self.colour2, (0, 2), (0, self.height-3), 1)
        # pygame.draw.line(self.buttonDOWN, (r-20, g-20, b-10), (1, 2), (1, self.height-3), 2)
        # pygame.draw.line(self.buttonDOWN, self.colour2, (self.width-1, 2), (self.width-1, self.height-3), 1)
        # self.buttonDOWN.set_at((1, 1), self.colour2)
        # self.buttonDOWN.set_at((self.width-2, 1), self.colour2)
        # self.buttonDOWN.set_at((1, self.height-2), self.colour2)
        # self.buttonDOWN.set_at((self.width-2, self.height-2), self.colour2)
        # self.buttonDOWN.blit(self.font.render(self.text, False, (0, 0, 0)), ((self.width/2)-(self.text_width/2)+1, (self.height/2)-(self.text_height/2)))

    def draw(self, surface):
        self.__mouse_check__()
        surface.blit(self.button_sprite, (self.left, self.top))

    def __mouse_check__(self):
        _1, _2, _3 = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not _1:
            self.mouse = "off"
        if mouse_x > self.left and mouse_x < self.left + self.width and mouse_y > self.top and mouse_y < self.top + self.height and not self.mouse == "down":
            self.mouse = "hover"
        if not self.mouse_down and _1 and self.mouse == "hover":
            self.mouse = "down"
            self.clicked = True
        if self.mouse == "off":
            self.clicked = False

    def click(self):
        _1, _2, _3 = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x > self.left and mouse_x < self.left + self.width and mouse_y > self.top and mouse_y < self.top + self.height and self.clicked and not _1:
            self.clicked = False
            return True
        else:
            return False

    def set_text(self, text, fontname="Arial", fontsize=None):
        self.text = text
        self.fontname = fontname
        if not fontsize == None:
            self.fontsize = fontsize
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)
        self.text_width, self.text_height = pygame.font.Font.size(self.font, self.text)
        if self.width_type == "text":
            self.width = self.text_width + 20
        self.buttonUP = pygame.Surface((self.width, self.height))
        self.buttonDOWN = pygame.Surface((self.width, self.height))
        self.buttonHOVER = pygame.Surface((self.width, self.height))
        self.__update__()

"""usage:
b = Button(params)  # create the button at start of program with chosen parameters

game loop:
    b.draw(surface_to_draw_to)  # pygame.surface.Surface()
    if b.click():  # check if the button was clicked
        do stuff for when button is clicked
"""