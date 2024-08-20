from bot.classes import BaseCommand

import difflib
import html


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


def command_entry(lang, cmd: BaseCommand, entry: str = None, inline_notice: bool = True):
    return (
        (
            f"""<code>/{cmd.name} {" ".join(cmd.args)}</code>\n"""
            + (
                lang.ALIASES
                + ": <code>/"
                + ("</code>, <code>/".join(cmd.aliases))
                + "</code>\n"
                if cmd.aliases
                else ""
            )
            + "\n"
            + (lang.COMMANDS.get(cmd.name) or "")
            + ("\n\n" + lang.INLINE_MODE_NOTICE if inline_notice else "")
        ) if cmd
        else lang.NO_ENTRY_FOR.format(html.escape(entry)) if entry
        else lang.NO_ENTRY
    )
