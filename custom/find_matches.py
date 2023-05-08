import difflib


def find_most_accurate(wordlist: list[str], typo: str) -> list[str]:
    matches = []
    precision = -1  # higher is better
    for word in wordlist:
        p = 0
        prev = ""
        for _, s in enumerate(difflib.ndiff(word, typo)):
            if s[0] == " " or (prev == "-" and s[0] == "+"):
                p += 1
            prev = s[0]
        if matches and precision < p:
            matches = [word]
            precision = p
        elif not matches or precision == p:
            matches += [word]
            precision = p
    return matches
