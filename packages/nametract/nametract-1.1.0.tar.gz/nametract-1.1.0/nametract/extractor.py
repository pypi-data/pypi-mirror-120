from typing import List
from nametract.tokenizer import *


def maybe_name(inp: Token, minimal_name_size: int) -> bool:
    return inp.token_type == TokenEnum.Literal and len(inp.contents) >= minimal_name_size and inp.contents[0].isupper()


def build_name(parts: List[str]) -> str:
    tmp_s = []

    for part in parts:
        if part == "-":
            tmp_s.append(part)
        else:
            if len(tmp_s) != 0 and tmp_s[-1][-1] != "-":  # Don't want to add whitespaces near "-"
                tmp_s.append(" ")
            tmp_s.append(part)

    return "".join(tmp_s)


def extract(inp: str, minimal_name_size=1, ignore_sentence_start=True) -> List[str]:
    """
    Extract anything that might be a name from text. Ignores things in the start of the sentence.
    :param inp: Text string to extract names from
    :param minimal_name_size: Minimal size (>=) of name, or of part of name from many words. Useful for filtering out things like "I"
    :param ignore_sentence_start: Whether to ignore words starting with capitals in the beginning of the sentences
    :return: List of strings with possible names
    """

    # Add additional punctuation in the end to ensure last word is processed
    tokens = tokenize(inp) + [Token(".", token_type=TokenEnum.Punctuation)]

    answ = []
    current_name = []
    ignore_next = ignore_sentence_start

    for i, token in enumerate(tokens):
        if token.token_type == TokenEnum.Punctuation and token.contents in "-—" and (i != len(tokens) - 1 and i != 0) \
                and maybe_name(tokens[i - 1], minimal_name_size=minimal_name_size) \
                and maybe_name(tokens[i + 1], minimal_name_size=minimal_name_size):
            current_name.append("-")
            continue

        if maybe_name(token, minimal_name_size) and \
                (not ignore_next or (i != len(tokens) - 1 and maybe_name(tokens[i + 1], minimal_name_size))):
            current_name.append(token.contents)
        elif not maybe_name(token, minimal_name_size) and len(current_name) > 0:
            answ.append(build_name(current_name))
            current_name = []

        if ignore_next:
            ignore_next = False

        if ignore_sentence_start and token.token_type == TokenEnum.Punctuation and token.token_type == ".":
            ignore_next = True

    return answ
