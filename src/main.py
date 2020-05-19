import pygame
import random
#import time
from score import Score2
from toolbox import SetUpTable

pygame.display.set_caption("Cribbage")

# INITIALIZATIONS

# Board class

# End of Board class

# Card class
 
class Card():
   
    def __init__(self, i, x, y):
        self.index = i
        self.x = x
        self.y = y
        self.height = cardHeight
        self.width = cardWidth
        self.name = cards[i]
        self.back = backOfCard
        self.face = pygame.image.load(cardFileNames[i])
        self.face = pygame.transform.smoothscale(self.face, (cardWidth, cardHeight))
        self.peek = pygame.transform.smoothscale(self.face, (cardPeekWidth, cardPeekHeight))
        self.showFace = False
        self.peekOn = False
        self.order = i // 4
        self.value = min(self.order+1, 10)    
        self.suit = i % 4
        self.rect = self.face.get_rect()
        #self.rect.center = (self.x, self.y)
 

    # Function to dislay a card in the shell
    #  parameters: none
    
    def show(self, up):
        print("Card.show():",self.index,self.name, self.value, self.order, self.suit, self.rect)
        
    
    # Function to update a card
    #  parametes:
    #   dx & dy: change in x & y from last update (supports animation)

    def update(self, dx, dy):

        self.x += dx
        self.y += dy
        #print("card (x,y)",self.x,self.y)
        if self.showFace:
            self.rect = screen.blit(self.face, (self.x, self.y))
        else:
            self.rect = screen.blit(self.back, (self.x, self.y))
            if self.peekOn:
                screen.blit(self.peek, (self.x, self.y))

# End of Card class

# Hand class, a list of Cards
class Hand():

    def __init__(self, cards, owner):
        self.cards = cards
        self.size = len(cards)
        if owner == 0:
            self.owner = "Player"
        elif owner == 1:
            self.owner = "Python"
        if owner == 2:
            self.owner = "Player Crib"
        elif owner == 3:
            self.owner = "Python Crib"    

                
    # Function to display contents of a Hand in the shell
    #  parameters: none

    def show(self):

        #print("in Hand.show:")
        for i in range(self.size):
            print(self.cards[i].index, self.cards[i].name, self.cards[i].order, self.cards[i].value, self.cards[i].suit)


    # Function to update a Hand, simply calls .update for each Card in Hand
    #  parameters: None
    
    def update(self):

        for i in range(self.size):
            self.cards[i].update(0, 0)


    # Function to flip a Hand face up to face down, or vice versa
    #  parameters: None

    def flip(self):
        
        for i in range(self.size):
            self.cards[i].showFace = not self.cards[i].showFace

                
    # Funtion to sort a Hand
    #  parameters:
    #    ascending (boolean):
    #      True: sorts the Hand in ascending order,
    #      False: sorts the Hand in descending order

    def sort(self, ascending):

        #print("in Hand.sort", self.size)
        if ascending:
            for i in range(self.size-1):
                for j in range(i+1, self.size):
                    if self.cards[i].index > self.cards[j].index:
                        self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
                        self.cards[i].x, self.cards[j].x = self.cards[j].x, self.cards[i].x
                        self.show()                 

    # Function to pull a set of cards from a Hand
    # parameters:
    #   list: list of the cards to pull by position in Hand
    #   mode (boolean):
    #     True: return a list of cards,
    #     False: return a list of card indices
    # returns a list of the requested cards in the requested type

    def pull(self, list, mode):

        pulledCards = []
        for i in range(self.size):
            if i in list:
                if mode:
                    pulledCards.append(self.cards[i])       
                else:
                    pulledCards.append(self.cards[i].index)
        return pulledCards


    # Funtion to score a Hand
    #  parameters:
    #    upcard: index of upcard, -1 if no upcard
    #    diff: difficulty of game (feature request: make difficulty global)
    #    crib (boolean):
    #      True: Hand is the crib (no score for flush of 4)
    #      False: Hand is not the crib
    #    spec: depricated (feature request: remove this parameter)
    
    def score(self, upcard, diff, crib, spec):

        size = self.size
        if size >= 2 and size <= 5:

            pairs = 0
            fifteens = 0
            runsof3 = 0
            runsof4 = 0
            runsof5 = 0
            flush3 = 0
            flush4 = 0
            flush5 = 0
            nibs = 0
            pip = []
            runner = []
            suit = []
            debug = 1
                
            #self.show()
            # sets of 2
            for i in range(size-1):
                for j in range(i+1, size):
                    x = self.cards[i].value
                    y = self.cards[j].value
                    if x + y == 15:
                        fifteens +=1
                        if diff < debug: print("2x15")
                    x = self.cards[i].order
                    y = self.cards[j].order
                    if x == y:
                        pairs +=1
                        if diff < debug: print("pair")
                    
            if size > 2:
                # sets of 5
                if size == 5:             
                    total = 0
                    run = 1
                    runner.clear()
                    flush = 1
                    suit.clear()
                    for i in range(size):
                        total += self.cards[i].value
                        runner.append(self.cards[i].order)
                        suit.append(self.cards[i].suit)
                        if i > 0:
                            if runner[i-1] == runner[i]-1:
                                run+=1
                            if suit[i-1] == suit[i]:
                                flush+=1
                                             
                    if total == 15:
                        fifteens+=1
                        if diff < debug: print("5x15")
                    if run == 5:
                        runsof5+=1
                        if diff < debug: print("run5")
                    if flush == 5:
                        flush5+=1
                        if diff < debug: print("fl5")

                # sets of 4
                if size >= 4:
                    for i in range(size-3):
                        for j in range(i+1, size-2):
                            for k in range(j+1, size-1):
                                for l in range(k+1, size):
                                    total = 0
                                    run = 1
                                    flush = 1
                                    runner.clear()
                                    suit.clear()
                                    n = 0
                                    for m in [i,j,k,l]:
                                        total += self.cards[m].value
                                        runner.append(self.cards[m].order)
                                        suit.append(self.cards[m].suit)
                                        if n > 0:
                                            if runner[n-1] == runner[n]-1 and not runsof5:
                                                run+=1
                                            if suit[n-1] == suit[n] and not flush5:
                                                flush+=1
                                        n+=1
                                        
                                    if total == 15:
                                        fifteens+=1
                                        if diff < debug: print("4x15")
                                    if run == 4:
                                        runsof4+=1
                                        if diff < debug: print("run4")
                                    if flush == 4:
                                        flush4+=1
                                        if diff < debug: print("fl4")

                # sets of 3
                for i in range(size-2):
                    for j in range(i+1, size-1):
                        for k in range(j+1, size):
                            total = 0
                            run = 1
                            runner.clear()
                            flush = 1
                            suit.clear()
                            n = 0
                            for m in [i,j,k]:
                                total += self.cards[m].value
                                runner.append(self.cards[m].order)
                                suit.append(self.cards[m].suit)
                                if n > 0:
                                    if runner[n-1] == runner[n]-1 and not runsof4 and not runsof5:
                                        run+=1
                                    if size == 3 and diff == 2: # count flush3 for 'what if' discard scoring
                                        if suit[n-1] == suit[n]:
                                                flush+=1
                                n+=1
                                
                            if total == 15:
                                fifteens+=1
                                if diff < debug: print("3x15")
                            if run == 3:
                                runsof3+=1
                                if diff < debug: print("3run")
                            if flush == 3:
                                flush3+=1
                                if diff < debug: print("3run")
                                
            # check if crib, if yes only count flush5        
            if crib:
                flush4 = 0

            # check for nibs if a common card was included in hand
            if upcard > 0:
                upcard_suit = upcard % 4
                for i in range(size):
                    if self.cards[i].order == 11 and self.cards[i].suit == upcard_suit:
                        nibs+=1
                        if diff < debug: print("nibs")
          
            
            score = pairs*2 + fifteens*2 + runsof3*3 + runsof4*4 + runsof5*5 + flush4*4 + flush5*5 + nibs + flush3*5/16
            return score
        else:
            return -1
        
    # End of score function
            
# End of Hand class

# Dealer Chip class

# End of Dealer Chip class


# Start the game
pygame.init()
gameWidth = 1000
gameHeight = 650
screen = pygame.display.set_mode((gameWidth, gameHeight))
clock = pygame.time.Clock()
running = True


# Deck variables
pips = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suits = ['C','D','H','S']
cards = []
cardFileNames = []
cardPics = []

# Cards
for i in range(13):
    for j in range (4):
        card = str(pips[i])+str(suits[j])
        cards.append(card)
        name = "../assets/"+card+".png"
        cardFileNames.append(name)


# ----- Load images for game items -----
# Background
backgroundImage = pygame.image.load("../assets/background1.png")

# The board
boardHeight = 1200
boardWidth = 3595
boardScale = 0.2
boardPic = pygame.image.load("../assets/board.png")
boardPic = pygame.transform.rotate(boardPic, 90)
boardPic = pygame.transform.scale(boardPic, (int(boardWidth*boardScale),int(boardHeight*boardScale)))
boardRect = boardPic.get_rect()

# Cards (backs only, faces loaded went dealt)
cardHeight = 100
cardWidth = 65
cardPeekHeight = 60
cardPeekWidth = 40

backOfCard = pygame.image.load("../assets/blue_back.png")
backOfCard = pygame.transform.smoothscale(backOfCard, (cardWidth, cardHeight))
cardWidth = backOfCard.get_width()
cardHeight = backOfCard.get_height()

# Dealer chip
dealerChipImage = pygame.image.load("../assets/dealer.png")
dealerChipImage = pygame.transform.smoothscale(dealerChipImage, (50,50))

# Discard button
discardButton = pygame.image.load("../assets/discard.png")
discardButton = pygame.transform.smoothscale(discardButton, (120,50))
discardButtonSmall = pygame.transform.smoothscale(discardButton, (100,40))
discardButtonRect = discardButton.get_rect()

# Game phase
dealingBug = pygame.image.load("../assets/phaseDealing.png")
sorting = pygame.image.load("../assets/phaseSorting.png")
discarding = pygame.image.load("../assets/phaseDiscarding.png")


# ----- Creen layout position variables for game items -----
# The board
boardRow = 240
boardCol = -20

# Card / Hand positions
deckRow = 300
deckCol = 800
playerRow = 120
playerCol = 75
pythonRow = 495
pythonCol = 75
playerCribRow = 160
playerCribCol = 685
pythonCribRow = 455
pythonCribCol = 685
playerHandPositions = []
pythonHandPositions = []
playerCribPositions = []
pythonCribPositions = []
dealerCribPositions = []
for i in range(6):
    playerHandPositions.append([playerCol*(i+1),playerRow])
    pythonHandPositions.append([pythonCol*(i+1),pythonRow])
    if i < 4:
        playerCribPositions.append([playerCribCol+(75*i),playerCribRow])
        pythonCribPositions.append([pythonCribCol+(75*i),pythonCribRow])

        
# Dealer chip positions
playerDealerChipRow = 150
playerDealerChipCol = 20
pythonDealerChipRow = 520
pythonDealerChipCol = 20
targetDealerChipRow = 335
targetDealerChipCol = 20

# Discard button position
discardButtonRow = 150
discardButtonCol = 540

# Phase text
phaseRow = 10
phaseCol = 20

                                  
# ----- Arrays for various hands -----
#player_hand = []
#player_card = []

python_hand = []
playerHand = []
playerDiscards = []
pythonHand = []
pythonDiscards = []
cribHand = []
cardsDealt = []
cardsKnownToPython = []

#python_card = []
#python_index = []
#python_array = [[], []]
crib_cards = []
hand_to_score = []
hand_to_score_card = []
hand_to_score_index = []
hand_to_score_array = [[], []]
cards_to_score = []
discards_to_score = []
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




# Dealing variables
playerIsDealer = True
evens = [2, 4, 6, 8, 10, 12]
odds = [1, 3, 5, 7, 9, 11]

# Scoring variables
PlayerWins = [0,0,0,0]
pythonWins = [0,0,0,0]

# Staging variables
winner = False
newHand = True
dealing = False
sorting = False
discarding = False
pegging = False
scoring = False

# Title Text
font = pygame.font.SysFont("lato", 48)
titleText = font.render("Python Cottage Cribbage!!", 1, (255, 255, 255))
titleRect = titleText.get_rect(center=(gameWidth/2, 30))
screenFont = pygame.font.SysFont("lato", 24)  # for future screen messages


# Other on screen messages
font = pygame.font.SysFont("lato", 32)
scoreTitle = font.render("Games Won", 1, (255,255,255))
dealingPhaseOn = font.render("Dealing...", 0, (255,255,255))
dealingPhaseOff = font.render("Dealing...", 0, (0,0,0))
sortingPhaseOn = font.render("Sorting...", 0, (255,255,255))
sortingPhaseOff = font.render("Sorting...", 0, (0,0,0))
discardPhaseOn = font.render("Discard", 0, (255,255,255))
discardPhaseOff = font.render("Discard", 0, (0,0,0))
discardTextOn = font.render("Select 2 cards to discard", 1, (255,255,255))
discardTextOff = font.render("Select 2 cards to discard", 1, (0,0,0))

# Get diffculty from player; 0 = easy, 1 = medium, 2 = hard, 3 = impossible
difficulty=1

# timers & velocities
shortTimer = 0
shortTimer = 10
mediumTimer = 0
mediumTimerMax = 50
longTimer = 0
longTimerMax = 250

dealerChipVelocity = 5
cardVelocity = 50


# ----- AND NOW, CRIBBAGE! -----

while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()


    # things to set at start of new game
    gameOn = True
    playerScore = 0
    pythonScore = 0
        

    # Game loop
    if gameOn:
        
        #screen.blit(background_image, (0,0))
        screen.fill((10,100,10))
        screen.blit(titleText, titleRect)
        #screen.blit((titleText + str(clock.get_fps()), titleRect))
        screen.blit(backOfCard, (deckCol, deckRow)) 

        diffText = "Difficulty: "
        if difficulty == 0:
            diffText = diffText + "Easy Peasy"
        elif difficulty == 1:
            diffText = diffText + "Medium"
        elif difficulty == 2:
            diffText = diffText + "Hard"
        elif difficulty == 3:
            diffText = diffText + "Impossible"
    
        screenText = screenFont.render(str(diffText), 1, (0,0,0))
        textRect = screenText.get_rect(center=(gameWidth/2 ,70))
        screen.blit(screenText, textRect)
        
        screen.blit(boardPic, (boardCol, boardRow))


        # Reset deck for new hand
        if newHand:
            playerCards = 0
            #player_hand = []
            playerDealt = []
            playerHand = []
            playerDiscards = []
            pythonCards = 0
            #python_hand = []
            pythonHand = []
            pythonDealt = []
            pythonDiscards = []
            crib = []
            cribHand = []
            cardsDealt.clear()
            cardsKnownToPython.clear()
            dealCounter = 0
            print("*********** new hand ***********")
            dealerChipRow = targetDealerChipRow
            dealerChipCol = targetDealerChipCol
            if difficulty == 0:
                playerIsDealer = True
                targetDealerChipRow = playerDealerChipRow
                targetDealerChipCol = playerDealerChipCol
            else:
                coin = random.randint(0,1) # flip a coin
                if coin == 0:
                    playerIsDealer = True
                    targetDealerChipRow = playerDealerChipRow
                    #targetDealerChipCol = playerDealerChipCol
                else:
                    playerIsDealer = False
                    targetDealerChipRow = pythonDealerChipRow
                    #targetDealerChipCol = pythonDealerChipCol             
             
            for i in range(52):
                cardsDealt.append(False)
                cardsKnownToPython.append(False)
                
            newHand = False
            dealing = True
            sorting = False
            discarding = False
            getUpCard = False
            pegging = False
            scoring = False
            phaseUpdated = False
            dealingTimer = mediumTimerMax

        # Deal the cards
        if dealing:

            screen.blit(dealingPhaseOn, (phaseCol, phaseRow))
            screen.blit(dealingBug, (phaseCol, phaseRow))
            
            if not phaseUpdated:               
                phaseUpdated = True
                print("DEALING")

            # Move Dealer chip to it's position
            if playerIsDealer:
                if dealerChipRow > targetDealerChipRow:
                    dealerChipRow -= dealerChipVelocity
                    if dealerChipRow < targetDealerChipRow:
                        dealerChipRow = targetDealerChipRow               
            else:
                if dealerChipRow < targetDealerChipRow:
                    dealerChipRow += dealerChipVelocity
                    if dealerChipRow > targetDealerChipRow:
                        dealerChipRow = targetDealerChipRow
                    
            screen.blit(dealerChipImage, (dealerChipCol, dealerChipRow))
            
            if playerIsDealer:
                playerGets = evens 
                pythonGets = odds  
            else:
                playerGets = odds
                pythonGets = evens
                
            # Pick a random card to deal
            pick = random.randint(0,51)
            while cardsDealt[pick]:
                pick = random.randint(0,51)
            cardsDealt[pick] = True

                    
            if dealCounter < 13:
                dealCounter += 1
                if dealCounter in playerGets:
                    playerHand.append(Card(pick, deckCol, deckRow))
                    playerCards += 1

                elif dealCounter in pythonGets:
                    pythonHand.append(Card(pick, deckCol, deckRow))
                    cardsKnownToPython[pick] = True
                    pythonCards += 1


            # Animate deal of the cards face down via Card.update() function
            for i in range(playerCards):
                dx = int((playerHandPositions[i][0] - playerHand[i].x)/5)
                dy = int((playerHandPositions[i][1] - playerHand[i].y)/5)
                #print("delta", i, dx, dy)
                playerHand[i].update(dx, dy)
            for i in range(pythonCards):
                dx = int((pythonHandPositions[i][0] - pythonHand[i].x)/5)
                dy = int((pythonHandPositions[i][1] - pythonHand[i].y)/5)
                pythonHand[i].update(dx, dy)
                #pythonHand.update()
                
            #
            dealingTimer -= 1
            #print("timer",dealingTimer)
            #print("counter",dealCounter)

            #Check to see if we're done dealing
            if dealCounter > 12 and dealingTimer <= 0:
                # make new Hands from dealt dards, turn on Peek if Easy mode
                playerDealt = Hand(playerHand,0)
                pythonDealt = Hand(pythonHand,1)
                if difficulty < 99:
                    for i in range(pythonCards):
                        pythonDealt.cards[i].peekOn = True
                
                dealing = False
                sorting = True
                screen.blit(dealingPhaseOff, (phaseCol, phaseRow))
                phaseUpdated = False                 

                        
        # SORTING phase
        if sorting:

            screen.blit(sortingPhaseOn, (phaseCol, phaseRow))
            screen.blit(dealerChipImage, (dealerChipCol, dealerChipRow))
        
            if not phaseUpdated:
                phaseUpdated = True
                print("SORTING")

            playerDealt.sort(True)
            playerDealt.flip()
            playerDealt.update()
            pythonDealt.sort(True)
            pythonDealt.update()
                      
            # Done sorting, update phase variables
            sorting = False
            screen.blit(sortingPhaseOff, (phaseCol, phaseRow))
            discarding = True
            phaseUpdated = False   


        # DISCARD Phase
        if discarding:

            screen.blit(discardPhaseOn, (phaseCol, phaseRow))

            # Move Dealer chip to it's position (in case it's not there yet)
            if playerIsDealer:
                dealerCribPositions = playerCribPositions
                if dealerChipRow > targetDealerChipRow:
                    dealerChipRow -= dealerChipVelocity/10
                    if dealerChipRow < targetDealerChipRow:
                        dealerChipRow = targetDealerChipRow               
            else:
                dealerCribPositions = playerCribPositions
                if dealerChipRow < targetDealerChipRow:
                    dealerChipRow += dealerChipVelocity/10
                    if dealerChipRow > targetDealerChipRow:
                        dealerChipRow = targetDealerChipRow

            screen.blit(dealerChipImage, (dealerChipCol, dealerChipRow))
            
            if not phaseUpdated:
                phaseUpdated = True
                playerDiscardDone = False
                pythonDiscardDone = False
                print("DISCARDING")

                discardTimer = 0
                keepersList = [0,1,2,3,4,5]
                discardsList = []
                discardPicks = []
                discards = 0
                #pythonKeepers = [0,1,2,3,4,5]
                #pythonDiscards = []
                pythonMaxScore = -1
                
                #python_discards = 0
               
                #best_hand = []
                #best_discard = []

                           
                for i in range(6):
                    discardPicks.append(False)

            # Player discard logic
            if not playerDiscardDone:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = event.pos
                    #print("mouse",mousePos)
                    for i in range(playerCards):
                        cardRect = playerDealt.cards[i].rect
                        if cardRect.collidepoint(mousePos):
                            print("Card clicked",i)
                            #if i in playerDiscards[i]:
                            if discardPicks[i]:
                                discardPicks[i] = False
                                keepersList.append(i)
                                discardsList.remove(i)
                                playerDealt.cards[i].showFace = True
                                playerDealt.cards[i].peekOn = False
                            else:
                                discardPicks[i] = True
                                keepersList.remove(i)
                                discardsList.append(i)
                                playerDealt.cards[i].showFace = False
                                playerDealt.cards[i].PeekOn = True
                            discards = len(discardsList)    
     
                # Display the player's hand based on discard options
                for i in range(playerCards):
                    if discardPicks[i]:
                        playerDealt.cards[i].peekOn = True
                    else:
                        playerDealt.cards[i].peekOn = False

                playerDealt.update()
 
                #print("discards",playerKeepers,playerDiscards)
                if discards == 2:
                    discardButtonRect = screen.blit(discardButton, (discardButtonCol,discardButtonRow))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    if discardButtonRect.collidepoint(mousePos):
                        print("Button clicked")
                        screen.blit(discardButtonSmall, (discardButtonCol+4,discardButtonRow+10))
                        print("keepers",keepersList)
                        playerKeepers = Hand(playerDealt.pull(keepersList, True),0).sort(True)
                        playerKeepers.show()
                        #playerCards = 4
                        print("discards",discardsList)
                        playerDiscards = Hand(playerDealt.pull(discardsList, True),0).sort(True)
                        playerDiscards.show()
                        for i in range(discards):
                            print("discard",i)
                            print(playerDiscards.cards[i].name)
                            dx = int((dealerCribPositions[i][0] - playerDiscards.cards[i].x)/5)
                            dy = int((dealerCribPositions[i][1] - playerDiscards.cards[i].y)/5)
                            playerDiscards.cards[i].update(dx, dy)

                
                if dx == 0 and dy == 0:
                    pythonDiscardDone = True
                    #
                    #
                    #
                    #
                    
                       
            # python discard logic
            if pythonDiscards == 0:
                hand_to_score_index.clear()
                hand_to_score_card.clear()
                hand_to_score_array.clear()
                discards_index.clear()
                discards_card.clear()
                discards_array.clear()
                cards_to_score.clear()
                #index_to_score.clear()
                discards_to_score.clear()
                #card1 = 0
                for i in range(0, pythonCards - 3):
                    for j in range(i+1, pythonCards - 2):
                        for k in range(j+1, pythonCards - 1):
                            for l in range(k+1, pythonCards):                                                             
                                m=-1; n=-1
                                for x in range(pythonCards):
                                    if not x in [i,j,k,l]:
                                        if m<0:
                                            m=x
                                        else:
                                            n=x
                                                                        
                                # if Easy, ignore score of discards
                                if difficulty == 0:
                                    scoreHand = Hand(pythonDealt.pull([i,j,k,l], True))
                                    keep_score = scoreHand.score(-1, difficulty, False, False)
                                    discard_score = 0
   
                                # if Medium, score hand and discards but not 'what if'
                                elif difficulty == 1:
                                    scoreHand = Hand(pythonDealt.pull([i,j,k,l], True),1)
                                    keep_score = scoreHand.score(-1, difficulty, False, False)
                                    scoreHand = Hand(pythonDealt.pull([m,n], True),1)
                                    discard_score = scoreHand.score(-1, difficulty, False, False)
                                    
                                # if Hard, score hand, discards and 'what if'
                                elif difficulty == 2:
                                    keep_score = 0
                                    discard_score = 0
                                    for I in range(52):
                                        # go through the deck (cards not know to python)
                                        # cards in player Hand will be used in 'what if' for fairness
                                        if not cardsKnownToPython[I]:
                                            # go through the deck (cards not know to python
                                            index_to_score = pythonDealt.pull([i,j,k,l], False)
                                            index_to_score.append(I)
                                            cards_to_score.clear()
                                            for J in range(len(index_to_score)):
                                                cards_to_score.append(Card(index_to_score[J], deck_col, deck_row))
                                            scoreHand = Hand(cards_to_score).sort(True)
                                            scoreHand = scoreHand.sort(True)
                                            keep_score += scoreHand.score(I, difficulty, False, False)
                                            
                                            index_to_score = pythonDealt.pull([m,n], False)
                                            index_to_score.append(I)
                                            cards_to_score.clear()
                                            for J in range(len(index_to_score)):
                                                cards_to_score.append(Card(index_to_score[J], deck_col, deck_row))
                                            scoreHand = Hand(cards_to_score).sort(true)
                                            scoreHand = scoreHand.sort(True)
                                            discard_score += scoreHand.score(I, difficulty, False, False)
                                            
                                    keep_score = keep_score / 46
                                    discard_score = discard_score / 46

                                # if Impossible (look in player's Hand):
                                #   score players Hand to predict their discards
                                #   omit player cards from 'what if' scori
                                #   ??fix the upcard on player deal??

                                #  TODO


                                # dealer benefits from discards/crib
                                if playerIsDealer:
                                    python_score = keep_score - discard_score
                                else:
                                    python_score = keep_score + discard_score
                                
                                if python_score > pythonMaxScore:
                                    #print("new max", python_score, keep_score, discard_score)
                                    pythonMaxScore = python_score
                                    bestCards = [i,j,k,l]
                                    bestDiscards = [m,n]
                                    #print("new keepers", [i,j,k,l])
                                    #print("new discards", [m,n])
                                    
                            # end of l loop  
                        # end of k loop  
                    # end of j loop
                # end of i loop
                #if card1 <= pythonCards -3:
                #    card1 += 1
                
       
                #print("Max score",pythonMaxScore)
                #print("Dealt ");pythonDealt.show()
                pythonKeepers = Hand(pythonDealt.pull(bestCards, True),1)
                #print("Keepers ");pythonKeepers.show()
                pythonDiscards = Hand(pythonDealt.pull(bestDiscards, True),1)
                #print("Discards ");pythonDiscards.show()
                pythonCards = 4

                for i in range(2):
                    dx = int((pythonCribPositions[i][0] - pythonDiscards.cards[i].x)/5)
                    dy = int((pythonCribPositions[i][1] - pythonDiscards.cards[i].y)/5)
                    pythonDiscards.cards[i].update(dx, dy)
                
                if dx == 0 and dy == 0:
                    pythonDiscardDone = True

                
                # put python discards in crib
                #print("best discards", best_discards)

            #  Display hands with current discard status
            #playerKeepers.update()
            #pythonKeepers.update()

            #if playerIsDealer:
            #    dealerCribRow = playerCribRow
            #else:
            #    dealerCribRow = pythonCribRow
            
            # check if we're done discarding
            if playerDiscardDone and pythonDiscardDone:
                # done discarding, update phase variables
                cribCards = playerDiscards,best_discards
                print("crib",cribCards)
                discarding = False
                getUpCard = True
                screen.blit(discardPhaseOff, (phaseCol, phaseRow))
                phase_updated = False        

        # Up-card
        if getUpCard:
            pick = random.randint(0,51)
            while cardsDealt[pick]:
                pick = random.randint(0,51)
            upCard = Card(pick, deckCol, deckRow)
            upCard.update(deckCol, deckRow)
            #pic_to_draw = pygame.transform.scale(card_pics[pick], (int(card_width*card_scale), int(card_height*card_scale)))        
            #screen.blit(pic_to_draw, (deck_col, deck_row))
            getUpCard = False
            pegging = True

           
        # pegging

        # scoring

        
        
        # wait for player to press SPACE to get a new hand
        #keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            new_hand = True
       
        # We have a winner!!
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    #pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
