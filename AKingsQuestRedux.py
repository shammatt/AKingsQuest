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
        self.health = 150
        self.health_potions = 1
        self.sword = 'dull'
        self.shield = False

    def add_potions(self, potions=1):
        self.health_potions += potions
        print(f"You now have {self.health_potions} health potion(s).")

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
        elif 0 <= chance <= 0.2:
            print("You missed your attack.")
            return 0
        elif 0.2 < chance <= 0.4:
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
        print(f"Your health is now: {self.health}")

        self.health_potions -= 1
        print(f"You now have {self.health_potions} health potion(s) remaining.")

    def get_potions_available(self):
        return self.health_potions > 0

    def movement(self):
        valid_options = {'north', 'east', 'west'}

        direction = input(f"Which direction would you like to search? {valid_options} ").lower()
        while direction not in valid_options:
            print("Incorrect Move. Please try again.")
            direction = input(f"Which direction would you like to search? {valid_options} ").lower()

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
            return random.random() >= 0.6

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
        while self.player.health > 0 and self.enemy.health > 0:
            print(f"Your health is: {self.player.health}, The enemies health is: {self.enemy.health}")
            player_option = self.battle_phase_option()
            
            # Options are a and p, p only available if player has a potion
            if player_option == 'p':
                self.player.heal()
            elif player_option == "a":
                self.enemy.damage(self.player.attack())

            # If enemy is defeated, then you do not take damage
            if self.enemy.health > 0:
                self.player.damage(self.enemy.attack())

        if self.player.health <= 0:
            self.loss()

        print(f"You defeated the enemy. Your health is: {self.player.health}")

    def battle_phase_option(self):
        """Move options during battle phase"""
        # Ensure player has a health potion
        if self.player.get_potions_available():
            text = "What would you like to do? (a for attack or p for drink health potion) "
            valid_options = {'a', 'p'}
        else:
            text = "What would you like to do? (a for attack) "
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
                    print("You found a potion!")
                    self.player.add_potions()
                else:
                    print("You searched the body and did not find anything of value.")

        print()

    def continuation_options(self):
        """Move options after battle phase"""
        valid_options = {'c'}
        text = "What would you like to do? (c for continue"
        # Ensure player has a health potion
        if self.player.get_potions_available():
            text += ", p for drink health potion"
            valid_options.add('p')
        if not self.enemy.looted:
            text += ", l for loot"
            valid_options.add('l')

        text += ") "

        option = input(text).lower()
        while option not in valid_options:
            print("Incorrect Move. Please try again.")
            option = input(text).lower()

        return option

    def enemy_generator(self, num_enemies, text_key=None):
        """If we want to display text, each enemy should have an associated string"""
        text = self.story[text_key] if text_key else None
        for i in range(num_enemies):
            if text:
                print(text[i])

            self.battle()
            self.continuation()

    def found_shield(self):
        self.player.shield = True

    def guessing_game(self, objective):
        correct_direction = random.choice(['north', 'east', 'west'])
        while self.player.movement() != correct_direction:
                print(f"You did not find the {objective}. Keep searching in another direction. ")
        print()

    def loss(self):
        print("Your health fell to 0. Your kindom has been taken over by the enemy.")
        input("Thank you for playing! Press the enter key to exit.")
        sys.exit(1)

    def print_story(self, text_key):
        for line in self.story[text_key]:
            print(line)

    def set_level(self, level):
        self.level = level

    def side_quest(self):
        rannumber = random.randrange(10) + 1
        tries = 3

        print("You have found a side quest, here is a chance to win 2 health potions.")
        print("Guess a number 1-10")
        while tries > 0:
            try:
                guess = int(input("Take a guess: "))
            except:
                print("Invalid input. You have lost a try.")
                tries -= 1
                continue

            if guess == rannumber:
                print_single_line("You guessed it!")
                self.player.add_potions(2)
                return
            elif guess > rannumber:
                print("Lower...")
            else:
                print("Higher...")

            tries -= 1
            print(f"Tries left: {tries}, correct number: {guess}")

        print_single_line("You ran out of tries. No health potions for you.")

    def upgrade_sword(self, sword):
        self.player.sword = sword


def main():
    # Open the story and store in var
    try:
        with open('story.json', 'r') as file:
            text_data = json.load(file)
    except FileNotFoundError:
        print("Error: The file was not found.")
        return
    except json.JSONDecodeError:
        print("Error: The file  is not a valid JSON file.")
        return

    # Set up Game instance
    game = Game(text_data)

    # Display intro sequence
    game.print_story('intro_sequence')

    # Get sword and get out of the room 
    game.guessing_game('weapon')
    game.print_story('bedroom_search')

    # Fight 3 enemies at level 0
    game.enemy_generator(3, 'level_one')

    # Climb down to the next level
    game.print_story('level_two_start')
    game.enemy_generator(1)

    # Shield found, enemies have more health
    game.found_shield()

    # Increase dificulty
    game.set_level(1)

    # Fight 2 enemies at level 1
    game.enemy_generator(2, 'level_two')

    # Side quest for extra potions
    game.side_quest()

    game.print_story('level_three_start')

    # New sword
    game.upgrade_sword('sharp')

    # Fight 2 enemies at level 2 Enemy health
    game.set_level(2)
    game.enemy_generator(2, 'level_three')

    # Basement sequence
    game.print_story('basement')
    game.guessing_game('button')
    game.upgrade_sword('z')

    # Boss sequence
    game.set_level(3)
    game.print_story('boss')
    game.battle()

    print("\n!!!You win!!!\nYou have recovered your castle. But the war is not over, you must continue forward and recover your kingdom.")
    input("Thank you for playing! Press the enter key to exit.")


if __name__ == '__main__':
    main()
