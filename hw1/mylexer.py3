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
    num_lines = int(input())
    print("Attempting to identify {} words".format(num_lines))

    for x in range(num_lines):
        # Read the next word
        word = input()
        if is_integer(word):
            print("Integer")
        elif is_decimal(word):
            print("Decimal")
        elif is_scientific(word):
            print("Scientific")
        elif is_hex(word):
            print("Hex")
        elif is_phone_number(word):
            print("Phone number")
        elif is_keyword(word):
            print("Keyword")
        elif is_identifier(word):
            print("Identifier")
        else:
            print("Invalid")
