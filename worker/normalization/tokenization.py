import re
from typing import List, Tuple


def tokenize_with_punctuation(text: str) -> List[Tuple[str, str]]:
    tokens = []
    
    # Pattern: word characters with apostrophes as part of words, whitespace, or single punctuation
    pattern = re.compile(r"(\w+(?:'\w*)*|\s+|\S)")

    for match in pattern.finditer(text):
        token = match.group(0)
        if token.isspace():
            tokens.append((token, 'space'))
        elif re.match(r'\w', token):
            tokens.append((token, 'word'))
        else:
            # Only treat as punctuation if it's not an apostrophe
            if token == "'":
                # Standalone apostrophe - could be word or punct depending on context
                # Treat as punct for now
                tokens.append((token, 'punct'))
            else:
                tokens.append((token, 'punct'))

    return tokens


def detokenize(tokens: List[Tuple[str, str]]) -> str:
    """
    Reconstruct text from tokenized list, preserving spaces and punctuation.
    """
    return ''.join(token for token, _ in tokens)