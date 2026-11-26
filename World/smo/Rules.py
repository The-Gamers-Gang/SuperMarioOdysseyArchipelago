from worlds.generic.Rules import set_rule as apply_rule
from .Options import SMOOptions
from .Logic import total_moons, count_moons


def set_rules(self, options : SMOOptions) -> None:
    """ Sets the placement rules for Super Mario Odyssey.
        Args:
            self: SMOWorld object for this player's world.
            options: The options from this player's yaml.
    """

    active = {loc.name: loc for loc in self.get_locations()} if self.short_route else None

    def set_location_rule(name, rule):
        if active is None:
            apply_rule(self.multiworld.get_location(name, self.player), rule)
        elif name in active:
            apply_rule(active[name], rule)

    # Prevents a softlock in Bowser from not having this moon in the moon list
    #self.multiworld.get_location("Big Broodal Battle" , self.player).place_locked_item(self.create_item("Bowser's Story Moon"))


    # Cascade Story Progress
    # set_rule(self.multiworld.get_location("Multi Moon Atop the Falls", self.player), lambda state: state.has("Cascade Story Moon", self.player))

    # if options.goal >= 4:
    #     # Sand Story Progress
    #     set_rule(self.multiworld.get_location("Moon Shards in the Sand", self.player), lambda state: state.has("Sand Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Showdown on the Inverted Pyramid", self.player), lambda state: state.has("Sand Story Moon", self.player))
    #
    # if options.goal > 5:
    #     # Wooded Story Progress
    #     set_rule(self.multiworld.get_location("Flower Thieves of Sky Garden", self.player), lambda state: state.has("Wooded Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Path to the Secret Flower Field", self.player), lambda state: state.count("Wooded Story Moon", self.player) >= 1)
    #     set_rule(self.multiworld.get_location("Defend the Secret Flower Field!", self.player), lambda state: state.count("Wooded Story Moon", self.player) >= 2)
    #
    # if options.goal >= 9:
    #     # Metro Story Progress
    #     set_rule(self.multiworld.get_location("Powering Up the Station", self.player), lambda state: state.count("Metro Story Moon", self.player) >= 4)
    #     set_rule(self.multiworld.get_location("A Traditional Festival!", self.player), lambda state: state.count("Metro Story Moon", self.player) >= 5)
    #
    # if options.goal >= 12:
    #     # Seaside Story Progress
    #     # set_rule(self.multiworld.get_location("The Glass Is Half Full!", self.player), lambda state: state.has("Seaside Story Moon", self.player) and
    #     #     state.has("Seaside Story Moon", self.player) and state.has("Seaside Story Moon", self.player) and state.has("Seaside Story Moon", self.player))
    #     #
    #     # # Snow Story Progress
    #     # set_rule(self.multiworld.get_location("The Bound Bowl Grand Prix", self.player), lambda state: state.has("Snow Story Moon", self.player) and
    #     #     state.has("Snow Story Moon", self.player) and state.has("Snow Story Moon", self.player) and state.has("Snow Story Moon", self.player))
    #
    #     # Luncheon Story Progress
    #     set_rule(self.multiworld.get_location("Under the Cheese Rocks", self.player), lambda state: state.has("Luncheon Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Big Pot on the Volcano: Dive In!", self.player), lambda state: state.count("Luncheon Story Moon", self.player) >= 2)
    #     set_rule(self.multiworld.get_location("Cookatiel Showdown!", self.player), lambda state: state.count("Luncheon Story Moon", self.player) >= 3)
    #
    # if options.goal >= 15:
    #     # Bowser Story Progress
    #     set_rule(self.multiworld.get_location("Smart Bombing", self.player), lambda state: state.has("Bowser Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Big Broodal Battle", self.player), lambda state: state.count("Bowser Story Moon", self.player) >= 2)
    #     set_rule(self.multiworld.get_location("Showdown at Bowser's Castle", self.player), lambda state: state.count("Bowser Story Moon", self.player) >= 3)


    # Outfit Moons
    if self.options.goal > self.options.goal.option_lake:
        set_location_rule("Mechanic Cap",
                 lambda state: state.has("Mechanic Cap", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_location_rule("Mechanic Outfit",
                 lambda state: state.has("Mechanic Outfit", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_location_rule("Fashionable Cap",
                 lambda state: state.has("Fashionable Cap", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_location_rule("Fashionable Outfit",
                 lambda state: state.has("Fashionable Outfit", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))

    if self.options.goal > self.options.goal.option_metro:
        set_location_rule("Pirate Hat",
             lambda state: state.has("Pirate Hat", self.player) or
            (count_moons(self, state, "Seaside", self.player) >= self.moon_counts["seaside"] and
            count_moons(self, state, "Snow", self.player) >= self.moon_counts["snow"]))
        set_location_rule("Pirate Outfit",
                 lambda state: state.has("Pirate Outfit", self.player) or
                (count_moons(self, state, "Seaside", self.player) >= self.moon_counts["seaside"] and
                count_moons(self, state, "Snow", self.player) >= self.moon_counts["snow"]))
        # set_rule(self.multiworld.get_location("Clown Hat", self.player),
        #          lambda state: state.has("Clown Hat", self.player) or
        #         (count_moons(self, state, "Snow", self.player) and
        #         count_moons(self, state, "", self.player)))
        # set_rule(self.multiworld.get_location("Clown Suit", self.player),
        #          lambda state: state.has("Clown Suit", self.player) or
        #         (count_moons(self, state, "", self.player) and
        #         count_moons(self, state, "", self.player)))
        # set_rule(self.multiworld.get_location("", self.player),
        #          lambda state: state.has("", self.player) or
        #         (count_moons(self, state, "", self.player) and
        #         count_moons(self, state, "", self.player)))


    if self.options.goal > self.options.goal.option_moon:
        set_location_rule("Cascade Kingdom - Caveman Cave-Fan",
                 lambda state: state.has("Caveman Headwear", self.player) and state.has("Caveman Outfit", self.player))
        set_location_rule("Lake Kingdom - That Trendy “Pirate” Look",
                 lambda state: state.has("Pirate Hat", self.player) and state.has("Pirate Outfit", self.player))
        set_location_rule("Lake Kingdom - Space Is “In” Right Now",
                 lambda state: state.has("Space Helmet", self.player) and state.has("Space Suit", self.player))
        set_location_rule("Lake Kingdom - That “Old West” Style",
                 lambda state: state.has("Cowboy Hat", self.player) and state.has("Cowboy Outfit", self.player))
        set_location_rule("Luncheon Kingdom - Mechanic: Repairs Complete!",
                 lambda state: state.has("Mechanic Cap", self.player) and state.has("Mechanic Outfit", self.player))
        set_location_rule("Moon Kingdom - Doctor in the House",
                 lambda state: state.has("Doctor Headwear", self.player) and state.has("Doctor Outfit", self.player))
        set_location_rule("Mushroom Kingdom - Totally Classic",
                 lambda state: (state.has("Mario 64 Cap", self.player) and state.has("Mario 64 Suit", self.player)) or (
                             state.has("Metal Mario Cap", self.player) and state.has("Metal Mario Clothes", self.player)))
        set_location_rule("Mushroom Kingdom - Courtyard Chest Trap",
                 lambda state: (state.has("Mario 64 Cap", self.player) and state.has("Mario 64 Suit", self.player)) or (
                             state.has("Metal Mario Cap", self.player) and state.has("Metal Mario Clothes", self.player)))
        set_location_rule("Metro Kingdom - Surprise Clown!",
                 lambda state: state.has("Clown Hat", self.player) and state.has("Clown Suit", self.player))

    # if options.goal > 15 or (options.shops != 0 and options.shops != 3):
    set_location_rule("Sand Kingdom - Dancing with New Friends", lambda state: (state.has("Sombrero", self.player) and state.has("Poncho", self.player)) or state.has("Skeleton Suit", self.player))
    if self.options.goal > self.options.goal.option_lake:
        set_location_rule("Lake Kingdom - I Feel Underdressed", lambda state: (state.has(
            "Swim Goggles", self.player) and state.has("Swimwear", self.player)) or state.has("Boxer Shorts",
                                                                                                      self.player))
        set_location_rule("Wooded Kingdom - Exploring for Treasure",
                 lambda state: state.has("Explorer Hat", self.player) and state.has("Explorer Outfit", self.player))


    if self.options.goal > self.options.goal.option_metro:
        set_location_rule("Metro Kingdom - Rewiring the Neighborhood",
                 lambda state: state.has("Builder Helmet", self.player) and state.has("Builder Outfit", self.player))
        set_location_rule("Seaside Kingdom - A Relaxing Dance",
                 lambda state: state.has("Resort Hat", self.player) and state.has("Resort Outfit", self.player))
        set_location_rule("Snow Kingdom - Moon Shards in the Cold Room",
                 lambda state: state.has("Snow Hood", self.player) and state.has("Snow Suit", self.player))
        set_location_rule("Snow Kingdom - Slip Behind the Ice",
                 lambda state: state.has("Snow Hood", self.player) and state.has("Snow Suit", self.player))
        set_location_rule("Snow Kingdom - I'm Not Cold!",
                 lambda state: state.has("Boxer Shorts", self.player))

    if self.options.goal > self.options.goal.option_metro:
        set_location_rule("Luncheon Kingdom - A Strong Simmer",
                 lambda state: state.has("Chef Hat", self.player) and state.has("Chef Suit", self.player))
        set_location_rule("Luncheon Kingdom - An Extreme Simmer",
                 lambda state: state.has("Chef Hat", self.player) and state.has("Chef Suit", self.player))

    if self.options.goal > self.options.goal.option_luncheon:
        set_location_rule("Bowser Kingdom - Scene of Crossing the Poison Swamp",
                 lambda state: state.has("Samurai Helmet", self.player) and state.has("Samurai Armor", self.player))
        set_location_rule("Bowser Kingdom - Taking Notes: In the Folding Screen",
                 lambda state: state.has("Samurai Helmet", self.player) and state.has("Samurai Armor", self.player))

    # Post Game Outfits
    if self.options.goal > self.options.goal.option_moon:
        for outfit in self.outfit_moon_counts.keys():
            if self.options.goal > self.options.goal.option_dark:
                if self.outfit_moon_counts[outfit] < self.moon_counts["dark"]:
                    set_location_rule(outfit,
                         lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
                             outfit] or state.has(outfit, self.player))
            elif self.options.goal > self.options.goal.option_darker:
                if self.outfit_moon_counts[outfit] < self.moon_counts["darker"]:
                    set_location_rule(outfit,
                             lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
                                 outfit] or state.has(outfit, self.player))

        # set_rule(self.multiworld.get_location("Luigi Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Luigi Cap"] or state.has("Luigi Cap", self.player))
        # set_rule(self.multiworld.get_location("Luigi Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Luigi Suit"] or state.has("Luigi Suit", self.player))
        # set_rule(self.multiworld.get_location("Doctor Headwear", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Doctor Headwear"] or state.has("Doctor Headwear", self.player))
        # set_rule(self.multiworld.get_location("Doctor Outfit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Doctor Outfit"] or state.has("Doctor Outfit", self.player))
        # set_rule(self.multiworld.get_location("Waluigi Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Waluigi Cap"] or state.has("Waluigi Cap", self.player))
        # set_rule(self.multiworld.get_location("Waluigi Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Waluigi Suit"] or state.has("Waluigi Suit", self.player))
        # set_rule(self.multiworld.get_location("Diddy Kong Hat", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Diddy Kong Hat"] or state.has("Diddy Kong Hat", self.player))
        # set_rule(self.multiworld.get_location("Diddy Kong Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Diddy Kong Suit"] or state.has("Diddy Kong Suit", self.player))
        # set_rule(self.multiworld.get_location("Wario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Wario Cap"] or state.has("Wario Cap", self.player))
        # set_rule(self.multiworld.get_location("Wario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Wario Suit"] or state.has("Wario Suit", self.player))
        # set_rule(self.multiworld.get_location("Hakama", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Hakama"] or state.has("Hakama", self.player))
        # set_rule(self.multiworld.get_location("Bowser's Top Hat", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bowser's Top Hat"] or state.has("Bowser's Top Hat", self.player))
        # set_rule(self.multiworld.get_location("Bowser's Tuxedo", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bowser's Tuxedo"] or state.has("Bowser's Tuxedo", self.player))
        # set_rule(self.multiworld.get_location("Bridal Veil", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bridal Veil"] or state.has("Bridal Veil", self.player))
        # set_rule(self.multiworld.get_location("Bridal Gown", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bridal Gown"] or state.has("Bridal Gown", self.player))
        # set_rule(self.multiworld.get_location("Gold Mario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Gold Mario Cap"] or state.has("Gold Mario Cap", self.player))
        # set_rule(self.multiworld.get_location("Gold Mario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Gold Mario Suit"] or state.has("Gold Mario Suit", self.player))
        # set_rule(self.multiworld.get_location("Metal Mario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Metal Mario Cap"] or state.has("Metal Mario Cap", self.player))
        # set_rule(self.multiworld.get_location("Metal Mario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Metal Mario Suit"] or state.has("Metal Mario Suit", self.player))

    # # Completion State
    # if options.goal == "sand":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Sand Multi-Moon", self.player) >= 2
    # if options.goal == "lake":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Lake Multi-Moon", self.player)
    # if options.goal == "metro":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Metro Multi-Moon", self.player) >= 2
    # if options.goal == "luncheon":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Luncheon Multi-Moon", self.player) >= 2
    # if options.goal == "moon":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Beat the Game", self.player)
    #     self.multiworld.get_location("Beat the Game", self.player).place_locked_item(self.create_item("Beat the Game"))
    # if options.goal == "dark":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Dark Side Multi-Moon", self.player)
    # if options.goal == "darker":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Darker Side Multi-Moon", self.player)

    # Place Goal moon at location
    if options.goal == "sand":
        self.multiworld.get_location("Sand Kingdom - The Hole in the Desert", self.player).place_locked_item(
            self.create_item("Sand Multi-Moon"))
    if options.goal == "lake":
        self.multiworld.get_location("Lake Kingdom - Broodals Over the Lake", self.player).place_locked_item(
            self.create_item("Lake Multi-Moon"))
    if options.goal == "metro":
        self.multiworld.get_location("Metro Kingdom - A Traditional Festival!", self.player).place_locked_item(
            self.create_item("Metro Multi-Moon"))
    if options.goal == "luncheon":
        self.multiworld.get_location("Luncheon Kingdom - Cookatiel Showdown!", self.player).place_locked_item(
            self.create_item("Luncheon Multi-Moon"))
    if options.goal == "dark":
        self.multiworld.get_location("Dark Side - Arrival at Rabbit Ridge!", self.player).place_locked_item(
            self.create_item("Dark Side Multi-Moon"))
    if options.goal == "darker":
        self.multiworld.get_location("Darker Side - A Long Journey's End!", self.player).place_locked_item(self.create_item("Darker Side Multi-Moon"))


    # Captures
    if options.capture_sanity.value == options.capture_sanity.option_true:
        # Cascade Story
        set_location_rule("Cascade Kingdom - Our First Power Moon",
                 lambda state: state.has("Chain Chomp", self.player))
        set_location_rule("Cascade Kingdom - Multi Moon Atop the Falls",
                 lambda state: (state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player)) and state.has(
            "Broode's Chain Chomp", self.player))
        set_location_rule("Broode's Chain Chomp",
                 lambda state: state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player))
        #set_rule(self.multiworld.get_location("Our First Power Moon", self.player),
        #         lambda state: state.has("Chain Chomp", self.player) or state.has("T-Rex", self.player))
        #set_rule(self.multiworld.get_location("Multi Moon Atop the Falls", self.player),
        #         lambda state: state.has("Broode's Chain Chomp", self.player))
        # Sand Story
        set_location_rule("Sand Kingdom - The Hole in the Desert",
                 lambda state: state.has("Bullet Bill", self.player) and state.has("Knucklotec's Fist", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Wooded Story
            set_location_rule("Wooded Kingdom - Path to the Secret Flower Field",
                     lambda state: state.has("Sherm", self.player))
            set_location_rule("Wooded Kingdom - Defend the Secret Flower Field!",
                     lambda state: state.has("Uproot", self.player) and state.has("Sherm", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Metro Story
            set_location_rule("Metro Kingdom - New Donk City's Pest Problem",
                     lambda state: state.has("Sherm", self.player))
            set_location_rule("Metro Kingdom - Powering Up the Station",
                     lambda state: state.has("Manhole", self.player))

        if self.options.goal > self.options.goal.option_metro:
            # Seaside Story
            set_location_rule("Seaside Kingdom - The Hot Spring Seal",
                     lambda state: state.has("Gushen", self.player))
            set_location_rule("Seaside Kingdom - The Glass Is Half Full!",
                     lambda state: state.has("Gushen", self.player))
            # Snow Story
            set_location_rule("Snow Kingdom - The Bound Bowl Grand Prix",
                     lambda state: state.has("Shiverian Racer", self.player))
            # Luncheon Story
            set_location_rule("Luncheon Kingdom - Under the Cheese Rocks",
                     lambda state: state.has("Hammer Bro", self.player))
            set_location_rule("Luncheon Kingdom - Climb Up the Cascading Magma",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Big Pot on the Volcano: Dive In!",
                     lambda state: state.has("Meat", self.player))
            set_location_rule("Luncheon Kingdom - Cookatiel Showdown!",
                     lambda state: state.has("Lava Bubble", self.player))

        if self.options.goal > self.options.goal.option_luncheon:
            # Ruined Story
            set_location_rule("Ruined Kingdom - Battle with the Lord of Lightning!",
                     lambda state: state.has("Spark Pylon", self.player))
            # Bowser Story
            set_location_rule("Bowser Kingdom - Infiltrate Bowser's Castle!",
                     lambda state: state.has("Spark Pylon", self.player))
            set_location_rule("Bowser Kingdom - Smart Bombing",
                     lambda state: state.has("Pokio", self.player))
            # Moon Story
            set_location_rule("Beat the Game",
                     lambda state: state.has("Bowser", self.player))

        # Cap
        set_location_rule("Cap Kingdom - Frog-jumping above the Fog",
                 lambda state: state.has("Frog", self.player))
        set_location_rule("Cap Kingdom - Frog-jumping from the Top Deck",
                 lambda state: state.has("Frog", self.player))
        set_location_rule("Cap Kingdom - Skimming the Poison Tide",
                 lambda state: state.has("Paragoomba", self.player))
        set_location_rule("Cap Kingdom - Slipping through the Poison Tide",
                 lambda state: state.has("Paragoomba", self.player))
        set_location_rule("Cap Kingdom - Push-Block Peril",
                 lambda state: state.has("Spark Pylon", self.player))
        set_location_rule("Cap Kingdom - Hidden Among the Push-Blocks",
                 lambda state: state.has("Spark Pylon", self.player))
        set_location_rule("Bonneton Tower Model",
                 lambda state: state.has("Spark Pylon", self.player) and state.has("Paragoomba" , self.player))

        # Cascade
        set_location_rule("Cascade Kingdom - Chomp Through the Rocks",
                 lambda state: state.has("Chain Chomp", self.player))
        set_location_rule("Cascade Kingdom - Dinosaur Nest: Running Wild!",
                 lambda state: state.has("T-Rex", self.player))
        set_location_rule("Cascade Kingdom - Nice Shot with the Chain Chomp!",
                 lambda state: state.has("Chain Chomp", self.player))
        set_location_rule("Cascade Kingdom - Very Nice Shot with the Chain Chomp!",
                 lambda state: state.has("Chain Chomp", self.player))
        set_location_rule("Cascade Kingdom - Behind the Waterfall",
                 lambda state: state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player))

        # Sand
        set_location_rule("Sand Kingdom - Wandering Cactus",
                 lambda state: state.has("Cactus", self.player))
        set_location_rule("Sand Kingdom - Underground Treasure Chest",
                 lambda state: state.has("Bullet Bill", self.player))
        set_location_rule("Sand Kingdom - Fishing in the Oasis",
                 lambda state: state.has("Lakitu", self.player))
        set_location_rule("Sand Kingdom - Love in the Heart of the Desert",
                 lambda state: state.has("Goomba", self.player))
        set_location_rule("Sand Kingdom - You're Quite a Catch, Captain Toad!",
                 lambda state: state.has("Lakitu", self.player))
        set_location_rule("Sand Kingdom - On the Lone Pillar",
                 lambda state: state.has("Bullet Bill", self.player))

        # Change when entrance rando implemented
        set_location_rule("Sand Kingdom - Strange Neighborhood",
                 lambda state: state.has("Mini Rocket", self.player))
        set_location_rule("Sand Kingdom - Above a Strange Neighborhood",
                 lambda state: state.has("Mini Rocket", self.player))
        set_location_rule("Inverted Pyramid Model",
                 lambda state: state.has("Mini Rocket", self.player) and state.has("Bullet Bill", self.player) and state.has("Knucklotec's Fist", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Wooded
            set_location_rule("Wooded Kingdom - By the Babbling Brook in the Deep Woods",
                     lambda state: state.has("Coin Coffer", self.player) or state.has("T-Rex", self.player))
            set_location_rule("Wooded Kingdom - The Hard Rock in Deep Woods",
                     lambda state: state.has("Coin Coffer", self.player) or state.has("T-Rex", self.player))
            set_location_rule("Wooded Kingdom - A Treasure Made of Coins",
                     lambda state: state.has("Coin Coffer", self.player))
            set_location_rule("Wooded Kingdom - Beneath the Roots of a Moving Tree",
                     lambda state: state.has("Tree", self.player))
            set_location_rule("Wooded Kingdom - Love in the Forest Ruins",
                     lambda state: state.has("Goomba", self.player))
            set_location_rule("Wooded Kingdom - Elevator Blind Spot",
                     lambda state: state.has("Sherm", self.player))
            set_location_rule("Wooded Kingdom - Inside the Rock in the Forest",
                     lambda state: state.has("Coin Coffer", self.player) or state.has("Sherm", self.player))
            set_location_rule("Wooded Kingdom - Stretching Your Legs",
                     lambda state: state.has("Uproot", self.player))
            # Add vine sub area uproot req if trick jump not possible
            # Change when entrance rando implemented
            set_location_rule("Wooded Kingdom - Wandering in the Fog",
                     lambda state: state.has("Paragoomba", self.player) and state.has("Mini Rocket", self.player))
            set_location_rule("Wooded Kingdom - Nut Hidden in the Fog",
                     lambda state: state.has("Mini Rocket", self.player))
            set_location_rule("Steam Gardener Watering Can",
                     lambda state: state.has("Boulder", self.player))

            # Lake
            set_location_rule("Lake Kingdom - End of the Hidden Passage",
                     lambda state: state.has("Zipper", self.player))
            set_location_rule("Lake Kingdom - Lake Fishing",
                     lambda state: state.has("Lakitu", self.player))
            set_location_rule("Lake Kingdom - I Met a Lake Cheep Cheep!",
                     lambda state: state.has("Cheep Cheep", self.player))
            set_location_rule("Lake Kingdom - A Successful Repair Job",
                     lambda state: state.has("Puzzle Part (Lake Kingdom)", self.player))
            # Change when entrance rando implemented
            set_location_rule("Lake Kingdom - Unzip the Chasm",
                     lambda state: state.has("Zipper", self.player))
            set_location_rule("Lake Kingdom - Super-Secret Zipper",
                     lambda state: state.has("Zipper", self.player))
            set_location_rule("Underwater Dome",
                     lambda state: state.has("Zipper", self.player))


        if self.options.goal > self.options.goal.option_lake:
            # Cloud
            set_location_rule("Cloud Kingdom - Picture Match: Basically a Goomba",
                     lambda state: state.has("Picture Match Part (Goomba)", self.player))

            # Lost
            set_location_rule("Lost Kingdom - Soaring Over the Forgotten Isle!",
                     lambda state: state.has("Glydon", self.player))
            set_location_rule("Lost Kingdom - Twist ‘n' Turn-Up Treasure",
                     lambda state: state.has("Tropical Wiggler", self.player))

            # Metro
            set_location_rule("Metro Kingdom - Remotely Captured Car",
                     lambda state: state.has("RC Car", self.player))
            set_location_rule("Metro Kingdom - RC Car Pro!",
                     lambda state: state.has("RC Car", self.player))
            set_location_rule("Metro Kingdom - Rewiring the Neighborhood",
                     lambda state: state.has("Spark Pylon", self.player))
            set_location_rule("Metro Kingdom - Off the Beaten Wire",
                     lambda state: state.has("Spark Pylon", self.player))
            # Change when entrance rando implemented
            set_location_rule("Metro Kingdom - Moon Shards Under Siege",
                     lambda state: state.has("Taxi", self.player) and state.has("Sherm", self.player))
            set_location_rule("Metro Kingdom - Sharpshooting Under Siege",
                     lambda state: state.has("Taxi", self.player) and state.has("Sherm", self.player))
            set_location_rule("Metro Kingdom - Inside the Rotating Maze",
                     lambda state: state.has("Manhole", self.player))
            set_location_rule("Metro Kingdom - Outside the Rotating Maze",
                     lambda state: state.has("Manhole", self.player))
            set_location_rule("Metro Kingdom - Vaulting Up a High-Rise",
                     lambda state: state.has("Mini Rocket", self.player))
            set_location_rule("Metro Kingdom - Hanging from a High-Rise",
                     lambda state: state.has("Mini Rocket", self.player))
            set_location_rule("Metro Kingdom - Sewer Treasure",
                     lambda state: state.has("Manhole", self.player))
            set_location_rule("Pauline Statue",
                     lambda state: state.has("Manhole", self.player) and state.has("Mini Rocket", self.player))

        if self.options.goal > self.options.goal.option_metro:
            # Seaside
            set_location_rule("Seaside Kingdom - Love by the Seaside",
                     lambda state: state.has("Goomba", self.player))
            set_location_rule("Seaside Kingdom - Fly Through the Narrow Valley",
                     lambda state: state.has("Gushen", self.player))
            set_location_rule("Seaside Kingdom - Treasure Chest in the Narrow Valley",
                     lambda state: state.has("Gushen", self.player))
            set_location_rule("Seaside Kingdom - Lighthouse Leaper",
                     lambda state: state.has("Glydon", self.player))
            set_location_rule("Sand Jar",
                     lambda state: state.has("Gushen", self.player))
            # Change when entrance rando implemented
            set_location_rule("Seaside Kingdom - Wading in the Cloud Sea",
                     lambda state: state.has("Mini Rocket", self.player))
            set_location_rule("Seaside Kingdom - Sunken Treasure in the Cloud Sea",
                     lambda state: state.has("Mini Rocket", self.player))

            # Snow
            set_location_rule("Snow Kingdom - Ice-Dodging Goomba Stack",
                     lambda state: state.has("Goomba", self.player))
            set_location_rule("Snow Kingdom - Fishing in the Glacier!",
                     lambda state: state.has("Lakitu", self.player))
            set_location_rule("Snow Kingdom - Snowline Circuit Class S",
                     lambda state: state.has("Shiverian Racer", self.player))
            set_location_rule("Shiverian Nesting Dolls",
                     lambda state: state.has("Ty-foo", self.player))
            # Change when entrance rando implemented
            set_location_rule("Snow Kingdom - Blowing and Sliding",
                     lambda state: state.has("Ty-foo", self.player))

            # Luncheon
            set_location_rule("Luncheon Kingdom - Love Above the Lava",
                     lambda state: state.has("Goomba", self.player))
            set_location_rule("Luncheon Kingdom - A Strong Simmer",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - An Extreme Simmer",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Excavate ‘n' Search the Cheese Rocks",
                     lambda state: state.has("Hammer Bro", self.player))
            set_location_rule("Luncheon Kingdom - Climb the Cheese Rocks",
                     lambda state: state.has("Hammer Bro", self.player))
            set_location_rule("Luncheon Kingdom - Light the Lantern on the Small Island",
                     lambda state: state.has("Fire Bro", self.player) or state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - All the Cracks Are Fixed",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Taking Notes: Swimming in Magma",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Magma Narrow Path",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Crossing to the Magma",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Treasure Beneath the Cheese Rocks",
                     lambda state: state.has("Hammer Bro", self.player))
            set_location_rule("Luncheon Kingdom - Alcove Behind the Pillars of Magma",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Beneath the Rolling Vegetables",
                     lambda state: state.has("Lava Bubble", self.player))
            set_location_rule("Luncheon Kingdom - Golden Turnip Recipe 3",
                     lambda state: state.has("Hammer Bro", self.player))
            set_location_rule("Souvenir Forks",
                     lambda state: state.has("Hammer Bro", self.player) and state.has("Lava Bubble", self.player))
            set_location_rule("Vegetable Plate",
                     lambda state: state.has("Hammer Bro", self.player) and state.has("Lava Bubble", self.player))
            # Change when entrance rando implemented
            set_location_rule("Luncheon Kingdom - Fork Flickin' to the Summit",
                     lambda state: state.has("Volbonan", self.player))
            set_location_rule("Luncheon Kingdom - Fork Flickin' Detour",
                     lambda state: state.has("Volbonan", self.player))

        if self.options.goal > self.options.goal.option_luncheon:
            # Bowser
            set_location_rule("Bowser Kingdom - Stack up above the wall",
                     lambda state: state.has("Goomba", self.player))
            set_location_rule("Bowser Kingdom - Poking Your Nose in the Plaster Wall",
                     lambda state: state.has("Pokio", self.player))
            set_location_rule("Bowser Kingdom - Poking the Turret Wall",
                     lambda state: state.has("Pokio", self.player))
            set_location_rule("Bowser Kingdom - Jizo All in a Row",
                     lambda state: state.has("Jizo", self.player))
            set_location_rule("Bowser Kingdom - Underground Jizo",
                     lambda state: state.has("Jizo", self.player))
            set_location_rule("Bowser Kingdom - Fishing(?) in Bowser's Castle",
                     lambda state: state.has("Lakitu", self.player))
            set_location_rule("Bowser Kingdom - Jizo's Big Adventure",
                     lambda state: state.has("Jizo", self.player))
            set_location_rule("Bowser Kingdom - Jizo and the Hidden Room",
                     lambda state: state.has("Jizo", self.player))
            set_location_rule("Bowser Kingdom - Behind the Big Wall",
                     lambda state: state.has("Spark Pylon", self.player))
            set_location_rule("Bowser Kingdom - Taking notes: Between spinies",
                     lambda state: state.has("Spark Pylon", self.player))

            # Moon
            #if self.options.goal > self.options.goal.option_moon:
            set_location_rule("Moon Kingdom - Under the Bowser Statue",
                    lambda state: state.has("Bowser statue", self.player))
            set_location_rule("Moon Kingdom - In a Hole in the Magma",
                     lambda state: state.has("Parabones", self.player))
            set_location_rule("Moon Kingdom - Around the Barrier Wall",
                     lambda state: state.has("Banzai Bill", self.player))
            set_location_rule("Moon Kingdom - Fly to the Treasure Chest and Back",
                 lambda state: state.has("Banzai Bill", self.player))


# for debugging purposes, you may want to visualize the layout of your world. Uncomment the following code to
# write a PlantUML diagram to the file "my_world.puml" that can help you see whether your regions and locations
# are connected and placed as desired
#     from Utils import visualize_regions
#     visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
