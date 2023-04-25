import sys
import pygame as pg
import random
import time

pg.init()
BLACK = [0,0,0]
GREEN = [25, 200, 50]
DARK_GREEN = [50, 125, 50]
BLUE = [50, 100, 200]
GREY = [50,50,50]
WHITE = [255,255,255]

WIDTH = 1200
HEIGHT = 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))
FONT = pg.font.Font('./LDFComicSansHairline.ttf', 24)
FONT_SMALL = pg.font.Font('./LDFComicSansHairline.ttf', 24)
RESET = FONT.render('RESET', True, WHITE, BLACK)


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

NUM_TO_FLIP = 3

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

pg.display.set_caption('Solitaire')
def get_deck():
    spades = [Card(f'Cards\\{i}_of_spades.png', 'spade', i) for i in range(2, 11)]
    hearts = [Card(f'Cards\\{i}_of_hearts.png', 'heart', i) for i in range(2, 11)]
    diamonds = [Card(f'Cards\\{i}_of_diamonds.png', 'diamond', i) for i in range(2, 11)]
    clubs = [Card(f'Cards\\{i}_of_clubs.png', 'club', i) for i in range(2, 11)]


    for i in range(11,14):
        spades.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_spades.png', 'spade', i))
        diamonds.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_diamonds.png', 'diamond', i))
        hearts.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_hearts.png', 'heart', i))
        clubs.append(Card(f'Cards\\{list(face_card.keys())[list(face_card.values()).index(i)]}_of_clubs.png', 'club', i))
    spades.append(Card(f'Cards\\ace_of_spades.png', 'spade', 1))
    hearts.append(Card(f'Cards\\ace_of_hearts.png', 'heart', 1))
    diamonds.append(Card(f'Cards\\ace_of_diamonds.png', 'diamond', 1))
    clubs.append(Card(f'Cards\\ace_of_clubs.png', 'club', 1))


    return spades + hearts + diamonds + clubs

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
    # if win.get_at(pos) == pg.Color(GREEN): print(1); return None, 0
    
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
                if from_top < 25 * (i):

                    num_cards += 1
        print('Selected ', num_cards, 'cards', 'from pile', index)
        return index, num_cards

    return None, 0

## Adds card to suit pile
def can_add_to_suit(pile, to_add):
    if pile == []: return to_add.value == 1
    return pile[-1].suit == to_add.suit and pile[-1].value +1 == to_add.value
    


## Finds which suit pile the cards are on
def get_pile_index(win, pos):
    if win.get_at(pos) == pg.Color(GREEN): return None
    if not between(pos, 170, 50, 530 + CARD_WIDTH, CARD_HEIGHT + 50): return None
    index = -1
    for i in range(4):
        if pos[0] > i*120 + 170:
            index += 1
        else:
            break
    print(f'Pile {index} has been clicked on')
    return index


def show_deck(win, deck):
    pos = ((WIDTH - CARD_WIDTH - 15), + DISTANCE_FROM_TOP)
    if deck:
        win.blit(CARD_BACK, pos)
        pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)
    else:
        pg.draw.rect(WIN, (50,50,50), pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)))


def show_revealed(win, revealed):
        for i in range(-3,0):
            try:
                pos = (WIDTH - 2* CARD_WIDTH + 20*i, DISTANCE_FROM_TOP)
                win.blit(revealed[i].pic, pos)
                pg.draw.rect(WIN, BLACK, pg.Rect(pos, (CARD_WIDTH, CARD_HEIGHT)), 2)
            except IndexError:
                pass


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

def show_piles(win, piles):
    pg.draw.rect(WIN, GREY, pg.Rect((170,50), (CARD_WIDTH, CARD_HEIGHT))) if not piles[0] else win.blit(piles[0][-1].pic, (170, 50))
    pg.draw.rect(WIN, GREY, pg.Rect((290,50), (CARD_WIDTH, CARD_HEIGHT))) if not piles[1] else win.blit(piles[1][-1].pic, (290, 50))
    pg.draw.rect(WIN, GREY, pg.Rect((410,50), (CARD_WIDTH, CARD_HEIGHT))) if not piles[2] else win.blit(piles[2][-1].pic, (410, 50))
    pg.draw.rect(WIN, GREY, pg.Rect((530,50), (CARD_WIDTH, CARD_HEIGHT))) if not piles[3] else win.blit(piles[3][-1].pic, (530, 50))


def blit_background(win, stacks, revealed, deck, piles):
    win.fill(GREEN)
    for i in range(len(stacks) - 1):
        show_stack(win, stacks[i], i*1.125)
    show_piles(win, piles)
    show_deck(win, deck)
    show_revealed(win, revealed)
    win.blit(RESET, (10,10))

    text_ins = FONT_SMALL.render('Flips    ', True, BLACK, DARK_GREEN)
    win.blit(text_ins, (WIDTH - CARD_WIDTH - 20, 10))
    text = FONT.render(' 1 ', True, BLACK, BLUE if (1 == NUM_TO_FLIP) else DARK_GREEN)
    win.blit(text, (WIDTH - CARD_WIDTH - 20, 10 + text_ins.get_rect().h))
    text = FONT.render(' 2 ', True, BLACK, BLUE if (2 == NUM_TO_FLIP) else DARK_GREEN)
    win.blit(text, (WIDTH - CARD_WIDTH - 20 + text.get_rect().w, 10 + text_ins.get_rect().h))
    text = FONT.render(' 3 ', True, BLACK, BLUE if (3 == NUM_TO_FLIP) else DARK_GREEN)
    win.blit(text, (WIDTH - CARD_WIDTH - 20 + (text.get_rect().w*2), 10 + text_ins.get_rect().h))
    text_btm = FONT_SMALL.render('cards.  ', True, BLACK, DARK_GREEN)
    win.blit(text_btm, (WIDTH - CARD_WIDTH - 20, 10 + text_ins.get_rect().h + text.get_rect().h))

def get_cards(stacks, index, num):
    if stacks[index]:
        cards = []

        for i in range(-num, 0):
            cards.append(stacks[index].pop(i))
            cards[-1].seen = True
        return cards
    return None


def add_cards(l, to_add):
        l.extend(to_add)


def move_card(win, pos, card, stacks, revealed, deck, piles):
    blit_background(win, stacks, revealed, deck, piles)

    win.blit(card.pic, (pos[0] - 37, pos[1] - 15))
    card.pos = pos
    card.seen = True
    pg.display.update()
    return card.pos


def move_cards(win, pos, cards, stacks, revealed, deck, piles):
    blit_background(win, stacks, revealed, deck, piles)

    for i, card in enumerate(cards):

        win.blit(card.pic, (pos[0] - 37, pos[1] - 15 + i*25))
    
    cards[0].pos = pos
    return None


def move(win, pos, cards, stacks, revealed, deck, piles):
    if cards:
        if len(cards) > 1:
            return move_cards(win, pos, cards, stacks, revealed, deck, piles)
        elif cards:
            return move_card(win, pos, cards[0], stacks, revealed, deck, piles)
    return []

### TODO MAKE IT SO WHEN THE DECK IS CLICKED ON IT FLIPS OVER THREE CARDS

def between(pos, upperx, uppery, lowerx, lowery):
    # print(pos, upperx, lowerx)
    return pos[1] < lowery and pos[1] > uppery and pos[0] < lowerx and pos[0] > upperx

def change_num_flip(pos):
    for i in range(3):
        if pos > WIDTH - CARD_WIDTH - 20 + i*27:
            NUM_TO_FLIP = i+1
    print(NUM_TO_FLIP)
    return NUM_TO_FLIP


def choose_action(pos):
    if between(pos, (WIDTH - 15 - CARD_WIDTH), DISTANCE_FROM_TOP, (WIDTH - 15), (DISTANCE_FROM_TOP + CARD_HEIGHT)):
        return 'deck', None
    elif between(pos, 15, DISTANCE_FROM_TOP, (7.875*CARD_WIDTH), HEIGHT):
        return 'stacks', None
    elif between(pos, (WIDTH - 2*CARD_WIDTH - 60), DISTANCE_FROM_TOP, WIDTH - CARD_WIDTH + 40, DISTANCE_FROM_TOP + CARD_HEIGHT):
        return 'revealed', None
    elif between(pos, 170, 50, 530 + CARD_WIDTH, CARD_HEIGHT + 50):
        return "piles", None
    elif between(pos, 10, 10, RESET.get_rect().w + 11, RESET.get_rect().h+10):
        print('reset')
        return 'reset', None
    elif between(pos, WIDTH - CARD_WIDTH - 20, 25, WIDTH - CARD_WIDTH - 20 + 81, 52):
        num = change_num_flip(pos[0])
        return 'change', num
    else:
        return None, None


def win_screen(win):
    win.fill(DARK_GREEN)
    text = FONT.render("You have completed the game", True, BLACK)
    tr = text.get_rect()
    tr.center = (WIDTH // 2, HEIGHT // 2)
    win.blit(text, tr)
    pg.display.update()
    time.sleep(5)

def reset():
    deck = get_deck()
    stacks = shuffle_deck(deck)
    for i in range(len(stacks) - 1):
        stacks[i][-1].seen = True
    revealed = []
    deck = stacks[-1]
    piles = [[], [], [], []]
    global NUM_TO_FLIP
    NUM_TO_FLIP = 3
    blit_background(WIN, stacks, revealed, deck, piles)
    return deck, piles, revealed, stacks 

def finished(piles):
    return sum([len(pile) for pile in piles]) == 52

def main(WIDTH, HEIGHT, WIN):
    deck,piles,revealed,stacks = reset()
    card = []
    index = None
    flip_cards = False
    to_pile = False
    while True:
        
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if pg.mouse.get_pressed()[0]:
                mouse_position = pg.mouse.get_pos()

                try:
                    action, num_to_flip = choose_action(mouse_position)

                    if action == 'stacks' or card:
                        if not card:

                            index, num = is_on_card_row(WIN, mouse_position, stacks)

                            if index is not None:

                                card = get_cards(stacks, index, num)
                                move(WIN, mouse_position, card, stacks, revealed, deck, piles)
                        else:
                            move(WIN, mouse_position, card, stacks, revealed, deck, piles)
                    elif action == 'deck':    
                        flip_cards = True
                    elif action == 'revealed':
                        if revealed and not card and not flip_cards:
                            card = [revealed.pop(-1)]
                        if card:
                            move(WIN, mouse_position, card, stacks, revealed, deck, piles)
                    elif action == 'piles':
                        if not card:
                            index = get_pile_index(WIN, mouse_position)
                            if index is not None and piles[index]:
                                card = [piles[index].pop(-1)]
                                move(WIN, mouse_position, card, stacks, revealed, deck, piles)
                                to_pile = True
                    elif action == 'change':
                        global NUM_TO_FLIP
                        NUM_TO_FLIP = num_to_flip
                        blit_background(WIN, stacks, revealed, deck, piles)
                    elif action == 'reset':
                        deck, piles, revealed, stacks = reset()
                        
                except AttributeError:
                    pass
            if not pg.mouse.get_pressed()[0]:
        
                if flip_cards:
                    if deck:
                        for i in range(NUM_TO_FLIP):
                            try:
                                revealed.append(deck.pop(0))
                            except:
                                pass
                    else:
                        deck = revealed
                        revealed = []
                    flip_cards = False
                    blit_background(WIN, stacks, revealed, deck, piles)
                elif to_pile:
                    new_index, _ = is_on_card_row(WIN, card[0].pos, stacks)

                    if new_index is not None and stacks[new_index]:
                        print(stacks[new_index])
                        if can_place_card(card[0], stacks[new_index][-1]):
                            add_cards(stacks[new_index], card)

                        else:
                            add_cards(piles[index], card)
                    else:
                        piles[index].append(card[0])
                    card = None
                    index = None
                    to_pile = False
                    blit_background(WIN, stacks, revealed, deck, piles)
                elif card and index is not None:
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
                            # card = None
                            print(f'Placed card in stack {new_index + 1}')
                        else:
                            add_cards(stacks[index], card)
                            # card = None
                            print('Cant place card there')
                        blit_background(WIN, stacks, revealed, deck, piles)
                    elif get_pile_index(WIN, pg.mouse.get_pos()) != None and len(card) == 1:
                        
                        new_index = get_pile_index(WIN, pg.mouse.get_pos())

                        if can_add_to_suit(piles[new_index], card[0]):
                            if stacks[index]:
                                stacks[index][-1].seen = True  
                            add_cards(piles[new_index], card)
                            if finished(piles):
                                win_screen(WIN)
                                deck, piles, revealed, stacks = reset()
                        else: 
                            add_cards(stacks[index], card)
                        # card = None
                        blit_background(WIN, stacks, revealed, deck, piles)
                    else:
                        add_cards(stacks[index], card)
                        # card = None
                        print('Cant place card there')
                    card = None
                    index = None
                    blit_background(WIN, stacks, revealed, deck, piles)
                elif card:
                    new_index, _ = is_on_card_row(WIN, card[0].pos, stacks)
                    try:
                        stack_top = stacks[new_index][-1]
                    except Exception:
                        stack_top = []
                    if new_index is not None:
                        if can_place_card(card[0], stack_top):
                            add_cards(stacks[new_index], card)
                            # card = None
                            print(f'Placed card in stack {new_index + 1}')
                        else:
                            add_cards(revealed, card)
                            # card = None
                            print('Cant place card there')
                        blit_background(WIN, stacks, revealed, deck, piles)
                    elif get_pile_index(WIN, pg.mouse.get_pos()) != None and len(card) == 1:
                        new_index = get_pile_index(WIN, pg.mouse.get_pos())
                        if can_add_to_suit(piles[new_index], card[0]):
                            add_cards(piles[new_index], card)
                        else: 
                            add_cards(revealed, card)
                        blit_background(WIN, stacks, revealed, deck, piles)
                        # card = None
                    else:
                        add_cards(revealed, card)
                        # card = None
                        print('Cant place card there')
                        blit_background(WIN, stacks, revealed, deck, piles)
                    card = None


        pg.display.update()

    
main(WIDTH, HEIGHT, WIN)