import pygame



class Button:

    def __init__(self, x_pos, y_pos, width, height, color, label, text_color,font_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.label = label

        self.text_color = text_color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        self.font = pygame.font.SysFont('cambria', font_size)
        self.text = self.font.render(self.label, True, self.text_color)
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # screen.blit(self.text, (self.x_pos+int(self.width/3), self.y_pos+int(self.height/4)))
        screen.blit(self.text, (self.x_pos, self.y_pos))


    def check_clicked(self, x_clicked , y_clicked):
        if( x_clicked >= self.x_pos 
        and x_clicked < self.x_pos + self.width
        and y_clicked >= self.y_pos
        and y_clicked < self.y_pos + self.height):
            return True
        
