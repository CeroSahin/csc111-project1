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

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World("map.txt", "locations.txt", "items.txt")
    p = Player(0, 0, 30)  # set starting location of player; you may change the x, y coordinates here as appropriate

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

        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        if location.visited:
            print(location.brief)
        else:
            print(location.long)
            location.visited = True

        print("What to do? \n")
        print("[menu]")
        #for action in location.available_actions():
        #    print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

        if choice in commands:  # if player wants to move.
            if choice in location.available_actions():
                w.update_position(p, choice)
            p.moves -= 1
        elif choice in picks:  # if player wants to pick up objects.
            item = w.find_item(choice.split()[1])
            w.pick_item(p, item, location)
            p.moves -= 1
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

        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
