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
from typing import Optional


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

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """
        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.current_position = start

class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name
        - brief
        - long
        - x
        - y
        - posdir
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
    # posdir: ?
    items: list[Item]
    visited: bool
    id: int

    def __init__(self, name: str, x: int, y: int, brief: str, long: str, items: [Item], id: int) -> None:
        """Initialize a new location.
        """
        self.name = name
        self.x = x
        self.y = y
        # self.posdir = posdir
        self.brief = brief
        self.long = long
        self.items = items
        self.visited = False
        self.id = id
        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        #actions = []


        return None
        # depends on position --> which way the player can go/ anywhere expect -1 ["go north", "go south", "go west", "go east", "fly"]

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed


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

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.moves = starting_moves
        self.score = 0
        self.can_fly = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - items
        - locations


    Representation Invariants:
        - all([[-1 <= position <= 1 for position in axis_values] for axis_values in self.map])
        - all([item.name in ["Cheat Sheet", "T-Card", "Lucky Pen", "Answer Sheet"] for item in items])
        - all([location.name in ["Buttery", "Trinity", "Queen's Park", "EJ Pratt", "Victoria", "Exam Center", "Location -1"] for location in locations])
    """
    map: list[list[int]]
    items: list[Item]
    locations: list[Location]

    def __init__(self, map_data: str, location_data: str, items_data: str) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.items = self.load_items(items_data)
        self.locations = self.load_locations(location_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: str) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        result = []
        with open(map_data) as f:
            lines = f.readlines()
            for x in lines:
                a = x.strip("\n")
                b = a.split()
                c = [int(m) for m in b]
                result.append(c)
        return result

    # TODO: Complete this method as specified. Do not modify any of this function's specifications.
    # TODO: Add methods for loading location data and item data (see note above).
    def load_items(self, items_data: str) -> list[Item]:
        """ Reads the items_data and returns a list of items. In our case the
        list should contain the tcard item, cheat sheet item, lucky pen item and answer sheet item.
        """
        result = []
        with open(items_data) as f:
            line_list = f.readlines()
            for line in line_list:
                a = line.strip()
                b = a.split()
                name = ""
                for item in b:
                    if b.index(item) >= 3:
                        name += item + " "
                new_item = Item(name, int(b[0]), int(b[1]), int(b[2]))
                result.append(new_item)

        return result

    def load_locations(self, location_data: str) -> list[Location]:
        """ Reads the location data and returns a list of locations. In our case, there are 5 of them."""
        result = []
        with open(location_data) as f:
            line = f.readline().strip()
            while line is not None:
                name = line
                location_id = int(f.readline().strip())

                items_in_location = []
                for item in self.items:
                    if item.start_position == location_id:
                        items_in_location.append(item)

                short_description = f.readline().strip()
                long_description = ""
                long_line = f.readline().strip()

                while long_line != "END":
                    long_description += long_line + " "
                    long_description = f.readline().strip()

                y = 0
                x = 0
                for row in self.map:
                    for spot in row:
                        if spot == id:
                            break
                        x += 1
                    y += 1

                new_location = Location(name, x, y, short_description, long_description, items_in_location, location_id)
                result.append(new_location)

        return result

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        for location in self.locations:
            if location.x == x and location.y == y:
                return location

        return

    def update_position(self, player: Player, choice: str) -> None:
        #determine player's location if go west ..., if go east...,
        #if choice == "go north"
        return None


    def handle_action(self, player: Player, location: Location, action: str):
        if action == "look":
            print(location.brief if location.visited else location.long)
        elif action == "inventory":
            print(player.inventory)
        elif action == "score":
            print(player.score)

    def check_fly(self, player: Player):
        if player.score > 30:
            print("You can now fly to the exam center whenever you want by using the command fly exam center")
            player.can_fly = True
        else:
            if player.can_fly:
                print("You lost your ability to fly because your points fell below the threshold.")

            player.can_fly = False

    def pick_item(self, player: Player, item: Item, player_location: Location):
        if item.current_position == player_location.id:
            player.inventory.append(item)
            player_location.items.remove(item)
            player.score += item.target_points
            self.check_fly(player)

    def find_item(self, name):
        for item in self.items:
            if name == item.name:
                return item
        return None

    def fly_exam_center(self, player):
        # send the player to the exam center.
        return
