from classes.game import Person, BColors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 40, 5000, "white")


# Create some Items
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals for 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals for 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]


# Instantiate Players
player1 = Person("Valos  ", 3260, 135, 300, 34, player_spells, player_items)
player2 = Person("Marcus ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot  ", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp    ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus  ", 11200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp    ", 1250, 130, 560, 325, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
t = 3
defeated_enemies = 0
defeated_players = 0
print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" + BColors.ENDC)

while running:


    print("======================================================================================")

    print("\n")
    print(BColors.BOLD + " NAME                            HP                              MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("\n", "You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
                defeated_enemies += 1

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(BColors.FAIL + "\nNot enough MP\n" + BColors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(BColors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + BColors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(BColors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                    defeated_enemies += 1

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(BColors.FAIL + "\n" + "None left..." + BColors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(BColors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + BColors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(BColors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + BColors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(BColors.FAIL + "\n" + str(item.name) + " deals " + str(item.prop) + " points of damage to "
                      + enemies[enemy].name.replace(" ", "") + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                    defeated_enemies += 1

    # Check if player won
    if defeated_enemies >= 3:
        print(BColors.OKGREEN + "You win!" + BColors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack

            target = random.randrange(0, t)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print("\n", enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "")
                  + " for", enemy_dmg, "points of damage.")

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]
                t -= 1
                defeated_players += 1

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            spell = enemy.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            enemy.reduce_mp(spell.cost)

            pct = enemy.hp / enemy.maxhp * 100

            if enemy.mp < spell.cost or spell.type == "white" and pct > 50:
                continue

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(BColors.OKBLUE + "\n" + spell.name + " heals " + enemy.name.replace(" ", "") + " for",
                      str(magic_dmg), "HP." + BColors.ENDC)

            elif spell.type == "black":

                target = random.randrange(0, t)

                players[target].take_damage(magic_dmg)

                print(BColors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + BColors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
                    t -= 1
                    defeated_players += 1

    # Check if enemy won
    if defeated_players >= 3:
        print(BColors.FAIL + "Your enemies have defeated you!" + BColors.ENDC)
        running = False

