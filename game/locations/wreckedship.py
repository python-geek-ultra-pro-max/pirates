
from game import location
from game import config
from game.display import announce
from game.events import *
from game.items import Cutlass
from game.items import Flintlock

class Wrecked_ship (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "wrecked ship"
        self.symbol = 'WS'
        self.visitable = True
        self.starting_location = Wrecked_ship(self)
        self.locations = {}
        self.locations["ship"] = self.starting_location
        self.locations["captain's cabin"] = Captain_cabin(self)

    def enter (self, ship):
        print ("arrived at a wrecked ship")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Wrecked_ship(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Wrecked Ship"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("arrive at the wrecked ship. Your ship is at anchor to the south.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["captain's cabin"]
        elif (verb == "north" or verb == "south"):
            announce ("You walk all the way around the wrecked ship. It's not very interesting.")


class Captain_cabin (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Captain_cabin"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_captain_cabin = Cutlass()
        self.item_in_clothes = Flintlock()

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the crew quarters ont eh wrecked ship."
        if edibles == False:
             description = description + " Nothing around here looks very edible."
        
        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_captain_cabin != None:
            description = description + " You see a " + self.item_in_captain_cabin.name + " kept on the deck."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the cabin floor."
        announce (description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["captain's cabin"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_captain_cabin == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_captain_cabin
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the captain's cabin.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_captain_cabin = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")
