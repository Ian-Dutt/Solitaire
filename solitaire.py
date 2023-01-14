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
        self.seen = False

    def __repr__(self) -> str:
        return f'{self.value} of {self.suit}\'s'

spades = [Card(f'Cards\\{i}_of_spades.png', 'spade', i) for i in range(2, 11)]
hearts = [Card(f'Cards\\{i}_of_hearts.png', 'heart', i) for i in range(2, 11)]
diamonds = [Card(f'Cards\\{i}_of_diamonds.png', 'diamond', i) for i in range(2, 11)]
clubs = [Card(f'Cards\\{i}_of_clubs.png', 'club', i) for i in range(2, 11)]
pg.display.set_caption('Solitaire')

for i in range(11,14):
    spades.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_spades.png', 'spade', i))
    diamonds.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_diamonds.png', 'diamond', i))
    hearts.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_hearts.png', 'heart', i))
    clubs.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_clubs.png', 'club', i))
spades.append(Card(f'Cards\\ace_of_spades.png', 'spade', 1))
hearts.append(Card(f'Cards\\ace_of_hearts.png', 'hearts', 1))
diamonds.append(Card(f'Cards\\ace_of_diamonds.png', 'diamonds', 1))
clubs.append(Card(f'Cards\\ace_of_clubs.png', 'clubs', 1))
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
            deck)

def is_card(pos, card):
    return pos[0] < card.pos[0] + CARD_WIDTH and pos[0] > card.pos[0] and card.pos[1] < pos[1] + CARD_HEIGHT and card.pos[1] > pos[1]


# This checks if the given position is on one of the cards in the 7 piles
# It returns the index of the stack and the number of cards that are going to be moved

def is_on_card_row(win, pos, stacks):
    if win.get_at(pos) == pg.Color(GREEN): return None, 0
    print('1')
    if pos[0] > 7.875*CARD_WIDTH + 15: return None, 0
    print('  2')
    index = 0
    offset = 0
    check = 0
    for i in range(8):
        check = offset*CARD_WIDTH + 15
        if pos[0] < check:
            break
    
        index = i
        offset += 1.125
    
    if pos[1] > DISTANCE_FROM_TOP:
        from_top = pos[1] - DISTANCE_FROM_TOP
        num_cards = len(stacks[index]) + 1
        for i in range(len(stacks[index])):
            if from_top < i*25:
                break
            num_cards -= 1
        # print('Distance from top:', num_cards)
        return index, num_cards
    print('   3')
    return None, 0


def show_deck(win):
    pos = ((WIDTH - CARD_WIDTH - 15), + DISTANCE_FROM_TOP)
    win.blit(CARD_BACK, pos)
    pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)


def show_revealed(win, revealed):

    for i in range(len(revealed)):
        if(i < 3):
            pos = (WIDTH - 2.5* CARD_WIDTH - 20*i, DISTANCE_FROM_TOP)
            win.blit(revealed[i].pic, pos)
            pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)

def show_stack(win, stack, offset):
    if not stack: return

    l = len(stack)
    for i in range(l):
        pos = (offset*CARD_WIDTH + 15,i*25 + DISTANCE_FROM_TOP)

        if not stack[i].seen:
            win.blit(CARD_BACK, pos)
        else:
            win.blit(stack[i].pic, pos)
        pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)

def can_place_card(to_add, stack_top):
    if stack_top == []: 
        return to_add.value == 13
    return to_add.suit != stack_top.suit and to_add.value == stack_top.value - 1

def blit_background(win, stacks, revealed):
    win.fill(GREEN)
    for i in range(len(stacks) - 1):

        show_stack(win, stacks[i], i*1.125)
    show_deck(win)
    show_revealed(win, revealed)


def get_cards(stacks, index, num):
    if stacks[index]:
        cards = []

        for i in range(-num, 0):
            cards.append(stacks[index].pop(i))
            # card.seen = True
        return cards
    return None

def add_cards(l, to_add):
        l.extend(to_add)


def move_card(win, pos, card, stacks, revealed):
    blit_background(win, stacks, revealed)

    win.blit(card.pic, (pos[0] - 37, pos[1] - 15))
    card.pos = pos
    card.seen = True
    pg.display.update()
    return card.pos

def move_cards(win, pos, cards, stacks, revealed):
    blit_background(win, stacks, revealed)

    for i, card in enumerate(cards):

        win.blit(card.pic, (pos[0] - 37, pos[1] - 15 + i*25))
    
    cards[0].pos = pos
    pg.display.update()
    return None

def move(win, pos, cards, stacks, revealed):
    if len(cards) > 1:
        return move_cards(win, pos, cards, stacks, revealed)
    else:
        return move_card(win, pos, cards[0], stacks, revealed)


def main(WIDTH, HEIGHT, WIN):
    # stacks = shuffle_deck(deck)
    stacks = [[spades[11]],[spades[0]],[spades[1]],[spades[12]], [hearts[0]], [spades[1]], []]
    for i in range(len(stacks) - 1):   
        stacks[i][-1].seen = True
    revealed = []
    blit_background(WIN, stacks, revealed)
    card = None
    index = None
    while True:
        
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if pg.mouse.get_pressed()[0]:
                mouse_position = pg.mouse.get_pos()
                
                try:
                    # move_card(WIN, pg.mouse.get_pos(), stacks, 1)
                    if not card:
                        index, num = is_on_card_row(WIN, mouse_position, stacks)

                        if index is not None:
                            card = get_cards(stacks, index, num)

                    else:
                        move(WIN, mouse_position, card, stacks, revealed)

                except AttributeError:
                    pass
            if not pg.mouse.get_pressed()[0]:
                if card:
                    new_index, _ = is_on_card_row(WIN, card[0].pos, stacks)
                    print(new_index)
                    try:
                        stack_top = stacks[new_index][-1]
                    except Exception:
                        stack_top = []

                    if new_index is not None:
                        
                        if can_place_card(card[0], stack_top):
                            if new_index != index and stacks[index]:
                                stacks[index][-1].seen = True

                            add_cards(stacks[new_index], card)
                            blit_background(WIN, stacks, revealed)
                            card = None
                            print(f'Placed card in stack {index + 1}')
                        else:
                            add_cards(stacks[index], card)
                            card = None
                            blit_background(WIN, stacks, revealed)
                            print('Cant place card there')
                    else:
                        add_cards(stacks[index], card)
                        card = None
                        blit_background(WIN, stacks, revealed)
                        print('Cant place card there')



        pg.display.update()
main(WIDTH, HEIGHT, WIN)