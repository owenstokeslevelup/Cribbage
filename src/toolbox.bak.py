# TOOLBOX for functions used by Cribbage game

# FUNCTION for scoring a hand
# parameters:
#   hand: list of CArds (see Card class)
#   common_card:
#     card added to hand; i.e. up-card or 'what if' card
#     index of common card or -1 if no common card 
#   diff:
#     difficulty of game as selected by user/player
#   crib:
#     True if scoring crib (need 5 card flush)
#   spec:
#     True if 'speculative' sccoring.  i.e. suited discards, running discards

def Score(hand, common_card, cards, diff, crib, spec):

    if cards >= 2 and cards <= 5:
        #index = hand_array[0]; #print("SCindex",index)
        #hand = hand_array[1]; #print("SChand",hand)
        pairs = 0
        fifteens = 0
        runsof3 = 0
        runsof4 = 0
        runsof5 = 0
        flush4 = 0
        flush5 = 0
        nibs = 0
        pip = []
        runner = []
        suit = []
            
        # sets of 2
        for i in range(cards-1):
            for j in range(i+1, cards):
                total = 0
                pip.clear()
                n = 0
                for m in (i,j):
                    total += values[int(index[m]) // 4]
                    pip.append(index[m] // 4)
                    if n > 0:
                        if pip[n-1] == pip[n]:
                            pairs += 1; print("pair")
                    n+=1
                if total == 15:
                    fifteens += 1; print("2x15")         

        if cards > 2:
            # sets of 5
            if cards == 5:             
                total = 0
                run = 1
                flush = 1
                runner.clear()
                suit.clear()
                for i in range(cards):
                    total += values[index[i] // 4]
                    runner.append(runOrder[index[i] // 4])
                    suit.append(index[i] % 4)
                    if i > 0:
                        if runner[i-1] == runner[i]-1:
                            run+=1
                        if suit[i-1] == suit[i]:
                            flush+=1
                                         
                if total == 15:
                    fifteens+=1; print("5x15")
                if run == 5:
                    runsof5+=1; print("run5")
                if flush == 5:
                    flush5+=1; print("fl5")

            # sets of 4
            for i in range(cards-3):
                for j in range(i+1, cards-2):
                    for k in range(j+1, cards-1):
                        for l in range(k+1, cards):
                            total = 0
                            run = 1
                            flush = 1
                            runner.clear()
                            suit.clear()
                            n = 0
                            for m in [i,j,k,l]:
                                total += values[index[m] // 4]
                                runner.append(runOrder[index[m] // 4])
                                suit.append(index[m] % 4)
                                if n > 0:
                                    if runner[n-1] == runner[n]-1 and not runsof5:
                                        run+=1
                                    if suit[n-1] == suit[n] and not flush5:
                                        flush+=1
                                n+=1
                                
                            if total == 15:
                                fifteens+=1; print("4x15", hand)
                            if run == 4:
                                runsof4+=1; print("run4", runner)
                            if flush == 4:
                                flush4+=1; print("fl4", suit)

            # sets of 3
            for i in range(cards-2):
                for j in range(i+1, cards-1):
                    for k in range(j+1, cards):
                        total = 0
                        run = 1
                        runner.clear()
                        n = 0
                        for m in [i,j,k]:
                            total += values[index[m] // 4]
                            runner.append(runOrder[index[m] // 4]); 
                            if n > 0:
                                if runner[n-1] == runner[n]-1 and not runsof4 and not runsof5:
                                    run+=1; 
                            n+=1
                            
                        if total == 15:
                            fifteens+=1; print("3x15")
                        if run == 3:
                            runsof3+=1; print("3run")
                
        # check if crib, if yes only count flush5        
        if crib:
            flush4 = 0

        # check for nibs
        """
        if common_card >= 0:
            for i in range(cards):
        """
        
        #print(hand)
        #print("2s",pairs,"15s",fifteens,"r3",runsof3,"r4",runsof4,"r5",runsof5,"f4",flush4,"f5",flush5)
        score = pairs*2 + fifteens*2 + runsof3*3 + runsof4*4 + runsof5*5 + flush4*4 + flush5*5
        return score
    else:
        return -1

# FUNCTION for scoring a hand
# parameters:
#   common_card:
#     card added to hand; i.e. turned card or 'what if' card
#     index of common card or -1 if no common card 
#   diff:
#     difficulty of game as selected by user/player
#     used to djfheufhvnoIJ

def Score2(hand_array, common_card, cards, diff, crib, values, runOrder):

    if cards >= 2 and cards <= 5:
        index = hand_array[0]; #print("SCindex",index)
        hand = hand_array[1]; #print("SChand",hand)
        pairs = 0
        fifteens = 0
        runsof3 = 0
        runsof4 = 0
        runsof5 = 0
        flush4 = 0
        flush5 = 0
        nibs = 0
        pip = []
        runner = []
        suit = []
            
        # sets of 2
        for i in range(cards-1):
            for j in range(i+1, cards):
                total = 0
                pip.clear()
                n = 0
                for m in (i,j):
                    total += values[int(index[m]) // 4]
                    pip.append(index[m] // 4)
                    if n > 0:
                        if pip[n-1] == pip[n]:
                            pairs += 1; print("pair")
                    n+=1
                if total == 15:
                    fifteens += 1; print("2x15")         

        if cards > 2:
            # sets of 5
            if cards == 5:             
                total = 0
                run = 1
                flush = 1
                runner.clear()
                suit.clear()
                for i in range(cards):
                    total += values[index[i] // 4]
                    runner.append(runOrder[index[i] // 4])
                    suit.append(index[i] % 4)
                    if i > 0:
                        if runner[i-1] == runner[i]-1:
                            run+=1
                        if suit[i-1] == suit[i]:
                            flush+=1
                                         
                if total == 15:
                    fifteens+=1; print("5x15")
                if run == 5:
                    runsof5+=1; print("run5")
                if flush == 5:
                    flush5+=1; print("fl5")

            # sets of 4
            for i in range(cards-3):
                for j in range(i+1, cards-2):
                    for k in range(j+1, cards-1):
                        for l in range(k+1, cards):
                            total = 0
                            run = 1
                            flush = 1
                            runner.clear()
                            suit.clear()
                            n = 0
                            for m in [i,j,k,l]:
                                total += values[index[m] // 4]
                                runner.append(runOrder[index[m] // 4])
                                suit.append(index[m] % 4)
                                if n > 0:
                                    if runner[n-1] == runner[n]-1 and not runsof5:
                                        run+=1
                                    if suit[n-1] == suit[n] and not flush5:
                                        flush+=1
                                n+=1
                                
                            if total == 15:
                                fifteens+=1; print("4x15", hand)
                            if run == 4:
                                runsof4+=1; print("run4", runner)
                            if flush == 4:
                                flush4+=1; print("fl4", suit)

            # sets of 3
            for i in range(cards-2):
                for j in range(i+1, cards-1):
                    for k in range(j+1, cards):
                        total = 0
                        run = 1
                        runner.clear()
                        n = 0
                        for m in [i,j,k]:
                            total += values[index[m] // 4]
                            runner.append(runOrder[index[m] // 4]); 
                            if n > 0:
                                if runner[n-1] == runner[n]-1 and not runsof4 and not runsof5:
                                    run+=1; 
                            n+=1
                            
                        if total == 15:
                            fifteens+=1; print("3x15")
                        if run == 3:
                            runsof3+=1; print("3run")
                
        # check if crib, if yes only count flush5        
        if crib:
            flush4 = 0

        # check for nibs
        """
        if common_card >= 0:
            for i in range(cards):
        """
        
        #print(hand)
        #print("2s",pairs,"15s",fifteens,"r3",runsof3,"r4",runsof4,"r5",runsof5,"f4",flush4,"f5",flush5)
        score = pairs*2 + fifteens*2 + runsof3*3 + runsof4*4 + runsof5*5 + flush4*4 + flush5*5
        return score
    else:
        return -1


# FUNCTION for sorting a list of Cards (see Card class)
# parameters:
#   hand: list of Cards
#   cards: number of Cards in list / number of Cards to be sorted
#   ascending: True if sorting in scending order

def Sort(hand, cards, ascending):

    if ascending:
        for i in range(cards-1):
            for j in range(i+1, cards):
                print("Sort:",i,j)
                print("Sort",hand[i].name,hand[j].name)
                if hand[i].index > hand[j].index:
                    hand[i], hand[j] = hand[j], hand[i]
        
        return hand
    
    else:
        return -1

def Show(hand, cards):
    
    for i in range(cards):
        print("Show card",i,hand[i].name,hand[i].index)
        
def Sort2(card_array, cards, sort_type):

    index = card_array[0]
    hand = card_array[1]
    if sort_type == 0: # sort ascending
        for i in range(cards-1):
            for j in range(i+1, cards):
                if index[i] > index[j]:
                    index[i], index[j] = index[j], index[i]
                    hand[i], hand[j] = hand[j], hand[i]
        
        return [index, hand]
    
    else:
        return [[],[]]
        
