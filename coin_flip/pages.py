from otree.api import Page
from .models import C, Player
import random

P_FAIR = 0.5
P_BIASED = 0.95  # Probability of heads for the biased coin

# Comprehension questions

class CompQuestion1(Page):
    template_name = 'coin_flip/CompQuestion.html'
    
    def is_displayed(self):
        # Display only if comprehension questions haven't been shown yet
        return not self.participant.vars.get('comp_questions_shown', False)

class CompQuestion2(Page):
    template_name = 'coin_flip/CompQuestion.html'
    
    def is_displayed(self):
        # Display only if comprehension questions haven't been shown yet
        return not self.participant.vars.get('comp_questions_shown', False)

class CompQuestion3(Page):
    template_name = 'coin_flip/CompQuestion.html'
    
    def is_displayed(self):
        # Display only if comprehension questions haven't been shown yet
        return not self.participant.vars.get('comp_questions_shown', False)
    
    def before_next_page(self):
        # Set the flag after the last comprehension question
        self.participant.vars['comp_questions_shown'] = True

# Introduction Pages
class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point5(Page):
    def is_displayed(self):
        return self.round_number == 2

class Introduction1point6(Page):
    def is_displayed(self):
        return self.round_number == 3

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 4

# Practice Rounds
class PracticeChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/PracticeChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        # Save the order of coins to the player model
        self.participant.vars['coin_order'] = coins
        self.player.coin_order = ','.join([coin[0] for coin in coins])
        practice_round_number = self.round_number - C.NUM_INTRO_PAGES
        return {
            'coins': coins,
            'practice_round_number': practice_round_number,
            'is_practice_round': True,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        # Flip the coins after the player makes a choice
        # Since it's a practice round, we flip the coins but won't affect total_winnings
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class PracticeRevealCoinOutcome(Page):
    template_name = 'coin_flip/PracticeRevealCoinOutcome.html'

    def vars_for_template(self):
        practice_round_number = self.round_number - C.NUM_INTRO_PAGES
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'practice_round_number': practice_round_number,
            'is_practice_round': True,
        }

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class PracticeChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/PracticeChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars.get('coin_order', [('fair', 'Fair'), ('biased', 'Biased')])
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        practice_round_number = self.round_number - C.NUM_INTRO_PAGES
        return {
            'coins': coins,
            'practice_round_number': practice_round_number,
            'is_practice_round': True,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        coins = self.participant.vars['coin_order']
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        # Save permutation choice to player model
        self.player.coin_permutation_choice = ''.join(outcomes)

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

# Real Rounds
class RoundInfo(Page):
    template_name = 'coin_flip/RoundInfo.html'

    def vars_for_template(self):
        real_round_number = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'real_round_number': real_round_number,
            'is_practice_round': False,
        }

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class ChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/ChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        # Save the order of coins to the player model
        self.participant.vars['coin_order'] = coins
        self.player.coin_order = ','.join([coin[0] for coin in coins])

        real_round_number = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'real_round_number': real_round_number,
            'is_practice_round': False,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        # Flip the coins after the player makes a choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class RevealCoinOutcome(Page):
    template_name = 'coin_flip/RevealCoinOutcome.html'

    def vars_for_template(self):
        real_round_number = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'real_round_number': real_round_number,
            'is_practice_round': False,
        }

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class ChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/ChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars['coin_order']
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        real_round_number = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'real_round_number': real_round_number,
            'is_practice_round': False,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        coins = self.participant.vars['coin_order']
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        # Save permutation choice to player model
        self.player.coin_permutation_choice = ''.join(outcomes)
        self.player.calculate_winnings()  # Call without parameters

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class Results(Page):
    def vars_for_template(self):
        # Get the player's total winnings
        total_winnings = self.player.total_winnings
        return {
            'winnings': total_winnings
        }

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

page_sequence = [
    # Introduction pages
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    # Comprehension questions
    CompQuestion1,
    CompQuestion2,
    CompQuestion3,
    # Practice rounds
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
