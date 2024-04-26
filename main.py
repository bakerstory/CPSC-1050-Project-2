# Baker Story
# CPSC 1050
# Project 2: RPG
# 4/25/2024
# Section: 001
# Github link: https://github.com/bakerstory/CPSC-1050-Project-2/blob/main/main.py
# Description:"Shadows of the Shogunate" is a text-based game where players take on the role of a Samurai navigating through battles and clan politics. The game features combat, clan management, a navigable map, and persistent game states through save/load functionalities.




import json  # Importing the JSON module for file I/O
import random  # Importing the random module for generating random numbers

# Class for Characters
class Character:
    def __init__(self, name, role, hp, attack, honor=50):
        self.name = name  # Character's name
        self.role = role  # Character's role (e.g., Samurai, Ninja)
        self.hp = hp  # Character's hit points
        self.attack = attack  # Character's attack power
        self.honor = honor  # Character's honor points

    def display_info(self):
        return f"{self.name} - Role: {self.role}, HP: {self.hp}, Attack: {self.attack}, Honor: {self.honor}"  # Display character information

    def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack)  # Generate random damage
        enemy.hp -= damage  # Reduce enemy's hit points
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")  # Print attack message

    def gain_honor(self, amount):
        self.honor += amount  # Increase honor points
        print(f"{self.name} gains {amount} honor.")  # Print honor gain message

    def lose_honor(self, amount):
        self.honor -= amount  # Decrease honor points
        print(f"{self.name} loses {amount} honor.")  # Print honor loss message

# Inheriting Character class for Samurai
class Samurai(Character):
    def __init__(self, name):
        super().__init__(name, "Samurai", 100, 20)  # Initialize Samurai with specific attributes

# Class for Clan
class Clan:
    def __init__(self, name, allies=None, enemies=None):
        self.name = name  # Clan's name
        self.allies = allies if allies else []  # List of ally clans
        self.enemies = enemies if enemies else []  # List of enemy clans

    def add_ally(self, clan):
        self.allies.append(clan)  # Add a clan to allies list

    def add_enemy(self, clan):
        self.enemies.append(clan)  # Add a clan to enemies list

# Class for Map
class Map:
    def __init__(self, size):
        self.size = size  # Size of the map
        self.tiles = [['.' for _ in range(size)] for _ in range(size)]  # Initialize map tiles with '.'
        self.player_position = (0, 0)  # Player's initial position on the map

    def display_map(self):
        for row in self.tiles:
            print(" ".join(row))  # Display map tiles

    def move_player(self, direction):
        x, y = self.player_position  # Get current player position
        if direction == "up" and x > 0:
            x -= 1  # Move player up
        elif direction == "down" and x < self.size - 1:
            x += 1  # Move player down
        elif direction == "left" and y > 0:
            y -= 1  # Move player left
        elif direction == "right" and y < self.size - 1:
            y += 1  # Move player right
        self.player_position = (x, y)  # Update player's position

# Game class
class ShadowsOfTheShogunate:
    def __init__(self):
        self.player = None  # Initialize player
        self.map = Map(5)  # Initialize map with size 5x5
        self.characters = []  # List of game characters
        self.clan = Clan("Tokugawa")  # Initialize player's clan

    def create_player(self):
        name = input("Enter your character's name: ")  # Input player's name
        role = input("Choose your role (Samurai, Ninja, Monk, Ronin): ")  # Input player's role
        if role.lower() == "samurai":
            self.player = Samurai(name)  # Create Samurai player
            self.clan.add_ally(self.clan)  # Add player's clan as an ally

    def display_menu(self):
        print("\nMenu:")  # Display menu options
        print("1. Display Characters")
        print("2. Display Clan Status")
        print("3. Combat")
        print("4. Move on Map")
        print("5. Save Game")
        print("6. Load Game")
        print("7. Exit")

    def menu_choice(self):
        while True:
            choice = input("Enter the number for your choice: ").strip()  # Get menu choice
            
            # Handle menu choices
            if choice == "1":
                self.display_characters()
                break
            elif choice == "2":
                self.display_clan_status()
                break
            elif choice == "3":
                self.combat()
                break
            elif choice == "4":
                self.move_on_map()
                break
            elif choice == "5":
                self.save_game()
                break
            elif choice == "6":
                self.load_game()
                break
            elif choice == "7":
                exit()
            else:
                print("Invalid choice. Please try again.")  # Print error message for invalid choice

    def add_character(self, character):
        self.characters.append(character)  # Add a character to the game

    def display_characters(self):
        for character in self.characters:
            print(character.display_info())  # Display character information

    def display_clan_status(self):
        print(f"Clan {self.clan.name} - Allies: {', '.join([ally.name for ally in self.clan.allies])}, Enemies: {', '.join([enemy.name for enemy in self.clan.enemies])}")  # Display clan status

    def combat(self):
        enemy = random.choice(self.characters)  # Choose a random enemy
        print(f"Battle begins! {self.player.name} vs {enemy.name}")  # Print battle message
        
        while self.player.hp > 0 and enemy.hp > 0:
            self.player.attack_enemy(enemy)  # Player attacks enemy
            if enemy.hp > 0:
                enemy.attack_enemy(self.player)  # Enemy attacks player
        
        if self.player.hp > 0:
            print(f"{self.player.name} wins the battle!")  # Print win message
            self.player.gain_honor(10)  # Gain honor
        else:
            print(f"{self.player.name} loses the battle!")  # Print lose message
            self.player.lose_honor(5)  # Lose honor

    def move_on_map(self):
        direction = input("Enter direction (up, down, left, right): ").strip().lower()  # Get direction input
        self.map.move_player(direction)  # Move player on the map
        print(f"You moved to position: {self.map.player_position}")  # Print new position

    def save_game(self):
        data = {
            "player": {
                "name": self.player.name,
                "role": self.player.role,
                "hp":self.player.hp,
                "attack": self.player.attack,
                "honor": self.player.honor
            },
            "characters": [char.__dict__ for char in self.characters],  # Save characters' attributes
            "clan": {
                "name": self.clan.name,
                "allies": [ally.name for ally in self.clan.allies],  # Save ally clan names
                "enemies": [enemy.name for enemy in self.clan.enemies]  # Save enemy clan names
            },
            "map": {
                "size": self.map.size,
                "player_position": self.map.player_position  # Save player's position on the map
            }
        }
        with open("save_game.json", "w") as file:
            json.dump(data, file)  # Save game data to a JSON file

    def load_game(self):
        with open("save_game.json", "r") as file:
            data = json.load(file)  # Load game data from JSON file
            self.player = Character(data["player"]["name"], data["player"]["role"], data["player"]["hp"], data["player"]["attack"], data["player"]["honor"])  # Create player from saved data
            self.characters = [Character(char["name"], char["role"], char["hp"], char["attack"], char["honor"]) for char in data["characters"]]  # Create characters from saved data
            
            # Initialize clan with saved data
            self.clan = Clan(data["clan"]["name"])
            self.clan.allies = [Clan(ally) for ally in data["clan"]["allies"]]
            
            # Initialize enemies for the clan
            self.clan.enemies = []
            for enemy_name in data["clan"]["enemies"]:
                for char in self.characters:
                    if char.name == enemy_name:
                        self.clan.enemies.append(char)
                        break

            # Initialize map with saved data
            self.map = Map(data["map"]["size"])
            self.map.player_position = tuple(data["map"]["player_position"])  # Set player's position from saved data

# Main game loop
def main():
    game = ShadowsOfTheShogunate()  # Create game instance
    
    # Game initialization
    game.create_player()  # Create player
    
    # Sample characters
    game.add_character(Samurai("Hanzo"))  # Add Samurai character
    game.add_character(Character("Yoshi", "Monk", 80, 15))  # Add Monk character

    while True:
        game.display_menu()  # Display game menu
        game.menu_choice()  # Get and process menu choice

if __name__ == "__main__":
    main()  # Start the game loop



