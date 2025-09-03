# Program: AKing'sQuest.py
# Date: 10/1/13
# Programmer: Matthew Shammami
# Description: A king's castle has been captured by an enemy army, he must get the legendary
#               Z-sword to fight off the enemy and recover his castle.

import random

def movement():
    compass = raw_input("Which direction would you like to search? (north, east, west)")
    compass = compass.lower()
    return compass
# AB = after battle and DB = during battle
def movesAB():
    move = raw_input("What would you like to do? (c for continue, p for drink health potion, or l for loot)")
    move = move.lower()
    return move

def movesDB():
    move = raw_input("What would you like to do? (a for attack or p for drink health potion)")
    move = move.lower()
    return move

# battle command
def battle():
    global health
    global healthpots
    global ehealth
    global loss
    print "You have entered a battle."
    while ehealth > 0 and health > 0:
        fight = movesDB()
        if fight == "a":
            Ddamage()
            Tdamage()
        elif fight == "p":
            if healthpots > 0:
                healthpotion()
                healthpots = healthpots - 1
                print "You now have", healthpots, "health potion(s)"
            else:
                print "You don't have any health potions!"
        else:
            print "Invalid input."
    checkloss()

def bossbattle():
    global health
    global healthpots
    global bosshealth
    global loss
    print "You have entered the boss battle."
    while bosshealth > 0 and health > 0:
        fight = movesDB()
        if fight == "a":
            Bdamage()
            Tdamage()
        elif fight == "p":
            if healthpots > 0:
                healthpotion()
                healthpots = healthpots - 1
                print healthpots
                print "You now have", healthpots, "health potion(s)"
            else:
                print "You don't have any health potions!"
        else:
            print "Invalid input."
    checkloss()
def continuation():
    move = movesAB()
    global healthpots
    randomnumber = 0
    randomnumber = randomnum()
    lootpass = 0
    while move != "c":
        if move == "p" :
            if healthpots > 0:
                healthpotion()
                healthpots = healthpots - 1
                print "You now have", healthpots, "health potion(s)"
            else:
                print "You don't have any health potions!"
        elif move == "l":
            if randomnumber == 1 and lootpass == 0:
                healthpots += 1
                lootpass += 1
                print "You have found a health potion, you know have:", healthpots, "health potions."
            elif lootpass == 1:
                print "You already looted the dead body!"
            else:
                print "You find nothing."
        else:
            print "Invalid entry."
        move = movesAB()

def healthpotion():
    global health
    health = health + 40
    print "Your health is:", health
    return health

# t is for taken and d is for dealt
def Tdamage():
    global health
    randomnumber = randomnum()
    if "shield" in inventory:
        if randomnumber == 0 or randomnumber == 3:
            health = health - 10
        elif randomnumber == 1:
            health = health - 5
        elif randomnumber == 2:
            print "You blocked the enemy's attack!"
    else:
        if randomnumber == 0 or randomnumber == 3 or randomnumber == 1:
            health = health - 10
        elif randomnumber == 2:
            print "The enemy missed its attack!"

    print "Your health is:", health
    return health

def Ddamage():
    global ehealth
    randomnumber = randomnum()
    if "dull sword" in inventory:
        if randomnumber == 1 or randomnumber == 2:
            ehealth = ehealth - 10
        elif randomnumber == 0:
            ehealth = ehealth - 5
        elif randomnumber == 3:
            print "You missed your attack."
    elif "sharp sword" in inventory:
        if randomnumber == 0 or randomnumber == 1:
            ehealth = ehealth - 10
        elif randomnumber == 2 or randomnumber == 3:
            ehealth = ehealth - 5
    print "The enemy's health is:", ehealth
    return ehealth

# your damage on the boss
def Bdamage():
    global bosshealth
    bosshealth = bosshealth - 10
    print "The boss's health is:", bosshealth
    return bosshealth

def ehealthL1():
    global ehealth
    ehealth = 30
    return ehealth

def ehealthL2():
    global ehealth
    ehealth = 40
    return ehealth

def ehealthL3():
    global ehealth
    ehealth = 60
    return ehealth

def randomnum():
    randomnumber = random.randrange(4)
    return randomnumber

def checkloss():
    global loss
    if health <= 0:
        loss = loss + 1
        return loss
def sidequest():
    global healthpots
    rannumber = random.randrange(10) + 1
    tries = 1
    win = 0
    print "Guess a number 1-10"
    guess = int(raw_input("Take a guess: "))
    while (guess != rannumber):
        if tries == 3:
            win += 1
            break
        elif (guess > rannumber):
            print "Lower..."
            print "Tries left:", 2 - tries
        else:
            print "Higher..."
            print "Tries left: ", 2 - tries
        guess = int(raw_input("Take a guess: "))
        tries += 1
    if win == 0:
        print "You guessed it!"
        healthpots += 2
        print "You now have", healthpots, "health potion(s)"
    elif win == 1:
        print "You ran out of tries. No health potions for you."
    return healthpots

# begging variables
health = 100
healthpots = 3
inventory = ["health potion"]
ehealth = 0
loss = 0
bosshealth = 100

# open the beggining story and print it
Backstory = open("beginning.txt", "r")
Bstory = Backstory.read()
print Bstory
Backstory.close()
raw_input("Press the enter key to continue.")
# get sword and get out of the room 
# this is used to force character to stay on track of story

compass = movement()

while compass != "east":
    if compass == "north":
        print "You need to get a weapon first. Keep searching in another direction."
    elif compass == "west":
        print "You need to get a weapon first. Keep searching in another direction."
    else:
        print "Invalid answer."
    compass = movement()
print "You found the sword!"
inventory.append("dull sword")
print "It a little dull but it will do. This is your inventory:", inventory, "You walk to the door right as a knight breaks through," \
      "You are going to have to fight for you life, hopefully the sword will do some damage!"

# battle 
while health > 0:
    ehealthL1()
    battle()
    break
while health > 0:
    continuation()
    print "You walk down the corridor."
    ehealthL1()
    battle()
    break
while health > 0:
    continuation()
    print "You walk down the corridor and encounter another enemy."
    ehealthL1()
    battle()
    break
while health > 0:
    continuation()
    print "You find the end of the corridor and climb down the stairs."
    raw_input("Press the enter key to continue.")
    print "You climb down the stairs, but the knights you see are better armed than the others you faught. "\
          "You see one that is not as well armed, you better kill him and steal his shield if you want to have a chance to defeat the others."
    raw_input("Press the enter key to continue.")
    print "You charge towards the weak knight."
    ehealthL1()
    battle()
    break
while health > 0:
    continuation()
    inventory.append("shield")
    print "You take his shield.", inventory, "But one of the more heavily armed vanguards spots you and is rushing towards you."
    ehealthL2()
    battle()
    break
while health > 0:
    continuation()
    print "You have found a side quest, here is a chance to win 2 health potions."
    sidequest()
    raw_input("Press the enter key to continue.")
    print "Only one more floor to go then i'll be in the basement. Just have to take out this last guy."
    ehealthL2()
    battle()
    break
while health > 0:
    continuation()
    print "You catch a glimpse of a shiny metal.\nYou look down and shuffle the dirt around the metal. " \
        "You find a sharpened sword that was once weilded by Arthur, your best knight. " \
        "You take it, knowing that it will come to good use.\n "
    inventory[1] = "sharp sword"
    print inventory
    print "You climb down the stairs."
    raw_input("Press the enter key to continue.")
    break
while health > 0:
    print "Another enemy, time to put this sword to good use."
    ehealthL3()
    battle()
    break
while health > 0:
    continuation()
    print "One last vangaurd to take out and then i'll be able to get the 'Z sword'."
    ehealthL3()
    battle()
    break
while health > 0:
    continuation()
    print "You climb down into the basement. It's very dark down here. You must find a button that will raise the 'Z sword' out of the chamber. "\
          "Enter a direction in which you would like to search."
    button = movement()
    while button != "west":
        if button == "north":
            print "You search the wall but come up short. Keep searching in another direction."
        elif compass == "east":
            print "You search the wall but don't find anything. Keep searching in another direction."
        else:
            print "Invalid answer."
        button = movement()
    inventory[1] = ("Z sword")
    raw_input("Press the enter key to activate the button.")
    print "You found the button. You hear a loud crash and gears begin to turn. The 'Z sword' begins to raise out of the center of the room. "\
          "A spotlight is shining on it. As you go to grab the sword, you hear an explosion. Vegeta, the enemy king, comes crawling through the hole in the wall. "\
          "You grab the sword", inventory, "and begin to rush to Vegeta. He is heavily armored. If you defeat him you'll have your castle back. "\
          "If you don't... well you dont want to find out."
    raw_input("Press the enter key to continue.")
    bossbattle()
    break

if loss == 1:
    print "You lost, your kindom has been taken over by the enemy."
else:
    print "You win! You have recovered your castle. But the war is not over, you must continue forward and recover your kingdom."



raw_input("Thank you for playing! Press the enter key to exit.")








