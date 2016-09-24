def main():
    num_lines = int(input())
    print("Attempting to identify {} words".format(num_lines))

    for x in range(num_lines):
        # Read the next word
        current_word = input()
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
    return False


def is_decimal(word):
    return False


def is_scientific(word):
    return False


def is_hex(word):
    return False


def is_phone_number(word):
    return False


def is_keyword(word):
    return False


def is_identifier(word):
    return False


# Main code
if __name__ == "__main__":
    main()
