from typing import List, Optional
from enum import Enum
import string
from dataclasses import dataclass


class TokenEnum(Enum):
    Literal = 1
    Number = 2
    Punctuation = 3


@dataclass
class Token:
    contents: str
    token_type: TokenEnum


def char_type(c: str) -> Optional[TokenEnum]:
    if c.isalpha():
        return TokenEnum.Literal
    elif c.isalnum():
        return TokenEnum.Number
    elif c in string.whitespace:
        return None
    else:
        return TokenEnum.Punctuation


def tokenize(inp: str) -> List[Token]:
    if len(inp) == 0:
        return []

    tokens = []
    token_start = 0
    token_type = char_type(inp[0])

    for i in range(len(inp)):
        if token_type is None:
            token_start = i
            token_type = char_type(inp[i])

        if (inp[i] in string.whitespace and token_type is not None) or (token_type != char_type(inp[i])):
            tokens.append(Token(inp[token_start:i], token_type))


            token_start = i
            token_type = char_type(inp[i])

    if token_type is not None:
        tokens.append(Token(inp[token_start:], token_type))

    return tokens
