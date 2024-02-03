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
    items: list[Item]
    visited: bool
    id: int

    def __init__(self, name: str, x: int, y: int, brief: str, long: str, items: [Item], id: int) -> None:
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

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.items = self.load_items(items_data)
        self.locations = self.load_locations(location_data)

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
        for line in lines:
            line = line.strip()
            row = line.split()
            begin = int(row[0])
            end = int(row[1])
            points = int(row[2])
            name = " ".join(row[2:])
            new_item = Item(name, begin, end, points)
            result.append(new_item)

        return result

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """ Reads the location data and returns a list of locations. In our case, there are 5 of them."""
        result = []
        lines = location_data.readlines()
        i = 0
        while i < len(lines):
            loc_name = lines[i].strip()
            loc_id = int(lines[i+1].strip())
            brief = lines[i+2].strip()
            long = lines[i+3].strip()
            x, y = self.get_coordinates(loc_id)
            new_loc = Location(name=loc_name, x=x, y=y, brief=brief, long=long, id=loc_id, items=None)
            result.append(new_loc)
            i += 6
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
        for i in self.map:
            for j in i:
                if loc_id == j:
                    y = i.index(loc_id)
                    x = self.map.index(i)
                    return (x, y)

        return None

    def update_position(self, player: Player, choice: str) -> None:
        """ Update the player's position on the map. """
        if choice == "go north":
            player.x += 1
        elif choice == "go south":
            player.x -= 1
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
        pick_subjects = []
        if location.items is not None:
            pick_subjects = [f"pick {item}" for item in location.items]
        actions = ["go north", "go south", "go west", "go east"]
        north_location = self.get_location(location.x + 1, location.y)
        south_location = self.get_location(location.x - 1, location.y)
        west_location = self.get_location(location.x, location.y - 1)
        east_location = self.get_location(location.x, location.y + 1)
        if north_location is None:
            actions.remove("go north")
        elif south_location is None:
            actions.remove("go south")
        if west_location is None:
            actions.remove("go west")
        elif east_location is None:
            actions.remove("go east")
        return actions + pick_subjects

    def handle_action(self, player: Player, location: Location, action: str):
        """ Handle all the other actions that do not require any modification. """
        if action == "look":
            print(location.brief if location.visited else location.long)
        elif action == "inventory":
            print(player.inventory)
        elif action == "score":
            print(player.score)

    def check_fly(self, player: Player):
        """ Return True if flying option is available else retur False. Flying option becomes
        available after player's score is greater than 30."""
        if player.score > 30:
            print("You can now fly to the exam center whenever you want by using the command fly exam center")
            player.can_fly = True
        else:
            if player.can_fly:
                print("You lost your ability to fly because your points fell below the threshold.")

            player.can_fly = False

    def pick_item(self, player: Player, item: Item, player_location: Location) -> bool:
        """ Pick the item and add it to player's inventory return True if the item is picked, else return False. """
        if item.current_position == player_location.id:
            player.inventory.append(item)
            player_location.items.remove(item)
            player.score += item.target_points
            self.check_fly(player)
            return True # item picked.
        else:
            print("You can't pick that item.")
            return False # item was not picked.

    def find_item(self, name) -> Optional[Item]:
        """ Return the item with the given name. """
        for item in self.items:
            if name == item.name:
                return item
        return

    def fly_exam_center(self, player):
        """ Fly the player to the exam center. Ignore physics laws and air friction. """
        player.x = 2
        player.y = 1
        return
