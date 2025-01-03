from dataclasses import dataclass
from pprint import pprint
import string

from functional_parsing_library.strings import char, char_in
from functional_parsing_library.combinators import separated_by, many

"""
<dutch-address> ::= <street-address> <newline> <postal-code> <whitespace> <city-name>

<street-address> ::= <street-name> <whitespace> <house-number>
<street-name> ::= <word-sequence>
<house-number> ::= <digit-sequence>

<postal-code> ::= <digit-sequence> <whitespace> <letter> <letter>
<city-name> ::= <word-sequence>

<word-sequence> ::= <word> | <word> <whitespace> <word-sequence>
<word> ::= <letter> | <letter> <word>
<digit-sequence> ::= <digit> | <digit> <digit-sequence>

<letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<whitespace> ::= " "
<newline> ::= "\n"
"""


@dataclass(frozen=True)
class PostalCode:
    number_part: int
    letter_1: str
    letter_2: str


@dataclass(frozen=True)
class StreetAddress:
    street: str
    house_number: int


@dataclass(frozen=True)
class DutchAddress:
    street_address: StreetAddress
    city: str
    postal_code: PostalCode


newline = char('\n')
whitespace = char(' ')
digit = (
    char('0')
    | char('1')
    | char('2')
    | char('3')
    | char('4')
    | char('5')
    | char('6')
    | char('7')
    | char('8')
    | char('9')
)
letter = char_in(string.ascii_uppercase)

digit_sequence = int * (''.join * many(digit))
word = ''.join * many(letter)
word_sequence = ' '.join * separated_by(word, separator=whitespace)

city_name = word_sequence
postal_code = PostalCode * (digit_sequence < whitespace) & letter & letter

street_name = word_sequence
house_number = digit_sequence
street_address = StreetAddress * (street_name < whitespace) & house_number

dutch_address = DutchAddress * (street_address < newline) & (postal_code < whitespace) & city_name


if __name__ == '__main__':
    example_address = "TWEEDE BANANENSTRAAT 67\n1012 AB KOMKOMMERVILLE"

    pprint(dutch_address(example_address).result)

