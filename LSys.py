from typing import List
from typing import Dict
import pygame
import math
import sys
from time import sleep
# [x] Define LSystem
# [x] Implement Sentence Generation
# [] Implement drawing

# Axiom: Initial String
# Production Rules: Change the String Iteratively
# Make geometric structures using the string


class LSystem():
    def __init__(self, axiom: str, rules: Dict[str, str], start: tuple, length: int, theta: int, ratio: float):
        self.sentence = axiom
        self.rules = rules
        self.startx = start[0]
        self.starty = start[1]
        self.x = self.startx
        self.y = self.starty
        self.length = length
        self.dtheta = math.radians(theta)
        self.theta = math.pi / 2
        self.positions = []
        self.ratio = ratio

    def __str__(self):
        return self.sentence

    def generate(self):
        self.length *= self.ratio
        self.theta = math.pi / 2 
        self.x = self.startx
        self.y = self.starty
        newSentence = ""
        for char in self.sentence:
            mapped = ""
            try:
                mapped = self.rules[char]
            except:
                mapped = char
            newSentence += mapped
        self.sentence = newSentence

    def draw(self, screen):
        color = 0
        dcolor = 255 / len(self.sentence)
        for char in self.sentence:
            if char == 'F' or char == 'G':
                x2 = self.x - self.length * math.cos(self.theta)
                y2 = self.y - self.length * math.sin(self.theta)
                pygame.draw.line(screen, (255 - color, color, 125 + color / 2), (self.x, self.y), (x2, y2))
                self.x = x2
                self.y = y2
            if char == '+':
                self.theta += self.dtheta
            if char == '-':
                self.theta -= self.dtheta
            if char == '[':
                self.positions.append({'x' : self.x, 'y' : self.y, 'theta' : self.theta})
            if char == ']':
                positions = self.positions.pop()
                self.x = positions['x']
                self.y = positions['y']
                self.theta = positions['theta']
            color += dcolor

def main():
    systemFile = sys.argv[1]
    sizeScreen = int(sys.argv[2]), int(sys.argv[3])
    start = int(sys.argv[4]), int(sys.argv[5])
    length = int(sys.argv[6])
    ratio = float(sys.argv[7])
    pygame.init()
    screen = pygame.display.set_mode(sizeScreen)
    system = None
    with open(systemFile, 'r') as f:
        axiom = f.readline()
        numRules = int(f.readline())
        rules = {}
        for i in range(numRules):
            rule = f.readline().split(' ')
            rules[rule[0]] = rule[1]
        system = LSystem(axiom, rules, start, length, int(f.readline()), ratio)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                system.draw(screen)
                system.generate()
        pygame.display.flip()
    pygame.quit()
        
if __name__ == '__main__':
    main()
