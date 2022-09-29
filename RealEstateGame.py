# Author: Greisy Virgen Larios
# GitHub username: greisyvirgen
# Date: 6/01/2022
# Description: Write a program which allows tow or more people to play a more simple version of Monopoly.
# Players start at "Go" (Spot 0), and move around the board by rolling a die with possible integer values
# of 1 to 6. If a player lands on an unowned spot, they will purchase it, as long as their current balance
# is greater than the price of the property. If a player lands on a space owned by another player, they'll
# pay the specified rent amount to the owner. If they pass "Go" they'll get money and if they reach an
# account balance of $0, they loose the game.

class RealEstateGame:
    """
    This class represents the aspects of the game. It will generate the board with its respective
    uniquely named spaces and the ‘Go’ space (from which the players will start the game. This class
    also generates the players with an initial account balance to start the game. This is the main
    class of the program from which the functionality of the game will be created.”This class represents
    the aspects of the game. It will generate the board with its respective uniquely named spaces and
    the ‘Go’ space (from which the players will start the game). This class also generates the players
    with an initial account balance to start the game.
    This is the main class of the program from which the functionality of the game will be created.
    """
    def __init__(self):
        """
        Initializes the data members as private. Takes no parameters.
        """
        self._player_info = {}      # Dictionary that contains player objects
        self._board_spaces = {}     # Dictionary that contains board info and property owner

    def create_spaces(self, go_money, spaces_array):
        """
        This function takes the amount of money given to the players once they’ve passed “GO” in the board,
        as well as an array that contains the properties on the game. The spaces are all of unique names
        with 24 spaces and 1 space for 'Go'. Each space has a rent amount assigned, it's purchase price
        should be 5 times that rent amount.
        """
        spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                  14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        # Need to relate the given parameter's rent value to the corresponding space

        # Set position 0 to be the money paid to the user for passing Go
        self._board_spaces[0] = go_money

        for index in range(len(spaces)):
            self._board_spaces[spaces[index]] = [spaces_array[index], None]
            # Adds the associated rent prices to each space in the board to a dictionary

    def create_player(self, name, initial_balance):
        """
        Takes two parameters: name - a unique name that represents each of the
        players. initial_balance – an initial amount for the player to start with.
        All players will begin the game at the ‘Go’ space.
        """
        # I am creating a Player object and storing it in my dictionary
        self._player_info[name] = Player(name)
        player = self._player_info[name]
        player.set_account_balance(initial_balance)

    def get_player_account_balance(self, player_name):
        """
        Takes the name of a player and returns their account balance.
        """
        if player_name in self._player_info:
            name = self._player_info[player_name]
            balance = name.get_account_balance()
            return balance

            # string_balance = player_name + " Balance = " + str(balance)
            # return string_balance   # Can also just return balance variable

    def get_player_current_position(self, player_name):
        """
        Takes the name of a player and returns their current position on the board.
        """
        if player_name in self._player_info:
            name = self._player_info[player_name]
            position = name.get_current_position()
            return position

            # string_position = player_name + " Position = " + str(position)
            # return string_position   # Can also just return position variable

    def buy_space(self, player_name):
        """
        Takes the name of a player and analyzes their current account balance. If their
        account balance is greater than the purchase price of the space, and the space
        is not currently owned by anyone, then the player will purchase the space and
        the purchase price will be deducted from their account. Now, that player will
        own that current property/space and the function will return True. If none of
        the above conditions are met, the method will return False.
        """
        # I already have a player object within my dictionary, I need to access its info like below
        # Also accessed my player object in my get current balance and position (FOR REFERENCE)
        for player in self._player_info:
            name = self._player_info[player_name]
            position = name.get_current_position()  # Getting player's current position
            player_balance = name.get_account_balance()

            if player == player_name:
                # If this is true, then check their balance > purchase price

                if position == 0:
                    # EXCEPTION to not be able to buy "Go" space
                    return False

                if position != 0:
                    # Now I want to check if that space is owned by someone else
                    for spaces in self._board_spaces:  # spaces is the key
                        if spaces == position:  # To compare player position to board space properties
                            space_owner = self._board_spaces[spaces][1]
                            # print(space_owner)
                            space_value = self._board_spaces[spaces][0]
                            space_value *= 5  # To get rent price * 5 for tot purchase price

                            if space_owner is not None:
                                # Since that space is owned, it can't be bought
                                return False

                            # Can do else or the if statement (making it clear to my brain lol)
                            else:
                                # Then it CAN be bought!!
                                if player_balance > space_value:
                                    self._board_spaces[position][1] = player_name
                                    # Add to player object in Player class
                                    name.set_owned_properties(player_name, position)
                                    player_balance -= space_value  # Subtract the value from player account
                                    name.set_account_balance(player_balance)   # Update player balance
                                    return True
                                return False
                    return False

    def move_player(self, player_name, move_spaces):
        """
        This function takes the player’s name and the amount of spaces for the player to move,
        in the range of 1 and 6. If player's balance is 0, the method will not perform any operations
        and just return. If the player lands on or passes ‘Go’ as they move, the player will receive the
        ‘Go’ set amount of money. Once player has moved, if the space landed on is owned by another
        player, then it’s rent amount should be deducted from current player and paid to space owner.
        If after paying rent the player ends with 0, the player looses the game and their properties are
        removed. If no one owns the space or the current player owns the space, no rent will be paid.
        """
        name = self._player_info[player_name]
        position = name.get_current_position()
        balance = name.get_account_balance()
        if balance == 0:    # The method shouldn't perform any functions
            return

        if 0 < move_spaces <= 6:  # Should be within dice range of 1 to 6
            # Set the player's position accordingly based on parameter
            new_position = position + move_spaces   # Changing the position
            name.set_position(new_position)        # Setting the new position for the player

            # Check if "Go" money should be added to player account
            if new_position >= 25:
                if position <= 24:    # Check if the previous position was less than 0
                    # if true, they get paid go money
                    money_for_go = self._board_spaces[0]
                    balance += money_for_go  # Add the "Go" money to the player's balance
                    name.set_account_balance(balance)    # Update player's balance
                # If player already passed go:
                new_position -= 25
                name.set_position(new_position)

            # After "Go" money & position is 0, no need to check for owner
            if new_position == 0:
                return

            # Check if anyone owns the current space or not
            owner = self._board_spaces[new_position][1]
            if owner is None:
                return

            if owner is not None:
                # The space has an owner
                if owner == player_name:
                    # No need to pay rent to themselves
                    return

                if owner != player_name:
                    owner = self._player_info[owner]  # Get the owner of the space
                    property_rent = self._board_spaces[new_position][0]   # Get the rent amount for space

                    if balance <= property_rent:
                        # The player will only pay as much as their current balance
                        owner.set_account_balance(balance)
                        balance = 0  # For current player's new balance
                        name.set_account_balance(balance)

                        if balance == 0:
                            player_properties = name.get_owned_properties()
                            if len(player_properties) == 0:
                                return

                            if len(player_properties) != 0:
                                name.remove_properties(player_name)

                                for space in range(1, 25):
                                    if self._board_spaces[space][1] is not None \
                                            and self._board_spaces[space][1] == player_name:
                                        self._board_spaces[space][1] = None

                    if balance > property_rent:
                        # Else, remove rent amount from player
                        balance -= property_rent
                        name.set_account_balance(balance)

                        # Pay owner of the space the corresponding rent amount
                        owner_balance = owner.get_account_balance()
                        owner_balance += property_rent
                        owner.set_account_balance(owner_balance)  # Update space owners account balance

    def check_game_over(self):
        """
        This method determines whether the game is over. This is determined by checking if all but
        one player has an account balance of 0. Then, the winner’s name will be returned. If there
        is no winner, then this method will return an empty string.
        """
        active_players = []  # To keep track of who has a balance greater than 0
        for player in self._player_info:
            name = self._player_info[player]   # Getting the player's in the game
            if name.get_account_balance() != 0:
                still_playing = name.get_name()
                active_players.append(still_playing)

        if len(active_players) == 1:   # There is only one person left since rest have lost
            winner = active_players[0]
            return winner

        if len(active_players) != 1:  # There are > 1 active players in the game
            active_players = []
            # Set my list to empty each run to make proper checks when called again
            return ""


class Player:
    """
    Initializes the player's information which will then be used and added to the
    main dictionary that contains the necessary information for each player.
    """
    def __init__(self, name):
        self._name = name
        self._balance = 0  # Initialize player's account balance which will change in set method
        self._position = 0  # Player's start at position 0 in the board ("Go" is pos 0)
        self._owned_properties = {}  # Set up properties they own

    def get_name(self):
        """ Returns the name of the current player object"""
        return self._name

    def get_account_balance(self):
        """ Returns the player's balance"""
        return self._balance

    def get_current_position(self):
        """ Returns the player's position"""
        return self._position

    def get_owned_properties(self):
        """ Returns the player's owned properties"""
        return self._owned_properties

    def set_account_balance(self, balance):
        """
        Updates the account balance accordingly
        """
        self._balance = balance

    def set_position(self, position):
        """
        Sets the most current position of the player in the board
        :param position: Player's current position in the board
        """
        self._position = position

    def set_owned_properties(self, name, space):
        """ Sets the properties owned by player in a dictionary"""
        self._owned_properties[name] = [space]
        # Add the owned space to player's info as a list

    def remove_properties(self, name):
        """Removes a player's owned properties"""
        self._owned_properties.pop(name)
