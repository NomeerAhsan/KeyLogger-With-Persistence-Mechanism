import re

SHIFT_MAP = {
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
    '0': ')',
    '-': '_',
    '=': '+',
    '[': '{',
    ']': '}',
    ';': ':',
    "'": '"',
    ',': '<',
    '.': '>',
    '/': '?',
    '\\': '|',
    '`': '~'
}

def decode_log(log_path):

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    data = data.replace("�", "")

    # -----------------------------------------
    # TOKENIZE
    # -----------------------------------------

    tokens = re.findall(r'\[.*?\]|.', data)

    output = ""

    shift_active = False
    caps_active = False

    for token in tokens:

        # -----------------------------------------
        # SHIFT STATE
        # -----------------------------------------

        if token == "[shift_down]":
            shift_active = True
            continue

        elif token == "[shift_up]":
            shift_active = False
            continue

        # -----------------------------------------
        # CAPS STATE
        # -----------------------------------------

        elif token == "[cap]":
            caps_active = not caps_active
            continue

        # -----------------------------------------
        # SPECIAL TAGS
        # -----------------------------------------

        elif token == "[enter]":
            output += "\n"
            continue

        elif token == "[tab]":
            output += "\t"
            continue

        elif token == "[backspace]":
            output = output[:-1]
            continue

        elif token in ("[control]", "[alt]"):
            continue

        # -----------------------------------------
        # NORMAL CHARACTER
        # -----------------------------------------

        ch = token

        # LETTERS
        if ch.isalpha():

            # DEFAULT = lowercase
            # only uppercase if inside caps/shift
            if shift_active or caps_active:
                output += ch.upper()

            else:
                output += ch.lower()

        # NUMBERS / SYMBOLS
        else:

            # SHIFTED NUMBER -> SPECIAL SYMBOL
            if shift_active and ch in SHIFT_MAP:
                output += SHIFT_MAP[ch]

            else:
                output += ch

    return output



decoded = decode_log("log.txt")

print("\n========== DECODED OUTPUT  ==========\n")
print(decoded)