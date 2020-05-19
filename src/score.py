# logic for scoring a hand
def Score2(hand, common_card, cards, diff, crib, values, runOrder):

    if cards >= 2 and cards <= 5:
        
        pairs = 0
        fifteens = 0
        runsof3 = 0
        runsof4 = 0
        runsof5 = 0
        flush4 = 0
        flush5 = 0
            
        # sets of 2
        for i in range(cards-1):
            for j in range(i+1, cards):
                total = 0
                pip = []
                n = 0
                for m in (i,j):
                    total += values[hand[m] // 4]
                    pip.append(hand[m] // 4)
                    if n > 0:
                        if pip[n-1] == pip[n]-1:
                            pairs += pairs; #print("pair")
                    n+=1
                if total == 15:
                    fifteens += 1; #print("2x15")         

        if cards > 2:
            # sets of 5
            if cards == 5:             
                total = 0
                run = 1
                flush = 1
                runner = []
                suit = []
                for i in range(cards):
                    total += values[hand[i] // 4]
                    runner.append(runOrder[hand[i] // 4])
                    suit.append(hand[i] % 4)
                    if i > 0:
                        if runner[i-1] == runner[i]-1:
                            run+=1
                        if suit[i-1] == suit[i]:
                            flush+=1
                                         
                if total == 15:
                    fifteens+=1; #print("5x15")
                if run == 5:
                    runsof5+=1; #print("run5")
                if flush == 5:
                    flush5+=1; #print("fl5")

            # sets of 4
            for i in range(cards-3):
                for j in range(i+1, cards-2):
                    for k in range(j+1, cards-1):
                        for l in range(k+1, cards):
                            total = 0
                            run = 1
                            flush = 1
                            runner = []
                            suit = []
                            n = 0
                            for m in [i,j,k,l]:
                                total += values[hand[m] // 4]
                                runner.append(runOrder[hand[m] // 4])
                                suit.append(hand[m] % 4)
                                if n > 0:
                                    if runner[n-1] == runner[n]-1 and not runsof5:
                                        run+=1
                                    if suit[n-1] == suit[n] and not flush5:
                                        flush+=1
                                n+=1
                                
                            if total == 15:
                                fifteens+=1; #print("4x15", hand)
                            if run == 4:
                                runsof4+=1; #print("run4", runner)
                            if flush == 4:
                                flush4+=1; #print("fl4", suit)

            # sets of 3
            for i in range(cards-2):
                for j in range(i+1, cards-1):
                    for k in range(j+1, cards):
                        total = 0
                        run = 1
                        runner = []
                        n = 0
                        for m in [i,j,k]:
                            total += values[hand[m] // 4]
                            runner.append(runOrder[hand[m] // 4]); #print(l, n, runner)
                            if n > 0:
                                if runner[n-1] == runner[n]-1 and not runsof4 and not runsof5:
                                    run+=1; #print("run",run)
                            n+=1
                            
                        if total == 15:
                            fifteens+=1; #print("3x15")
                        if run == 3:
                            runsof3+=1; #print("3run")
                
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


