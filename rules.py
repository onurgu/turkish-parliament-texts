"""
This file includes the hand written rules on how to clean raw text data.
Each rule may have a condition.
"""
import re
rules = [
    (lambda text: re.sub("\xad\n","",text) , lambda term_name,filename : True),
    (lambda text: re.sub("\n"," ",text) , lambda term_name,filename : False),
]
