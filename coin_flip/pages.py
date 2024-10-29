# pages.py

from otree.api import Page
from .models import C, Player
import random

P_FAIR = 0.5
P_BIASED = 0.95  # Probability of heads for the biased coin

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point5(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point6(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 1

class RoundInfo(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'is_practice_round': self.is_practice_round(),
        }

    def is_displayed(self):
        return self.round_number <= C.NUM_ROUNDS

    def is_practice_round(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class ChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']

    def vars_for_template(self):
        # Define and shuffle the two coins
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        # Store the coin order in participant.vars
        self.participant.vars['coin_order'] = coins
        return {
            'coins': coins,
            'round_number': self.round_number,
            'is_practice_round': self.is_practice_round(),
        }

    def before_next_page(self):
        # Store the chosen coin
        self.player.chosen_coin = self.player.coin_choice
        # Flip the coins after the player makes a choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number <= C.NUM_ROUNDS

    def is_practice_round(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class RevealCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': self.round_number,
            'is_practice_round': self.is_practice_round(),
        }

    def is_displayed(self):
        return self.round_number <= C.NUM_ROUNDS

    def is_practice_round(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class ChoosePermutation(Page):
    form_model = 'player'

    def get_form_fields(self):
        # Retrieve coin order
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        # Create form fields based on the coin codes
        form_fields = [f"{coin[0]}_outcome" for coin in coins]
        return form_fields

    def vars_for_template(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        return {
            'coins': coins,
            'round_number': self.round_number,
            'is_practice_round': self.is_practice_round(),
        }

    def before_next_page(self):
        # Store the player's permutation choice
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        self.player.coin_permutation_choice = ''.join(outcomes)
        # Calculate winnings only if not a practice round
        if not self.is_practice_round():
            self.player.calculate_winnings(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number <= C.NUM_ROUNDS

    def is_practice_round(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class Results(Page):
    def vars_for_template(self):
        # Sum over all winnings from real rounds only
        real_rounds = self.player.in_rounds(C.PRACTICE_ROUNDS + 1, C.NUM_ROUNDS)
        total_winnings = sum([p.total_winnings for p in real_rounds])
        return {
            'winnings': total_winnings
        }

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

page_sequence = [
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    RoundInfo,
    ChooseCoin,
    RevealCoinOutcome,
    ChoosePermutation,
    Results
]
