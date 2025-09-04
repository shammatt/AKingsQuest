# Program: AKing'sQuest.py
# Date: 9/2/25
# Programmer: Matthew Shammami
# Description: A king's castle has been captured by an enemy army, he must get the legendary
#               Z-sword to fight off the enemy and recover his castle.
import json
import random
import sys


def print_single_line(text):
    print(text)
    input("Press the enter key to continue.")


class Player:
    def __init__(self):
        self.health = 100
        self.health_potions = 1
        self.sword = 'dull'
        self.shield = False

    def add_potions(self, potions=1):
        self.health_potions += potions
        print("You now have {self.health_potions} health potion(s)")

    def attack(self):
        """Deal 10 damage with dull sword 50% of the time, and miss or 5 damage the other 50%
           Deal 10 damage or 5 damage 50% of the time with the sharp sword
           Always deal 10 damage with the Z sword
        """
        if self.sword == 'z':
            return 10

        chance = random.random()
        if self.sword == 'sharp':
            return 10 if chance >= 0.5 else 5
        elif 0 <= chance <= 0.25:
            return 0
        elif 0.5 < chance <= 0.75:
            return 5
        else:
            return 10 

    def damage(self, hit):
        if hit == 0:
            print("The enemy missed their attack.")
            return

        if self.shield:
            # 25% chance to block the attack or 50% chance to take half damage
            chance = random.random()
            if chance >= 0.75:
                print("You blocked the enemy's attack!")
                return
            elif chance >= 0.5:
                hit = hit // 2

        self.health -= hit

    def heal(self):
        self.health += 40
        print("Your health is now:", self.health)

        self.health_potions -= 1
        print("You now have ", self.health_potions, " health potion(s) remaining.")

    def get_potions_available(self):
        return self.health_potions > 0

    def movement(self):
        valid_options = {'north', 'east', 'west'}

        direction = input("Which direction would you like to search? {valid_options}").lower()
        while direction not in valid_options:
            print("Incorrect Move. Please try again.")
            direction = input("Which direction would you like to search? {valid_options}").lower()

        return direction


class Enemy:
    health_options = [30, 40, 60, 100]
    boss_miss_factor = 0.1
    grunt_miss_factor = 0.24

    def __init__(self, level=0):
        self.health = Enemy.health_options[level]
        self.looted = False
        self.level = level
        self.miss_factor = Enemy.grunt_miss_factor if level < 3 else Enemy.boss_miss_factor
    
    def attack(self):
        return 10 if random.random() > self.miss_factor else 0

    def damage(self, hit):
        self.health -= hit

    def drop_potion(self):
        if not self.looted:
            self.looted = True
            return random.random() >= 0.67

        return False

    def reset(self, level):
        self.level = level
        self.health = self.health_options[self.level]
        self.looted = False
        self.miss_factor = Enemy.grunt_miss_factor if self.level < 3 else Enemy.boss_miss_factor


class Game:
    def __init__(self, text_data):
        self.player = Player()
        self.enemy = Enemy()
        self.level = 0
        self.story = text_data

    def battle(self):
        print("You have entered a battle.")

        self.enemy.reset(self.level)
        while self.player.health >= 0 and self.enemy.health >= 0:
            player_option = self.battle_phase_option()
            
            # Options are a and p, p only available if player has a potion
            if player_option == 'p':
                self.player.heal()
            elif player_option == "a":
                self.enemy.damage(self.player.attack())

            self.player.damage(self.enemy.attack())
            print("Your health is: {self.player.health}, The enemies health is: {self.enemy.health}")

        if self.player.health < 0:
            Game.loss()

    def battle_phase_option(self):
        """Move options during battle phase"""
        # Ensure player has a health potion
        if self.player.get_health_potions():
            text = "What would you like to do? (a for attack or p for drink health potion)"
            valid_options = {'a', 'p'}
        else:
            text = "What would you like to do? (a for attack)"
            valid_options = {'a'}

        option = input(text)
        while option not in valid_options:
            print("Incorrect Move. Please try again.")
            option = input(text)

        return option

    def continuation(self):
        option = None
        while option != 'c':
            option = self.continuation_options()
            if option == 'p':
                self.player.heal()
            elif option == 'l':
                if self.enemy.drop_potion():
                    self.player.add_potions()


    def continuation_options(self):
        """Move options after battle phase"""
        valid_options = {'c'}
        text = "What would you like to do? (c for continue"
        # Ensure player has a health potion
        if self.player.get_health_potions():
            text += ", p for drink health potion"
            valid_options.add('p')
        elif not self.enemy.looted:
            text += ", l for loot"
            valid_options.add('l')

        text += ')'

        option = input(text).lower()
        while option not in valid_options:
            print("Incorrect Move. Please try again.")
            option = input(text).lower()

        return option

    def find_sword(self):
        # Small guessing game
        correct_direction = random.choice(['north', 'east', 'west'])
        while self.player.movement() != correct_direction:
                print("You did not find your weapon. Keep searching in another direction.")
        
        self.print_story('bedroom_search')

    def found_shield(self):
        self.player.shield = True

    def loss():
        print("Your health fell to 0. Your kindom has been taken over by the enemy.")
        input("Thank you for playing! Press the enter key to exit.")
        sys.exit(1)

    def print_story(self, key):
        for line in self.story[key]:
            print(line)
        input("Press the enter key to continue.")

    def set_level(self, level):
        self.level = level

    def side_quest(self):
        rannumber = random.randrange(10) + 1
        tries = 3

        print("Guess a number 1-10")
        while tries > 0:
            try:
                guess = int(input("Take a guess: "))
            except:
                print("Invalid input. You have lost a try.")
                tries -= 1
                continue

            if guess == rannumber:
                self.player.add_potions(2)
                print_single_line("You guessed it!")
                return
            elif guess > rannumber:
                print("Lower...")
            else:
                print("Higher...")

            tries -= 1
            print("Tries left:", tries)

        print_single_line("You ran out of tries. No health potions for you.")


def main():
    # Open the story and store in var
    try:
        with open('story.json', 'r') as file:
            text_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file  is not a valid JSON file.")
        return

    # Set up Game instance
    game = Game(text_data)

    # Display intro sequence
    game.print_story('intro_sequence')

    # Get sword and get out of the room 
    game.find_sword()

    text = ["You are going to have to fight for you life, hopefully the sword will do some damage!",
            "You walk down the corridor.",
            "You continue down the corridor and encounter another enemy."]

    # Fight 3 enemies at level 0; 30 HP
    for i in range(4):
        if i < 3:
            print(text[i])
        elif i == 3:
            print_single_line("You find the end of the corridor and climb down the stairs.")
            game.print_story('level_two_start')

        game.battle()
        game.continuation()

    # Shield found, enemies have more health
    game.found_shield()
    game.set_level(1)

    text = ["You take his shield. However one of the more heavily armed vanguards spots you and is rushing towards you.",
            "Only one more floor to go then i'll be in the basement. Just have to take out this last guy."]

    for i in range(2):
        if i == 1:
            game.side_quest()

        print(text[i])

        game.battle()
        game.continuation()




    print("You win! You have recovered your castle. But the war is not over, you must continue forward and recover your kingdom.")
    input("Thank you for playing! Press the enter key to exit.")


if __name__ == "__main__":
    main()


"""
while health > 0:
    continuation()
    print("You find the end of the corridor and climb down the stairs."
    input("Press the enter key to continue.")
    print("You climb down the stairs, but the knights you see are better armed than the others you faught. "\
          "You see one that is not as well armed, you better kill him and steal his shield if you want to have a chance to defeat the others."
    input("Press the enter key to continue.")
    print("You charge towards the weak knight."
    ehealthL1()
    battle()
    break
while health > 0:
    continuation()
    inventory.append("shield")
    print("You take his shield.", inventory, "But one of the more heavily armed vanguards spots you and is rushing towards you."
    ehealthL2()
    battle()
    break
while health > 0:
    continuation()
    print("You have found a side quest, here is a chance to win 2 health potions."
    sidequest()
    input("Press the enter key to continue.")
    print("Only one more floor to go then i'll be in the basement. Just have to take out this last guy."
    ehealthL2()
    battle()
    break
while health > 0:
    continuation()
    print("You catch a glimpse of a shiny metal.\nYou look down and shuffle the dirt around the metal. " \
        "You find a sharpened sword that was once weilded by Arthur, your best knight. " \
        "You take it, knowing that it will come to good use.\n "
    inventory[1] = "sharp sword"
    print(inventory
    print("You climb down the stairs."
    input("Press the enter key to continue.")
    break
while health > 0:
    print("Another enemy, time to put this sword to good use."
    ehealthL3()
    battle()
    break
while health > 0:
    continuation()
    print("One last vangaurd to take out and then i'll be able to get the 'Z sword'."
    ehealthL3()
    battle()
    break
while health > 0:
    continuation()
    print("You climb down into the basement. It's very dark down here. You must find a button that will raise the 'Z sword' out of the chamber. "\
          "Enter a direction in which you would like to search."
    button = movement()
    while button != "west":
        if button == "north":
            print("You search the wall but come up short. Keep searching in another direction."
        elif compass == "east":
            print("You search the wall but don't find anything. Keep searching in another direction."
        else:
            print("Invalid answer."
        button = movement()
    inventory[1] = ("Z sword")
    input("Press the enter key to activate the button.")
    print("You found the button. You hear a loud crash and gears begin to turn. The 'Z sword' begins to raise out of the center of the room. "\
          "A spotlight is shining on it. As you go to grab the sword, you hear an explosion. Vegeta, the enemy king, comes crawling through the hole in the wall. "\
          "You grab the sword", inventory, "and begin to rush to Vegeta. He is heavily armored. If you defeat him you'll have your castle back. "\
          "If you don't... well you dont want to find out."
    input("Press the enter key to continue.")
    bossbattle()
    break
"""
