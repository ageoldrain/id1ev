# models.py

from otree.api import *
import random

doc = """
Curiosity and Information Demand
"""

debug = False

class C(BaseConstants):
    NAME_IN_URL = 'economics_experiment'
    PLAYERS_PER_GROUP = None
    PRACTICE_ROUNDS = 3  # Number of practice rounds
    REAL_ROUNDS = 10     # Number of real rounds
    NUM_ROUNDS = PRACTICE_ROUNDS + REAL_ROUNDS  # Total rounds (13)

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            if 'fair_left' not in self.session.vars:
                self.session.vars['fair_left'] = 0  # Or some default value
            if 'biased_left' not in self.session.vars:
                self.session.vars['biased_left'] = 0  # Or some default value

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Player's choice between 'fair' or 'biased' coin
    coin_choice = models.StringField(choices=['fair', 'biased'])
    chosen_coin = models.StringField()

    # Player's guesses for the outcome of each coin
    fair_outcome = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the Fair coin"
    )
    biased_outcome = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the Biased coin"
    )

    # Results
    chosen_coin_result = models.StringField()
    fair_coin_result = models.StringField()
    biased_coin_result = models.StringField()
    coin_permutation_choice = models.StringField()
    coin_permutation_result = models.StringField()

    total_winnings = models.CurrencyField(initial=cu(0))

    def flip_chosen_coin(self, p_fair: float, p_biased: float):
        """
        Flip both coins and store the results.
        """
        assert 0 <= p_fair <= 1, "Probability for the fair coin must be between 0 and 1."
        assert 0 <= p_biased <= 1, "Probability for the biased coin must be between 0 and 1."

        # Flip the fair coin
        self.fair_coin_result = 'H' if random.random() < p_fair else 'T'
        # Flip the biased coin
        self.biased_coin_result = 'H' if random.random() < p_biased else 'T'

        # Store the result of the chosen coin
        if self.coin_choice == 'fair':
            self.chosen_coin_result = self.fair_coin_result
        elif self.coin_choice == 'biased':
            self.chosen_coin_result = self.biased_coin_result

        # Combine the coin outcomes into a permutation result
        self.coin_permutation_result = f"{self.fair_coin_result}{self.biased_coin_result}"

        if debug:
            print(f"Fair coin result: {self.fair_coin_result}")
            print(f"Biased coin result: {self.biased_coin_result}")
            print(f"Chosen coin: {self.coin_choice}")
            print(f"Chosen coin result: {self.chosen_coin_result}")
            print(f"Coin permutation result: {self.coin_permutation_result}")

    def calculate_winnings(self, p_fair: float, p_biased: float):
        """
        Calculate the player's winnings based on their guesses and the coin results.
        Only updates total_winnings if it's a real round.
        """
        # Only calculate winnings for real rounds
        if self.round_number > C.PRACTICE_ROUNDS:
            # Check if the player guessed the outcome of the chosen coin correctly
            if self.coin_choice == 'fair':
                if self.fair_outcome == self.fair_coin_result:
                    self.total_winnings += p_biased * 2  # Expected value of biased coin
            elif self.coin_choice == 'biased':
                if self.biased_outcome == self.biased_coin_result:
                    self.total_winnings += p_fair * 2  # Expected value of fair coin
        else:
            if debug:
                print(f"Round {self.round_number} is a practice round. No winnings added.")
