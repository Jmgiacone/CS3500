import string


def main():
    num_lines = int(input())
    print("Attempting to identify {} words".format(num_lines))

    for i in range(num_lines):
        # Read the next word
        current_word = input()
        print("{}: ".format(i + 1), end="")

        if is_integer(current_word):
            print("Integer")
        elif is_decimal(current_word):
            print("Decimal")
        elif is_scientific(current_word):
            print("Scientific")
        elif is_hex(current_word):
            print("Hex")
        elif is_phone_number(current_word):
            print("Phone number")
        elif is_keyword(current_word):
            print("Keyword")
        elif is_identifier(current_word):
            print("Identifier")
        else:
            print("Invalid")


def is_integer(word):
    state = 1

    for current_char in word:
        if state == 1:
            if current_char in string.digits:
                state = 3
            elif current_char in ['+', '-']:
                state = 2
            else:
                return False
        elif state == 2:
            if current_char in string.digits:
                state = 3
            else:
                return False
        else:
            if current_char in string.digits:
                state = 3
            else:
                
                return False
    
    return state == 3


def is_decimal(word):
    # Check to see where the period is in the string
    try:
        period_index = list(word).index(".")
    except ValueError:
        # No period, automatically not a decimal
        return False

    # The part before the period is not an integer
    if not is_integer(word[:period_index]):
        return False

    # Start the automaton from the character after '.'
    word = word[period_index + 1:]
    state = 1

    for current_char in word:
        if state == 1:
            if current_char in string.digits:
                state = 2
            else:
                return False
        else:
            if current_char not in string.digits:
                return False

    return state == 2


def is_scientific(word):
    # Check to see if there is an 'E' in the word
    try:
        e_index = list(word).index("E")
    except ValueError:
        # No 'E' in the string, can't be a scientific number
        return False

    if not is_decimal(word[:e_index]):
        return False

    word = word[e_index + 1:]
    state = 1

    for current_char in word:
        if state == 1:
            if current_char == "0":
                pass
            elif current_char in string.digits:
                state = 3
            elif current_char in ["+", "-"]:
                state = 2
            else:
                return False
        elif state == 2:
            if current_char == 0:
                pass
            elif current_char in string.digits:
                state = 3
            else:
                return False
        else:
            if current_char not in string.digits:
                return False

    return state == 3


def is_hex(word):
    # First 6 ascii letters in uppercase: [A, B, C, D, E, F]
    uppercase_hex_digits = string.ascii_uppercase[:6]
    state = 1

    for current_char in word:      
        if state == 1:
            if current_char in string.digits or current_char in uppercase_hex_digits:
                state = 2
            elif current_char == "H":
                return False
            else:
                return False
        elif state == 2:
            if current_char in string.digits or current_char in uppercase_hex_digits:
                pass
            elif current_char == "H":
                state = 3
            else:
                return False
        elif state == 3:
            return False

    return state == 3


def is_phone_number(word):
    return False


def is_keyword(word):
    state = 1

    for current_char in word:
        if state == 1:
            if current_char == "w":
                state = 2
            elif current_char == "e":
                state = 3
            elif current_char == "p":
                state = 10
            else:
                return False
        elif state == 2:
            if current_char == "h":
                state = 4
            else:
                return False
        elif state == 3:
            if current_char == "l":
                state = 5
            elif current_char == "n":
                state = 6
            else:
                return False
        elif state == 4:
            if current_char == "i":
                state = 7
            else:
                return False
        elif state == 5:
            if current_char == "s":
                state = 8
            else:
                return False
        elif state == 6:
            if current_char == "d":
                state = 9
            else:
                return False
        elif state == 7:
            if current_char == "l":
                state = 8
            else:
                return False
        elif state == 8:
            if current_char == "e":
                state = 9
            else:
                return False
        elif state == 10:
            if current_char == "r":
                state = 11
            else:
                return False
        elif state == 11:
            if current_char == "i":
                state = 12
            else:
                return False
        elif state == 12:
            if current_char == "n":
                state = 13
            else:
                return False
        elif state == 13:
            if current_char == "t":
                state = 9
            else:
                return False

    return state == 9


def is_identifier(word):
    state = 1

    # Keywords can't be identifiers or hex numbers
    if is_keyword(word) or is_hex(word):
        return False

    for current_char in word:
        if state == 1:
            if current_char in string.ascii_letters:
                state = 2
            else:
                return False
        else:
            if not (current_char in string.ascii_letters or current_char in string.digits or current_char == "_"):
                return False

    return state == 2


# Main code
if __name__ == "__main__":
    main()
