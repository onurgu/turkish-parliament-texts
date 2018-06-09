"""
This file includes the hand written rules on how to clean raw text data.
Each rule may have a condition.
"""
import re


def no_condition(term_name, filename):
    """
    Always True condition. Always applies the rule. Aka no condition.
    """
    return True


def never_condition(term_name,filename):
    """
    Always False condition. Never applies the rule.
    """
    return False

rules = [
    # ("R1", lambda text: re.sub("\xad\n","",text) , lambda term_name, filename : True),
    ("R1", lambda text: re.sub("\xad\n ?","",text) , no_condition), # same as above line
    # ("R3", lambda text: re.sub("\n"," ",text) , lambda term_name,filename : False),
    ("R2", lambda text: re.sub("\n"," ",text) , never_condition),  # same as above line
]
