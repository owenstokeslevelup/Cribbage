import pygame
import random
#import pdb; pdb.set_trace()
from score import Score2
from toolbox import Score
from toolbox import Sort
from toolbox import Show
from table import SetUpTable

# INITIALIZATIONS

# Card class
class Card():

    def __init__(self, i, name, face):
        """print("i",i)
        print("name",name)
        print("face",face)"""
        self.index = i
        self.name = name
        self.face = face
        self.back = back_of_card
        self.size = 0.1

    def update(self, screen, x, y, up):
        #print("card",self.name,self.index)
        if up:
            screen.blit(self.face, (x, y))
        else:
            screen.blit(self.back, (x, y))
        
#end of Card class

# Hand class, a set of Cards
class Hand():

    def __init__(self, cards, size):
        self.cards = cards
        self.size = size

    def mysort(self, ascending):

        if ascending:
            #print("acsending",ascending)
            for i in range(self.size-1):
                for j in range(i+1,self.size):
                    if self.cards[i].index > self.cards[j].index:
                        self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
                        
# end of Hand class

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Screen position variables
player_row = 120
player_col = 75
player_crib_row = 160
player_dealer_chip_row = 156
player_dealer_chip_col = 20
python_row = 495
python_col = 75
python_crib_row = 455
python_dealer_chip_row = 531
python_dealer_chip_col = 20
dealer_crib_row = 0
crib_row = 0
crib_col = 685
board_row = 240
board_col = -20
deck_row = 300
deck_col = 800
phase_row = 10
phase_col = 20

# set the table
SetUpTable(screen, game_height, game_width, board_col, board_row)

# define the deck
pips = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suits = ['C','D','H','S']
values = [1,2,3,4,5,6,7,8,9,10,10,10,10]
runOrder = [1,2,3,4,5,6,7,8,9,10,11,12,13]
cards = []
card_pics = []
card_height = 1055
card_width = 689
card_scale = 0.1

# arrays for various hands
player_hand = []
#playerHand = []
player_card = []
player_index = []
player_array = [[], []]
python_hand = []
pythonHand = []
python_card = []
python_index = []
python_array = [[], []]
crib_hand = [[], []]
hand_to_score = []
hand_to_score_card = []
hand_to_score_index = []
hand_to_score_array = [[], []]
cards_to_score = []
best_hand_card = []
best_hand_index = []
best_hand_array = [[], []]
discards = []
discards_card = []
discards_index = []
discards_array = [[], []]
best_discards_card = []
best_discards_index = []
best_discards_array = [[], []]
cards_dealt = []
cards_known_to_python = []

# scoring variables
player_score = 0
python_score = 0
player_is_dealer = ""

# staging variables
winner = False
new_hand = True
dealing = False
sorting = False
discarding = False
pegging = False
scoring = False

# other on screen messages
font = pygame.font.SysFont("lato", 32)
score_title = font.render("Games Won", 1, (255,255,255))
dealing_phase_on = font.render("Dealing...", 0, (255,255,255))
dealing_phase_off = font.render("Dealing...", 0, (0,0,0))
sorting_phase_on = font.render("Sorting...", 0, (255,255,255))
sorting_phase_off = font.render("Sorting...", 0, (0,0,0))
discard_phase_on = font.render("Discard", 0, (255,255,255))
discard_phase_off = font.render("Discard", 0, (0,0,0))
discard_text_on = font.render("Select 2 cards to discard", 1, (255,255,255))
discard_text_off = font.render("Select 2 cards to discard", 1, (0,0,0))

# Get diffculty from player; 0 = easy, 1 = medium, 2 = hard
difficulty=0
if difficulty == 0:
    diff_text = "Difficulty: Easy Peasy"
elif difficulty == 1:
    diff_text = "Difficulty: Medium"
elif difficulty == 2:
    diff_text = "Difficulty: Hard"
    
screen_font = pygame.font.SysFont("lato", 24)
screen_text = screen_font.render(str(diff_text), 1, (255,255,255))
text_rect = screen_text.get_rect(center=(game_width/2 ,70))
screen.blit(screen_text, text_rect)

pygame.display.flip()

# load images
# cards
for i in range(13):
    for j in range (4):
        card = str(pips[i])+str(suits[j])
        cards.append(card)
        name = "../assets/"+card+".png"
        pic_to_load = pygame.image.load(name)
        pic_to_load = pygame.transform.scale(pic_to_load, (int(card_width*card_scale), int(card_height*card_scale)))
        card_pics.append(pic_to_load)
# card back 
back_of_card = pygame.image.load("../assets/blue_back.png")
back_of_card = pygame.transform.scale(back_of_card, (int(card_width*card_scale), int(card_height*card_scale)))
# dealer chip
dealer_chip = pygame.image.load("../assets/dealer1.png")
dealer_chip = pygame.transform.scale(dealer_chip, (36,36))
#print(cards)
#for i in range(52): screen.blit(card_pics[i], (i*10, i*10)); pygame.display.flip()
 


# AND NOW, CRIBBAGE...

while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Game loop
    if not winner:

        # shuffle deck for new hand
        if new_hand:
            #for cards in playerHand
            player_cards = 0
            player_hand = []
            python_cards = 0
            python_hand = []
            python_hand_pips = []
            #playerHand.clear()
            #pythonHand.clear()
            cards_dealt.clear()
            cards_known_to_python.clear()
            if player_is_dealer == "":
                coin = random.randint(0,1)
                if difficulty == 0:
                    player_is_dealer = True
                elif coin == 0:
                    player_is_dealer = True
                else:
                    player_is_dealer = False
            for i in range(52):
                cards_dealt.append(False)
                cards_known_to_python.append(False)
            new_hand = False
            dealing = True
            sorting = False
            discarding = False
            get_up_card = False
            pegging = False
            scoring = False
            phase_updated = False

        # deal the cards
        if dealing:
            if not phase_updated:
                screen.blit(dealing_phase_on, (phase_col, phase_row))
                phase_updated = True
                if player_is_dealer:
                    screen.blit(dealer_chip, (player_dealer_chip_col, player_dealer_chip_row))
                else:
                    screen.blit(dealer_chip, (python_dealer_chip_col, python_dealer_chip_row))
                       
            if player_cards < 6:
                # Deal (contruct) a random card
                pick = random.randint(0,51)
                while cards_dealt[pick]:
                    pick = random.randint(0,51)
                cards_dealt[pick] = True
                player_hand.append(Card(pick, cards[pick], card_pics[pick]))
                player_hand[player_cards].update(screen, player_col*(player_cards+1), player_row, False)
                
                player_card.append(cards[pick])
                player_index.append(pick)
                player_cards += 1
                
                # draw a card back for each card dealt
                #screen.blit(back_of_card_draw, (player_col*player_cards, player_row))
                
            if python_cards < 6:
                pick = random.randint(0,51)
                while cards_dealt[pick]:
                    pick = random.randint(0,51)
                cards_dealt[pick] = True
                cards_known_to_python[pick] = True
                python_hand.append(Card(pick, cards[pick], card_pics[pick]))
                python_hand[python_cards].update(screen, python_col*(python_cards+1), python_row, False)
                #print("this card",python_hand[python_cards].name)
                python_card.append(cards[pick])
                python_index.append(pick)
                python_cards +=1
                              
                # draw a card back for each card dealt
                #screen.blit(back_of_card, (python_col*python_cards, python_row))         

            # check to see if we're done dealing
            if player_cards == 6 and python_cards == 6:
                playerHand = Hand(player_hand, player_cards)
                pythonHand = Hand(python_hand, python_cards)
                # draw remaining cards
                screen.blit(back_of_card, (deck_col, deck_row))
                pygame.display.flip()
                # done dealing, update phase variables
                dealing = False
                sorting = True
                screen.blit(dealing_phase_off, (phase_col, phase_row))
                phase_updated = False

        # sorting phase
        if sorting:
            
            if not phase_updated:
                screen.blit(sorting_phase_on, (phase_col, phase_row))
                pygame.display.flip()
                phase_updated = True
                print("SORTING")

            playerHand.mysort(True)
            pythonHand.mysort(True)

            """player_hand = Sort(player_hand, player_cards, True)
            Show(player_hand, player_cards) 
            python_hand = Sort(python_hand, python_cards, True)
            Show(python_hand, python_cards)
            """
            
            for i in range(6):    
                pic_to_draw = pygame.transform.scale(playerHand.cards[i].face, (int(card_width*card_scale), int(card_height*card_scale)))
                playerHand.cards[i].update(screen, player_col*(i+1), player_row, True)

                if difficulty < 99:
                    pic_to_draw = pygame.transform.scale(pythonHand.cards[i].face, (int(card_width*card_scale), int(card_height*card_scale)))
                    #screen.blit(pic_to_draw, (python_col*(i+1), python_row))
                    pythonHand.cards[i].update(screen, python_col*(i+1), python_row, True)
                    
            #done sorting, update phase variables
            sorting = False
            discarding = True
            screen.blit(sorting_phase_off, (phase_col, phase_row))
            phase_updated = False   

        # Discard phase
        if discarding:

            if phase_updated == False:
                screen.blit(discard_phase_on, (phase_col, phase_row))
                pygame.display.flip()
                phase_updated = True
                print("DISCARDING")
                player_discards = 0
                python_discards = 0
                max_score = 0
                best_hand = []
                best_discard = []    
                
            # python discard logic
            if python_discards == 0:
                hand_to_score_index.clear()
                hand_to_score_card.clear()
                hand_to_score_array.clear()
                discards_index.clear()
                discards_card.clear()
                discards_array.clear()
                cards_to_score.clear()
                for i in range(0, 3):
                    hand_to_score_index.append(python_index[i])
                    hand_to_score_card.append(python_card[i])
                    cards_to_score.append(python_hand[i])
                    for j in range(i+1, 4):
                        hand_to_score_index.append(python_index[j])
                        hand_to_score_card.append(python_card[j])
                        cards_to_score.append(python_hand[j])
                        for k in range(j+1, 5):
                            hand_to_score_index.append(python_index[k])
                            hand_to_score_card.append(python_card[k])
                            cards_to_score.append(python_hand[k])
                            for l in range(k+1, 6):
                                hand_to_score_index.append(python_index[l])
                                hand_to_score_card.append(python_card[l])
                                cards_to_score.append(python_hand[l])
                                hand_to_score_array = [hand_to_score_index, hand_to_score_card]; print("score",hand_to_score_array)
                                scoreHand = Hand(hand_to_score_array)
                                for I in range(4):
                                    print(scoreHand.cards[i].name)
                                
                                for x in range(python_cards):
                                    if (x != i) and (x != j) and (x != k) and (x != l):
                                        #discards.append(python_hand[x])
                                        discards_index.append(python_index[x])
                                        discards_card.append(python_card[x])
                                discards_array = [discards_index, discards_card]; print("discard",discards_array)                                            
                                # if Easy, ignore score of discards
                                if difficulty == 0:
                                    #keep_score = Score2(hand_to_score, -1, 4, difficulty, False, values, runOrder)
                                    #discard_score = 0
                                    test_score = Score(python_hand, -1, 4, difficulty, False, False); print("test score", test_score)
                                    keep_score = Score2(hand_to_score_array, -1, 4, difficulty, False, values, runOrder); print("Score hand:",hand_to_score_array)
                                    discard_score = 0
   
                                # if Medium, score hand + crib but without 'what if'
                                elif difficulty == 1:
                                    keep_score=0
                                    discard_score=0
                                    #keep_score = Score2(hand_to_score_array, -1, 4, difficulty, False, values, runOrder)
                                    #discard_score = Score2(discards_array, -1, 2, difficulty, False, values, runOrder)

                                # if Hard, score hand, crib and 'what if'
                                elif difficulty == 2:
                                    what_if_keep = hand_to_score
                                    what_if_discards = discards
                                    what_if_score = 0
                                    keep_score = 0
                                    discard_score = 0
                                    for I in range(52):
                                        if not cards_known_to_python[I]:
                                            what_if_keep.append(I)
                                            what_if_discards.append(I)

                                            what_if_keep = sorted(what_if_keep)
                                            what_if_discards = sorted(what_if_discards)
                                            #keep_score += Score2(what_if_keep, I, 5, difficulty, False, values, runOrder)
                                            #discard_score += Score2(what_if_keep, I, 3, difficulty, False, values, runOrder)                                        

                                            what_if_keep.remove(I)
                                            what_if_discards.remove(I)
                                            
                                    keep_score = keep_score / 46
                                    discard_score = discard_score / 46
                                         
                                # dealer benefits from discards/crib
                                if player_is_dealer:
                                    python_score = keep_score - discard_score
                                else:
                                    python_score = keep_score + discard_score
                                
                                print("scores", python_score, keep_score, discard_score)
                                    
                                if python_score > max_score:
                                    print("new max")
                                    max_score = python_score
                                    best_hand_index.clear()
                                    best_hand_card.clear()
                                    best_discards_index.clear()
                                    best_discards_card.clear()
                                    for I in range(4):
                                        best_hand_index.append(hand_to_score_index[I])
                                        best_hand_card.append(hand_to_score_card[I])
                                    for I in range(2):
                                        best_discards_index.append(discards_index[I])
                                        best_discards_card.append(discards_card[I])
                                    best_hand_array = [best_hand_index, best_hand_card]
                                    best_discards_array = [best_discards_index, best_discards_card]

                                print("best hand so far", best_hand_array)
                                hand_to_score_index.remove(python_index[l])
                                hand_to_score_card.remove(python_card[l])
                                print("best discards so far", best_discards_array)
                                discards_index.clear()
                                discards_card.clear()
                            # end of l loop  
                            hand_to_score_index.remove(python_index[k])
                            hand_to_score_card.remove(python_card[k])
                        # end of k loop  
                        hand_to_score_index.remove(python_index[j])
                        hand_to_score_card.remove(python_card[j])
                    # end of j loop
                    hand_to_score_index.remove(python_index[i])
                    hand_to_score_card.remove(python_card[i])
                # end of i loop
            print("Max score",max_score)
            print("Dealt",python_array)
            print("Keepers",best_hand_array)
            print("Discards",best_discards_array)
            # put python discards in crib
            for i in range(2):
                #discard = best_discards_index[i]; print(discard)
                #position = python_index.index(discard); print(position)
                print("--------------------------")
                pic_to_draw = pygame.transform.scale(back_of_card, (int(card_width*card_scale), int(card_height*card_scale)))
                screen.blit(pic_to_draw, (crib_col + 75*i, dealer_crib_row))

            python_discards = 2                
            cards_discarded = 4

            # check if we're done discarding
            if python_discards == 2:
                if player_is_dealer:
                    dealer_crib_row = player_crib_row
                else:
                    dealer_crib_row = python_crib_row
                for i in range(cards_discarded):
                    screen.blit(back_of_card, (crib_col*(i+1), dealer_crib_row))

                # done discarding, update phase variables
                discarding = False
                get_up_card = True
                screen.blit(discard_phase_off, (phase_col, phase_row))
                phase_updated = False        

        # Up-card
        if get_up_card:
            pick = random.randint(0,51)
            while cards_dealt[pick]:
                pick = random.randint(0,51)
            pic_to_draw = pygame.transform.scale(card_pics[pick], (int(card_width*card_scale), int(card_height*card_scale)))        
            screen.blit(pic_to_draw, (deck_col, deck_row))
            get_up_card = False
            pegging = True
            
        # pegging

        # scoring
        
        # wait for player to press SPACE to get a new hand
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:    
            print("*********** new hand ***********")
            if player_is_dealer:
                player_is_dealer = False
            else:
                player_is_dealer = True
            new_hand = True
        
        # We have a winner!!
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
