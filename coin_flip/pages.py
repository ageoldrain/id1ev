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
    template_name = 'coin_flip/PracticeChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins
        return {
            'coins': coins,
            'round_number': self.round_number,
            'is_practice_round': True,  # Explicitly set to True
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class RoundInfo(Page):
    template_name = 'coin_flip/RoundInfo.html'

    def vars_for_template(self):
        is_practice_round = self.round_number <= C.PRACTICE_ROUNDS

        return {
            'round_number': self.round_number - C.PRACTICE_ROUNDS if not is_practice_round else self.round_number,
            'is_practice_round': is_practice_round,
        }

    def is_displayed(self):
        return True

class ChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/ChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins

        is_practice_round = False  # Since this is a real round
        adjusted_round_number = self.round_number - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'round_number': adjusted_round_number,
            'is_practice_round': is_practice_round,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number > C.PRACTICE_ROUNDS

class PracticeRevealCoinOutcome(Page):
    template_name = 'coin_flip/PracticeRevealCoinOutcome.html'

    def vars_for_template(self):
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': self.round_number,
            'is_practice_round': True,  # Explicitly set to True
        }

    def is_displayed(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class RevealCoinOutcome(Page):
    template_name = 'coin_flip/RevealCoinOutcome.html'

    def vars_for_template(self):
        is_practice_round = False  # Since this is a real round
        adjusted_round_number = self.round_number - C.PRACTICE_ROUNDS
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': adjusted_round_number,
            'is_practice_round': is_practice_round,
        }

    def is_displayed(self):
        return self.round_number > C.PRACTICE_ROUNDS

class PracticeChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/PracticeChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        return {
            'coins': coins,
            'round_number': self.round_number,
            'is_practice_round': True,  # Explicitly set to True
        }

    def before_next_page(self):
        pass

    def is_displayed(self):
        return self.round_number <= C.PRACTICE_ROUNDS

class ChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/ChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars['coin_order']
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        is_practice_round = False  # Since this is a real round
        adjusted_round_number = self.round_number - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'round_number': adjusted_round_number,
            'is_practice_round': is_practice_round,
        }

    def before_next_page(self):
        coins = self.participant.vars['coin_order']
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        self.player.coin_permutation_choice = ''.join(outcomes)
        self.player.calculate_winnings(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number > C.PRACTICE_ROUNDS

class Results(Page):
    def vars_for_template(self):
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
    # Practice rounds
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,
    # Real rounds
    RoundInfo,
    ChooseCoin,
    RevealCoinOutcome,
    ChoosePermutation,
    Results,
]
