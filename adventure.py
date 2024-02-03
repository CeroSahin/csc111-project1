"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

from game_data import World, Player

if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0, 30)

    menu = ["look", "inventory", "score", "quit", "back"]
    commands = ["go north", "go south", "go west", "go east", "fly"]
    picks = ["pick t-card", "pick cheat sheet", "pick lucky pen"]

    while not p.victory:
        location = w.get_location(p.x, p.y)

        if location.id == 5 and p.inventory == w.items:
            print("Congratulations and good luck on the test!")
            p.victory = True

        if p.moves == 0:
            print("Time is over, Sorry pal!")
            break

        if location.visited:
            print(location.brief)
        else:
            print(location.long)
            location.visited = True

        print("What to do? \n")
        print("[menu]")
        for action in w.available_actions(location):
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

        if choice in commands:  # if player wants to move.
            if choice in w.available_actions(location):
                w.update_position(p, choice)
                p.moves -= 1
            else:
                print("I cannot do this command.")
        elif choice in picks:  # if player wants to pick up objects.
            item = w.find_item(choice.split()[1])
            picked = w.pick_item(p, item, location)
            p.moves -= 1 if picked else 0  # decrease the number of moves if the item is picked.
        elif choice == "quit":
            print("Good Game!")
            break
        if choice == "fly exam center":
            if p.can_fly:
                w.fly_exam_center(p)
            else:
                print("Currently, you do not have access to this command.")
        elif choice in menu:
            w.handle_action(p, location, choice)
        else:
            print("Sorry, I do not get this command!")
