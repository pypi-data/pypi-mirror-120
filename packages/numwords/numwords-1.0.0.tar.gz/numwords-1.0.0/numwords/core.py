import math
from typing import Dict, List, Tuple


NUM_LIMIT: int = 10**66-1

DIGITS_WORDS_MAP: Dict[str, str] = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
}

NUMBERS_WORDS_MAP: Dict[str, str] = {
    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen'
}

TENS_PLACE_MAP: Dict[str, str] = {
    '2': 'twenty',
    '3': 'thirty',
    '4': 'fourty',
    '5': 'fifty',
    '6': 'sixty',
    '7': 'seventy',
    '8': 'eighty',
    '9': 'ninety'
}

LARGE_NUMBERS: List[str] = [
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
    "undecillion",
    "duodecillion",
    "tredecillion",
    "quattuordecillion",
    "quindecillion",
    "sexdecillion",
    "septendecillion",
    "octodecillion",
    "novemdecillion",
    "vigintillion"
]


def numwords(num: int) -> str:
    if num > NUM_LIMIT:
        raise ValueError(f'Value should not exceed {NUM_LIMIT}')
    
    num_str = str(num)
    num_str_rev = num_str[::-1]    #Reversing the number
    
    batches: List[str] = []
    n_div = math.ceil(len(num_str_rev) / 3)
    for idx in range(n_div):
        batches.append(num_str_rev[idx * 3:(idx + 1) * 3:])

    counter = -1
    
    for batch in batches:
        batch_num, batch_str = batches_to_words(batch)
        if counter == -1:
            string = batch_str
        elif batch_num == "000":
            pass
        else:
            string = f"{batch_str} {LARGE_NUMBERS[counter]} {string}"
        counter += 1
    string = " ".join(string.split())
    return string.strip().title()


def batches_to_words(batch: str) -> Tuple[str, str]:
    string = ''
    if len(batch) == 3 and batch[2] != '0':
        string += f"{DIGITS_WORDS_MAP[batch[2]]} hundred"
    if len(batch) >= 2 and batch[1] != '0':
        if 9 < int(batch[1::-1]) < 20:
            string += f" {NUMBERS_WORDS_MAP[batch[1::-1]]}"
        else:
            string += f" {TENS_PLACE_MAP[batch[1]]}"
    if len(batch) >= 1 and batch[0] != '0':
        if 9 < int(batch[1::-1]) < 20:
            pass
        else:
            string += f" {DIGITS_WORDS_MAP[batch[0]]}"        
    return (batch[::-1], string)