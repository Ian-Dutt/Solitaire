import sys
import pygame as pg
import random

WIDTH = 1200
HEIGHT = 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))

BLACK = [0,0,0]
GREEN = [25, 200, 50]

DECK = True

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

DECK = spades + hearts + diamonds + clubs

def shuffle_deck(deck):
    random.shuffle(deck)

    return ([deck.pop(0)], [deck.pop(0), deck.pop(0)], 
            [deck.pop(0), deck.pop(0), deck.pop(0)], 
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            [deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0), deck.pop(0)],
            deck)


# This checks if the given position is on one of the cards in the 7 piles
# It returns the index of the stack and the number of cards that are going to be moved

def is_on_card_row(win, pos, stacks):
    if win.get_at(pos) == pg.Color(GREEN): return None, 0

    if pos[0] > 7.875*CARD_WIDTH + 15: return None, 0

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
        from_top = pos[1] - DISTANCE_FROM_TOP - 25
        num_cards = 0

        for i in range(len(stacks[index])):
            if i == len(stacks[index]) - 1:
                num_cards += 1
            elif stacks[index][i].seen:
                print(from_top, i)
                if from_top < 25 * (i):
                    if from_top < 25 * (i-1): return None, 0
                    num_cards += 1

        return index, num_cards

    return None, 0


def show_deck(win, deck):
    pos = ((WIDTH - CARD_WIDTH - 15), + DISTANCE_FROM_TOP)
    if deck:
        win.blit(CARD_BACK, pos)
        pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)
    else:
        pg.draw.rect(WIN, (50,50,50), pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)))


def show_revealed(win, revealed):
    for i in range(-3, 0):
        try:
            pos = (WIDTH - 2* CARD_WIDTH + 20*i, DISTANCE_FROM_TOP)
            win.blit(revealed[i].pic, pos)
            pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)
        except IndexError:
            break


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
    return is_red(to_add.suit) != is_red(stack_top.suit) and to_add.value == stack_top.value - 1


def blit_background(win, stacks, revealed, deck):
    win.fill(GREEN)
    for i in range(len(stacks) - 1):

        show_stack(win, stacks[i], i*1.125)
    show_deck(win, deck)
    show_revealed(win, revealed)


def get_cards(stacks, index, num):
    if stacks[index]:
        cards = []

        for i in range(-num, 0):
            print(i)
            cards.append(stacks[index].pop(i))
            # card.seen = True
        return cards
    return None


def add_cards(l, to_add):
        l.extend(to_add)


def move_card(win, pos, card, stacks, revealed, deck):
    blit_background(win, stacks, revealed, deck)

    win.blit(card.pic, (pos[0] - 37, pos[1] - 15))
    card.pos = pos
    card.seen = True
    pg.display.update()
    return card.pos


def move_cards(win, pos, cards, stacks, revealed, deck):
    blit_background(win, stacks, revealed, deck)

    for i, card in enumerate(cards):

        win.blit(card.pic, (pos[0] - 37, pos[1] - 15 + i*25))
    
    cards[0].pos = pos
    pg.display.update()
    return None


def move(win, pos, cards, stacks, revealed, deck):
    if len(cards) > 1:
        return move_cards(win, pos, cards, stacks, revealed, deck)
    else:
        return move_card(win, pos, cards[0], stacks, revealed, deck)


### TODO MAKE IT SO WHEN THE DECK IS CLICKED ON IT FLIPS OVER THREE CARDS

def between(pos, upperx, uppery, lowerx, lowery):
    return pos[1] < lowery and pos[1] > uppery and pos[0] < lowerx and pos[0] > upperx


def choose_action(pos):
    if between(pos, (WIDTH - 15 - CARD_WIDTH), DISTANCE_FROM_TOP, (WIDTH - 15), (DISTANCE_FROM_TOP + CARD_HEIGHT)):
        return 'deck'
    elif between(pos, 15, DISTANCE_FROM_TOP, HEIGHT, 755):
        return 'stacks'
    elif between(pos, WIDTH - 2.5*CARD_WIDTH + 40, DISTANCE_FROM_TOP, WIDTH - CARD_WIDTH + 40, DISTANCE_FROM_TOP - CARD_HEIGHT):
        return 'revealed'
    # elif between(pos, )
    else:
        return None


def main(WIDTH, HEIGHT, WIN):
    deck = DECK
    stacks = shuffle_deck(deck)
    # stacks = [[spades[11]],[spades[0]],[spades[1]],[spades[12]], [hearts[0]], [spades[1]], []]
    for i in range(len(stacks) - 1):   
        stacks[i][-1].seen = True
    revealed = []
    deck.pop(-1)
    blit_background(WIN, stacks, revealed, deck)
    card = None
    index = None
    flip_cards = False
    num_to_flip = 3
    while True:
        
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if pg.mouse.get_pressed()[0]:
                mouse_position = pg.mouse.get_pos()

                try:
                    action = choose_action(mouse_position)
                    if action == 'stacks' or card:
                        if not card:
                            index, num = is_on_card_row(WIN, mouse_position, stacks)
                            if index is not None:
                                card = get_cards(stacks, index, num)
                                move(WIN, mouse_position, card, stacks, revealed, deck)
                        else:
                            move(WIN, mouse_position, card, stacks, revealed, deck)
                    elif action == 'deck':    
                        flip_cards = True
                    elif action == 'revealed':
                        print('Hey there')

                except AttributeError:
                    pass
            if not pg.mouse.get_pressed()[0]:
                if flip_cards:
                    if deck:
                        for i in range(len(deck)):
                            if i < 3:
                                revealed.append(deck.pop(0))
                        blit_background(WIN, stacks, revealed, deck)
                    else:
                        deck = revealed
                        revealed = []
                        blit_background(WIN, stacks, revealed, deck)
                    flip_cards = False
                elif card:
                    new_index, _ = is_on_card_row(WIN, card[0].pos, stacks)
                    try:
                        stack_top = stacks[new_index][-1]
                    except Exception:
                        stack_top = []

                    if new_index is not None:
                        
                        if can_place_card(card[0], stack_top):
                            if new_index != index and stacks[index]:
                                stacks[index][-1].seen = True

                            add_cards(stacks[new_index], card)
                            blit_background(WIN, stacks, revealed, deck)
                            card = None
                            print(f'Placed card in stack {new_index + 1}')
                        else:
                            add_cards(stacks[index], card)
                            card = None
                            blit_background(WIN, stacks, revealed, deck)
                            print('Cant place card there')
                    else:
                        add_cards(stacks[index], card)
                        card = None
                        blit_background(WIN, stacks, revealed, deck)
                        print('Cant place card there')



        pg.display.update()
main(WIDTH, HEIGHT, WIN)