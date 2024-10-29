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


class PracticeChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/practicechoosecoin.html'

    def vars_for_template(self):
        # Define and shuffle the two coins
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        # Store the coin order in participant.vars
        self.participant.vars['coin_order'] = coins
        return {
            'coins': coins,
            'round_number': self.round_number,
        }

    def before_next_page(self):
        # Store the chosen coin
        self.player.chosen_coin = self.player.coin_choice
        # Flip the coins after the player makes a choice
        # Since it's a practice round, we flip the coins but won't affect total_winnings
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        # Show this page only during practice rounds (e.g., rounds 1-3)
        return self.round_number <= 3

class ChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins
        return {
            'coins': coins,
            'round_number': self.round_number,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        # Show this page only during real rounds
        return self.round_number > 3

# Similarly, create practice versions of other pages if needed

class PracticeRevealCoinOutcome(Page):
    template_name = 'coin_flip/revealcoinoutcome.html'  # Use the same template
    def vars_for_template(self):
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': self.round_number,
        }

    def is_displayed(self):
        return self.round_number <= 3

class RevealCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': self.round_number,
        }

    def is_displayed(self):
        return self.round_number > 3

class PracticeChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/choosepermutation.html'  # Use the same template

    def get_form_fields(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        form_fields = [f"{coin[0]}_outcome" for coin in coins]
        return form_fields

    def vars_for_template(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        return {
            'coins': coins,
            'round_number': self.round_number,
        }

    def before_next_page(self):
        # Since it's a practice round, we won't calculate winnings
        pass

    def is_displayed(self):
        return self.round_number <= 3

class ChoosePermutation(Page):
    form_model = 'player'

    def get_form_fields(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        form_fields = [f"{coin[0]}_outcome" for coin in coins]
        return form_fields

    def vars_for_template(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        return {
            'coins': coins,
            'round_number': self.round_number,
        }

    def before_next_page(self):
        # Store the player's permutation choice
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        self.player.coin_permutation_choice = ''.join(outcomes)
        # Calculate winnings
        self.player.calculate_winnings(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number > 3

class Results(Page):
    def vars_for_template(self):
        # Sum over all winnings from real rounds only
        real_rounds = self.player.in_rounds(4, C.NUM_ROUNDS)
        total_winnings = sum([p.total_winnings for p in real_rounds])
        return {
            'winnings': total_winnings
        }

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

# Adjust the page_sequence to include practice pages
page_sequence = [
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    # Repeat the practice pages for three practice rounds
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    # Now include the real rounds
    ChooseCoin,
    RevealCoinOutcome,
    ChoosePermutation,
    Results,
]
