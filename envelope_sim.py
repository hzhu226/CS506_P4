import random

def pick_envelope(switch, verbose):
    ball = ["b", "b", "b", "r"]
    enve_1 = random.sample(ball, 2)
    if "r" in enve_1:
        enve_2 = ["b", "b"]
    else:
        ballLeft = ["b", "r"]
        enve_2 = random.sample(ballLeft, 2)
    enves = [enve_1, enve_2]
    random.shuffle(enves)
    enveSelec = enves.pop()
    if enveSelec == enve_1:
        pick = 0
        left = 1
    else:
        pick = 1
        left = 0
    ballSelec = random.choice(enveSelec)
    if ballSelec == "b":
        if switch == False:
            if verbose == True:
                print("Envelope 0: " + enve_1[0] + " " + enve_1[1])
                print("Envelope 1: " + enve_2[0] + " " + enve_2[1])
                print("I picked envelope " + str(pick))
                print("and drew a " + ballSelec)
            if "r" in enveSelec:
                return True
            else:
                return False
        if switch == True:
            enveLeft = enves.pop()
            if verbose == True:
                print("Envelope 0: " + enve_1[0] + " " + enve_1[1])
                print("Envelope 1: " + enve_2[0] + " " + enve_2[1])
                print("I picked envelope " + str(pick))
                print("and drew a " + ballSelec)
                print("Switch to envelope " + str(left))
            if "r" in enveLeft:
                return True
            else:
                return False

    if ballSelec == "r":
        if verbose == True:
            print("Envelope 0: " + enve_1[0] + " " + enve_1[1])
            print("Envelope 1: " + enve_2[0] + " " + enve_2[1])
            print("I picked envelope " + str(pick))
            print("and drew a " + ballSelec)
        return True

def run_simulation(n):
    win = 0
    verbose = False

    print("After " + str(n) + " simulations:")
    for i in range(n):
        if pick_envelope(True, verbose) == True:
            win = win + 1
    print("  Switch successful: {:.2%}".format(win / n))

    win = 0
    for i in range(n):
        if pick_envelope(False, verbose) == True:
            win = win + 1
    print("  No-switch successful: {:.2%}".format(win / n))
