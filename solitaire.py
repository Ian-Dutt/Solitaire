import sys
import pygame as pg
import random

WIDTH = 1200
HEIGHT = 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))

BLACK = [0,0,0]
GREEN = [25, 200, 50]

CARD_WIDTH = 94
CARD_HEIGHT = 135
DISTANCE_FROM_TOP = 250
CARD_BACK = pg.transform.scale(pg.image.load('Cards\\card_back_red.png'), (CARD_WIDTH, CARD_HEIGHT))
CARD_BACK_RECT = CARD_BACK.get_rect()
face_card = {
    'king' : 13,
    'queen' : 12,
    'jack' : 11,
    'Ace' : 14,
}

def is_red(suit):
    return (suit == 'heart' or suit == 'diamond')
class Card:
    def __init__(self, pic, suit, value, pos = (0,0)) -> None:
        self.pic = pg.image.load(pic)
        self.pic = pg.transform.scale(self.pic, (CARD_WIDTH, CARD_HEIGHT))
        self.pos = pos
        self.suit = suit
        self.value = value if isinstance(value, int) else face_card.get(value)

    def __repr__(self) -> str:
        return f'{self.value} of {self.suit}\'s'

spades = [Card(f'Cards\\{i}_of_spades.png', 'spade', i) for i in range(2, 11)]
hearts = [Card(f'Cards\\{i}_of_hearts.png', 'heart', i) for i in range(2, 11)]
diamonds = [Card(f'Cards\\{i}_of_diamonds.png', 'diamond', i) for i in range(2, 11)]
clubs = [Card(f'Cards\\{i}_of_clubs.png', 'club', i) for i in range(2, 11)]
pg.display.set_caption('Solitaire')

for i in range(11,15):
    spades.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_spades.png', 'spade', i))
    diamonds.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_diamonds.png', 'diamond', i))
    hearts.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_hearts.png', 'heart', i))
    clubs.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_clubs.png', 'club', i))

WIN.fill(GREEN)

deck = spades + hearts + diamonds + clubs

def shuffle_deck(deck):
    random.shuffle(deck)

    return ([deck.pop(0)], [deck.pop(0), deck.pop(0)], 
            [deck.pop(0), deck.pop(0), deck.pop(0)], 
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            deck)



def show_deck(win):
    pos = ((WIDTH - CARD_WIDTH - 15), + DISTANCE_FROM_TOP)
    win.blit(CARD_BACK, pos)
    pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)


def show_revealed(win, revealed):
    rev = revealed[::-1]
    for i in range(len(revealed)):
        if(i < 3):
            pos = (WIDTH - 2.5* CARD_WIDTH - 30*i, DISTANCE_FROM_TOP)
            win.blit(revealed[i].pic, pos)
            pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)

def show_stack(win, stack, offset):
    l = len(stack)
    for i in range(l):
        pos = (offset*CARD_WIDTH + 15,i*20 + DISTANCE_FROM_TOP)
        if i < l - 1:
            win.blit(CARD_BACK, pos)
        else:
            win.blit(stack[-1].pic, pos)
        pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)



def blit_background(win, stacks, revealed):
    win.fill(GREEN)
    for i in range(len(stacks) - 1):
        show_stack(win, stacks[i], i*1.125)
    show_deck(win)
    show_revealed(win, revealed)


def move_card(win, pos, stacks, index, revealed):
    card = stacks[index][-1]

    blit_background(win, stacks, revealed)

    win.blit(card.pic, (pos[0] - 37, pos[1] - 67))
    pg.display.update()
    return card.pos





def main(WIDTH, HEIGHT, WIN):
    stacks = shuffle_deck(deck)
    for i in range(len(stacks)):
        
        print(len(stacks[i]))
    revealed = [stacks[0][0], stacks[1][1], stacks[2][2], stacks[3][3]]
    blit_background(WIN, stacks, revealed)

    clicked = None
    while True:
        
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if pg.mouse.get_pressed()[0]:
                try:
                    # move_card(WIN, pg.mouse.get_pos(), stacks, 1)
                    
                    clicked = (pg.mouse.get_pos())
                    print(clicked)
                except AttributeError:
                    pass
            if not pg.mouse.get_pressed()[0]:
                
                clicked = None
                print(clicked)

        pg.display.update()
main(WIDTH, HEIGHT, WIN)