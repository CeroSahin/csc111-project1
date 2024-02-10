"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO
import random


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name
        - start_position
        - target_position
        - target_points
        - current_position

    Representation Invariants:
        - self.name in ["Cheat Sheet", "T-Card", "Lucky Pen", "Answer Sheet"]
        - 0 <= self.start_position <= 5
        - self.start_position != self.target_position
        - 0 <= self.target_position <= 5
        - 0 < self.target_points
        - 0 <= self.current_position <= 5
    """
    name: str
    start_position: int
    target_position: int
    target_points: int
    current_position: int
    can_pick_up = bool

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """
        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.current_position = start
        self.can_pick_up = False


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name
        - brief
        - long
        - x
        - y
        - items
        - visited
        - id
    Representation Invariants:
        - len(self.brief) >= len(self.long)
        - self.name in self.brief and self.name in self.long
        - -1 <= self.x <= 1
        - -1 >= self.y <= 1
        - 0 <= len(self.items) <= 4
        - -1 <= self.id <= 5
    """
    name: str
    brief: str
    long: str
    x: int
    y: int
    items: list[Item]
    visited: bool
    id: int
    investigations = list[list]

    def __init__(self, name: str, x: int, y: int, brief: str, long: str, items: [Item], id: int,
                 investigations: list[list]) -> None:
        """Initialize a new location.
        """
        self.name = name
        self.x = x
        self.y = y
        self.brief = brief
        self.long = long
        self.items = items
        self.visited = False
        self.id = id
        self.investigations = investigations


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x
        - y
        - inventory
        - victory
        - moves
        - score
        - can_fly

    Representation Invariants:
        - -1 <= self.x <= 1
        - -1 <= self.y <= 1
        - 0 <= len(self.inventory) <= 4
        - 0 <= self.moves
        - 0 <= self.score
    """
    x: int
    y: int
    inventory: list[Item]
    victory: bool
    moves: int
    score: int
    can_fly: bool

    def __init__(self, x: int, y: int, starting_moves: int) -> None:
        """
        Initializes a new Player at position (x, y) with a maximum of starting_moves moves.
        """
        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.moves = starting_moves
        self.score = 0
        self.can_fly = False


class MagicDoor:
    """An item in the locations

    Instance Attributes:
        - location
        - key
        - password
        - secret_message

    Representation Invariants:
        -self.name in ["Buttery", "Trinity", "Queen's Park", "Victoria", "EJ Pratt"]
        -self.key.name in ["key B", ""key T", "key Q", "key V", "key E"]
        -len(self.password) >= 3
        #self.secret_message'la ilgili ekstra bir RI yazmadım
    """
    location: Location
    key: Item
    password: Optional[str]
    secret_message: Optional[str]

    def __init__(self, location: Location, key: Item, password: str = "", secret_message: str = "") -> None:
        """Initialize a MagicDoor object
        """
        self.location = location
        self.key = key
        self.password = password
        self.secret_message = secret_message


class UltimateMagicDoor(MagicDoor):
    """An UltimateMagicDoor object for Exam Center
    """

    def open_ultimate_door(self, key: Item) -> None:
        """The method to open the ultimate door at exam center if the correct key is taken
        """
        if key == self.key:
            winning_player = self.play_xox()
            if winning_player[:7] == "Player1":
                print(
                    "Congratulations you've won the XOX game and are able to open the ultimate magic door. "
                    "Your secret message is: VTE")
            else:
                print("You have lost the game :(")
        else:
            print("Wrong key!")

    def play_xox(self) -> str:
        """The player plays a game of xox with the computer in order to win a hint about the order of the passwords
        """
        xox_list = [["", "", ""], ["", "", ""], ["", "", ""]]
        i = 0
        list1 = ["X", "0"]
        available_moves = list(range(1, 10))
        print("In order to open the ultimate magic door you have to win a game of XOX! Good luck :)")
        while not all([all([place != "" for place in row]) for row in xox_list]):
            for index in range(0, 3):
                if xox_list[index][0] == xox_list[index][1] == xox_list[index][2] and xox_list[index][0] != "":
                    return f"Player{list1.index(xox_list[index][0]) + 1} won"

                elif xox_list[0][index] == xox_list[1][index] == xox_list[2][index] and xox_list[0][index] != "":
                    return f"Player{list1.index(xox_list[0][index]) + 1} won"

            if (xox_list[0][0] == xox_list[1][1] == xox_list[2][2] and xox_list[1][1] != "") or (
                    xox_list[0][2] == xox_list[1][1] == xox_list[2][0] and xox_list[1][1] != ""):
                return f"Player{list1.index(xox_list[1][1]) + 1} won"

            if i % 2 == 0:
                for line in xox_list:
                    print(line)
                move = int(input(
                    "for a XOX table whose positions are numbered as\n\n1 2 3\n4 5 6\n7 8 9\n\nWhich index do"
                    " you want to put 'X' in?"))
            else:
                move = random.choice(available_moves)

            row = ((move - 1) // 3)
            column = (move % 3) - 1
            if xox_list[row][column] != "":
                print("That place is already taken")
                pass
            else:
                if i % 2 == 0:
                    character = "X"
                else:
                    character = "0"
                xox_list[row][column] = character
                available_moves.remove(move)
                i += 1


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - items
        - locations


    Representation Invariants:
        - all([[-1 <= position <= 1 for position in axis_values] for axis_values in self.map])
        - all([item.name in ["Cheat Sheet", "T-Card", "Lucky Pen", "Answer Sheet"] for item in items])
        - all([location.name in ["Buttery", "Trinity", "Queen's Park", "EJ Pratt", "Victoria", "Exam Center",
        "Location -1"] for location in locations])
    """
    map: list[list[int]]
    items: list[Item]
    locations: list[Location]
    magic_doors: list[MagicDoor]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.items = self.load_items(items_data)
        self.locations = self.load_locations(location_data)
        self.magic_doors = self.load_magic_doors(items_data)

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        result = []
        lines = map_data.readlines()
        for line in lines:
            line = line.strip()
            row = line.split()
            res = [eval(i) for i in row]
            result.append(res)
        return result

    def load_items(self, items_data: TextIO) -> list[Item]:
        """ Reads the items_data and returns a list of items. In our case the
        list should contain the tcard item, cheat sheet item, lucky pen item and answer sheet item.
        """
        result = []
        lines = items_data.readlines()
        i = 0
        for line in lines:
            if i >= 9:
                break
            i += 1
            line = line.strip()
            row = line.split()
            begin = int(row[0])
            end = int(row[1])
            points = int(row[2])
            name = " ".join(row[3:])  # 2 yazıyordu bence 3 olması gerekiyor
            # if i >= 5:
            #   new_item = Key(name, begin, end, points)
            # else:
            new_item = Item(name, begin, end, points)
            result.append(new_item)

        items_data.seek(0)
        return result

    def load_magic_doors(self, magic_door_data: TextIO) -> list[MagicDoor]:
        """Method to load the Magic Doors in the map
        """
        result = []
        lines = magic_door_data.readlines()
        for i in range(1, len(self.locations) - 1):
            place = self.locations[i]
            place_key_name = "key " + place.name[:1]
            new_key = ""
            for key in self.items:
                if key.name == place_key_name:
                    new_key = key
            line = lines[i + 10].strip()
            new_magic_door = MagicDoor(location=place, key=new_key)  # key türünde değil diyor
            password_message_list = line.split()
            if password_message_list[0] != "-":
                password = password_message_list[0]
                new_magic_door.password = password
            if password_message_list[1] != "-":
                secret_message = password_message_list[1]
                new_magic_door.secret_message = secret_message

            result.append(new_magic_door)

        return result

    def required_items(self) -> set[Item]:
        """Returns a list of required items that the player should have in order to win the game.
        In our case they are: t-card, lucky pen, cheat sheet"""
        result = set()
        for i in range(0, 3):
            result.add(self.items[i])

        return result

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """ Reads the location data and returns a list of locations. In our case, there are 5 of them."""
        result = []
        lines = location_data.readlines()
        i = 0
        while i <= 40:
            loc_name = lines[i].strip()
            loc_id = int(lines[i + 1].strip())
            brief = lines[i + 2].strip()
            long = lines[i + 3].strip()
            x, y = self.get_coordinates(loc_id)

            items_in_location = []
            for item in self.items:
                if item.start_position == loc_id:
                    items_in_location.append(item)

            investigations = self.form_investigations(loc_name, lines)

            new_loc = Location(name=loc_name, x=x, y=y, brief=brief, long=long, id=loc_id,
                               items=items_in_location, investigations=investigations)  # itemlar None mı?
            result.append(new_loc)
            i += 6
        return result

    def form_investigations(self, location_name: str, lines: list) -> list[list]:
        """A method to form a dictionary of investigations that could be done in a location
        """
        result = []
        for i in range(43, len(lines), 6):
            line = lines[i].strip()
            if line == location_name:
                for j in range(1, 5):
                    whole_description = lines[i + j].strip()
                    index1 = whole_description.find(":")
                    index2 = whole_description.find(";")
                    name = whole_description[:index1]
                    description = whole_description[(index1 + 1):index2]
                    associated_item = whole_description[(index2 + 1):]
                    specific_location_list = [name, description]
                    if associated_item != "-":
                        specific_location_list.append(associated_item)
                    result.append(specific_location_list)

        return result

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        for location in self.locations:
            if location.x == x and location.y == y:
                if location.id == -1:
                    return None
                return location
        return None

    def get_coordinates(self, loc_id: int) -> Optional[tuple]:
        """ Returns the coordinates of the location with the given loc_id. """
        for i in self.map:  # row, y
            for j in i:  # x
                if loc_id == j:
                    y = i.index(loc_id)
                    x = self.map.index(i)
                    return (x, y)

    def update_position(self, player: Player, choice: str) -> None:
        """ Update the player's position on the map. """
        if choice == "go north":
            player.x -= 1  # + ve - nin yerini değiştirdim
        elif choice == "go south":
            player.x += 1  # + ve - nin yerini değiştirdim
        elif choice == "go west":
            player.y -= 1
        elif choice == "go east":
            player.y += 1
        return None

    def available_actions(self, location: Location):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        # pick_subjects = []
        # if location.items is not None:
        #    pick_subjects = [f"pick {item}" for item in location.items]
        actions = ["go north", "go south", "go west", "go east"]
        north_location = self.get_location(location.x - 1, location.y)  # + - değiştirdim
        south_location = self.get_location(location.x + 1, location.y)  # + - değiştirdim
        west_location = self.get_location(location.x, location.y - 1)
        east_location = self.get_location(location.x, location.y + 1)
        if north_location is None:
            actions.remove("go north")
        if south_location is None:  # elif --> if
            actions.remove("go south")
        if west_location is None:
            actions.remove("go west")
        if east_location is None:  # elif -> if
            actions.remove("go east")
        return actions  # + pick_subjects

    def handle_action(self, player: Player, location: Location, action: str):
        """ Handle all the other actions that do not require any modification. """
        if action == "look":
            print(location.long)
        elif action == "inventory":
            inventory_list = []
            for item in player.inventory:
                inventory_list.append(item.name)
            print(inventory_list)
        elif action == "score":
            print(player.score)
        elif action == "moves":
            print(player.moves)

    def check_fly(self, player: Player):
        """ Return True if flying option is available else return False. Flying option becomes
        available after player's score is greater than 30."""
        if player.score >= 100:
            print("You can now fly to any location you want whenever you want by using the command fly")
            player.can_fly = True
        else:
            if player.can_fly:
                print("You lost your ability to fly because your points fell below the threshold.")

            player.can_fly = False

    def pick_item(self, player: Player, item: Item, player_location: Location) -> bool:
        """ Pick the item and add it to player's inventory return True if the item is picked, else return False. """
        if item.current_position == player_location.id and item.can_pick_up:
            player.inventory.append(item)
            player_location.items.remove(item)
            player.score += item.target_points
            self.check_fly(player)
            return True  # item picked.
        else:
            print("Can't pick up that item here")  # You can't pick that item here
            return False  # item was not picked.

    def find_item(self, name: str) -> Optional[Item]:
        """ Return the item with the given name. """
        for item in self.items:
            if name == item.name:
                return item
        return

    def fly_to(self, player: Player, location_name: str):
        """ Fly the player to the exam center. Ignore physics laws and air friction. """
        for location in self.locations:
            if location.name == location_name:
                player.moves -= 1
                player.x = location.x
                player.y = location.y
                return

        print("I cannot fly there!")

    def open_magic_door(self, p: Player, key: Item, magic_door: MagicDoor) -> None:
        """If player has the required key in their inventory and tries to open the correct door
        Different cases:
            1-player doesn't have the correct key
            3-player opens an empty door
            4-player has to enter the password --> (if correct congratulation message, able to pick up answer sheet),
            (if false message) +
            5-player opens the door with the correct key and recieves the password
        """
        if self.get_location(p.x, p.y) == magic_door.location and key.target_position == self.get_location(p.x, p.y).id:
            if magic_door.password != "":
                tried_password = input("Enter password: ")
                if tried_password == magic_door.password:
                    print(
                        "Congratulations, you entered the right password and opened the lock! The beaming light "
                        "coming inside is too bright. But as your eyes get more used to the brightness you start to "
                        "see a document which has the name of your CS proffesors. At first glance it looks like a "
                        "practice test. However when you look closely you see that it is a test that you haven't seen "
                        "before and it has the answers inside. It is an answer sheet!")
                    for item in self.get_location(p.x, p.y).items:
                        if item.name == "answer sheet":
                            item.can_pick_up = True
                else:
                    print("Wrong password try again")

            elif magic_door.secret_message == "":
                print("This magic door is empty :(")

            else:
                print("Secret password: " + magic_door.secret_message)

        else:
            print("Sorry, couldn't open the door")

    def investigate(self, p: Player, location: str) -> Optional[str]:
        """A method which gives further informaion about the specific place that is selected in the location
        Can also be used to determine whether an object can be picked up
        Cases:
            -specific location isn't in Location
            -specific location is in Location --> print out the description ,if any item is associated
            with the description --> able to pick it up (doesn't pick it up --> False)            -
        """
        for specific_location in self.get_location(p.x, p.y).investigations:
            if location in specific_location:
                p.moves -= 1
                print(specific_location[1])
                item = ""
                if len(specific_location) == 3:
                    item = self.find_item(specific_location[2])
                    item.can_pick_up = True
                action = input("What do you want to do here?")
                if action in ["look", "inventory", "score", "quit", "moves"]:
                    if isinstance(item, Item):
                        item.can_pick_up = False
                    return action
                elif action in ["go north", "go south", "go west", "go east", "fly", "open magic door",
                                "open ultimate magic door"]:
                    if isinstance(item, Item):
                        item.can_pick_up = False
                    return action
                elif action == "investigate":
                    if isinstance(item, Item):
                        item.can_pick_up = False
                    for i in range(len(self.get_location(p.x, p.y).investigations)):
                        print(self.get_location(p.x, p.y).investigations[i][0])
                    location_to_investigate = input("Where should I investigate? ")
                    output = self.investigate(p, location_to_investigate)
                    return output
                elif "pick" in action:
                    item_to_pick = action[5:]
                    if isinstance(item, Item):
                        if item_to_pick != item.name:
                            item.can_pick_up = False
                    return action
                else:
                    print("I don't understand this action")
                    return

        print(f"Can't investigate {location} in {self.get_location(p.x, p.y).name}")
