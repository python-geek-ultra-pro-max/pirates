from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Fish (Context, event.Event):

    def __init__ (self):
        super().__init__()
        self.name = "fish visitor"
        self.fish = 1
        self.verbs['catch'] = self
        self.verbs['feed'] = self
        
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "catch"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the fish got caught."
                if (self.fish > 1):
                    self.fish = self.fish - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.lucky == True):
                    self.result["message"] = "luckly, the fish got caught."
                else:
                    self.result["message"] = c.get_name() + " is attacked by a shark."
                    if (c.inflict_damage (self.seagulls, "Pecked to death by a shark")):
                        self.result["message"] = ".. " + c.get_name() + " is pecked to death by a shark!"

        elif (verb == "feed"):
            self.fish = self.fish + 1
            self.result["newevents"].append (Fish())
            self.result["message"] = "the fish are happy"
            self.go = True
        elif (verb == "help"):
            print ("the fish will pester you until you feed them or catch them")
            self.go = False
        else:
            print ("it seems the only options here are to feed or catch")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.fish) + " fish has appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result
