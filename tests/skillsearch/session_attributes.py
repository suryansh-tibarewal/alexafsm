from collections import namedtuple
from typing import List

from alexafsm.session_attributes import SessionAttributes as SessionAttributesBase, INITIAL_STATE

from tests.skillsearch.skill import Skill

import json

Slots = namedtuple('Slots', ['query', 'nth'])
NUMBER_SUFFIXES = {'st', 'nd', 'rd', 'th'}
ENGLISH_NUMBERS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth',
                   'ninth', 'tenth']


class SessionAttributes(SessionAttributesBase):
    slots_cls = Slots

    not_sent_fields = []

    def __init__(self,
                 intent: str = None,
                 slots=None,
                 state: str = INITIAL_STATE):
        super().__init__(intent, slots, state)

    def to_json(self):
        print("got here")
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

        # @property
    # def nth_as_index(self):
    #     """Return -1 if we cannot figure out what index was actually meant by the user"""
    #     if not self.slots.nth:  # Amazon's intent system might not give us anything
    #         return -1
    #     elif self.slots.nth in ENGLISH_NUMBERS:
    #         return ENGLISH_NUMBERS.index(self.slots.nth)
    #     else:
    #         try:
    #             # Amazon SOMETIMES gives us "5th" instead of "fifth", so we can try to parse it!
    #             # this is not always the case -- it gives us "second" instead of 2nd
    #             if self.slots.nth[-2:] in NUMBER_SUFFIXES:
    #                 return int(self.slots.nth[:-2]) - 1
    #             else:
    #                 # otherwise probably directly a number in string format
    #                 return int(self.slots.nth) - 1
    #         except ValueError:
    #             return -1

    # @property
    # def skill(self):
    #     return self.skills[self.skill_cursor]
