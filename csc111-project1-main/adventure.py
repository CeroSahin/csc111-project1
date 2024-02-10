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

from game_data import World, Player, UltimateMagicDoor

if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0, 45)

    required_items = w.required_items()

    menu = ["look", "inventory", "score", "quit", "moves"]  # backi sildim, moves ekledim
    commands = ["go north", "go south", "go west", "go east", "fly", "open magic door", "open ultimate magic door",
                "investigate"]
    picks = ["pick t-card", "pick cheat sheet", "pick lucky pen", "pick key ...", "some secret items..."]

    i = 0
    while not p.victory:
        location = w.get_location(p.x, p.y)
        if i == 0:
            print("You've got an important exam coming up this evening, and you've been studying for weeks.\n"
                  "Last night was a particularly late night on campus. You had difficulty focusing, so \nrather than "
                  "staying in one place, you studied in various places throughout campus as the \nnight progressed. "
                  "Unfortunately, when you woke up this morning, you were missing some \nimportant exam-related items. "
                  "You cannot find your T-card, and you're nervous they won't \nlet you into tonight's exam without it."
                  " Also, you seem to have misplaced your lucky exam \npen - even if they let you in, you can't "
                  "possibly write with another pen! Finally, your \ninstructor for the course lets you bring a cheat "
                  "sheet - a handwritten page of information \nin the exam. Last night, you painstakingly crammed as "
                  "much material onto a single page as \nhumanly possible, but that's missing, too! All of this stuff "
                  "must be around campus \nsomewhere! Can you find all of it before your exam starts tonight?\n")

        if set(p.inventory) in required_items:
            print("a")

        if location.id == 5 and required_items.issubset(set(p.inventory)):
            print("Congratulations you were able to come to Exam Center and collect all your "
                  "missing items before the exam started. Good luck on the test!")
            p.victory = True
            break

        if p.moves == 0 and p.victory is not True:  # ikinci condition ekledim
            print("Time is over, Sorry pal!")
            break

        if location.visited:
            print(location.brief)
        else:
            print(location.long)
            location.visited = True

        print("What to do? \n")
        print("[menu]\n[picks]\n[commands]")
        choice = input("\nEnter action: ")
        i += 1

        if choice in commands or choice in menu or "pick" in choice or choice in ["[menu]", "[picks]", "[commands]"]:

            if choice == "[commands]":
                for command in commands:
                    print(command)
                choice = input("\nWhat should I do?: ")

            if "investigate" in choice:
                if location.name == "Exam Center":
                    print("There is nothing to investigate here")
                else:
                    for i in range(len(w.get_location(p.x, p.y).investigations)):
                        print(w.get_location(p.x, p.y).investigations[i][0])
                    location_to_investigate = input("Where should I investigate? ")
                    output = w.investigate(p, location_to_investigate)
                    if output is not None:
                        choice = output

            if "fly" in choice:
                if p.can_fly:
                    location_name = input("Fly to where?: ")
                    w.fly_to(p, location_name)
                else:
                    print("Currently, you do not have access to this command.")

            if choice == "open magic door":
                if w.get_location(p.x, p.y).name == "Exam Center":
                    print("Unfortunately, there is no ordinary magic door here")
                else:
                    p.moves -= 1
                    magic_door = ""
                    for door in w.magic_doors:
                        if door.location == w.get_location(p.x, p.y):
                            magic_door = door
                    key_name = input("The door is locked. What should I open it with?")
                    key = w.find_item(key_name)
                    if key is not None:
                        w.open_magic_door(p, key, magic_door)
                    else:
                        print(f"I can't open the door with {key_name}")

            if choice == "open ultimate magic door":
                if w.get_location(p.x, p.y) == w.locations[6]:
                    p.moves -= 1
                    new_ultimate_door = UltimateMagicDoor(w.locations[6], w.items[7])
                    potential_key = input("What should I open the door with? ")
                    for key in p.inventory:
                        if key.name == potential_key:
                            new_ultimate_door.open_ultimate_door(key)
                else:
                    print(f"There isn't an ulitmate magic door in {w.get_location(p.x, p.y)}")

            if choice in w.available_actions(location):
                w.update_position(p, choice)
                p.moves -= 1

            elif choice not in (w.available_actions(location) + menu) and all(
                    [c not in choice for c in ["investigate", "fly",
                                               "open magic door", "pick", "open ultimate magic door"]]):
                print("I cannot go this way.")

            elif choice == "[picks]":
                for pick in picks:
                    print(pick)
                choice = input("\nWhat should I pick?: ")

            if "pick" in choice:
                item_name_list = choice.split()[1:]
                item_name = item_name_list[0]
                for i in range(1, len(item_name_list)):
                    item_name = item_name + " " + str(item_name_list[i])
                item = w.find_item(
                    item_name)
                if item is not None:
                    picked = w.pick_item(p, item, location)  # itemin lokasyonda olup olmadığına bakıyor
                    if picked:
                        print(f"Item {item_name} is added to your inventory")
                else:
                    print(f"You cannot pick a(n) {item_name} in {location.name}")
                    picked = None
                p.moves -= 1 if picked else 0  # decrease the number of moves if the item is picked.

            elif choice == "[menu]":
                print("Menu Options: \n")
                for option in menu:
                    print(option)
                choice = input("\nWhat should I do?: ")

            if choice == "quit":
                print("Good Game!")
                break

            if choice in menu:
                w.handle_action(p, location, choice)

        else:  # hangi if'in else'i, her yorumdan sonra veriyor
            print("Sorry, I do not get this command!")
