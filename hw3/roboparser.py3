import string
import sys
import copy

# Important global variables
tokens = []


def is_relation():
    # Relation :=   < | > | = | #
    return tokens[0] == "<" or tokens[0] == ">" or tokens[0] == "=" or tokens[0] == "#"


def is_add_operator():
    # AddOperator :=   + | - | or

    return tokens[0] == "+" or tokens[0] == "-" or tokens[0] == "or"


def is_mul_operator():
    # MulOperator :=   * | / | and
    return tokens[0] == "*" or tokens[0] == "/" or tokens[0] == "and"


def is_expression():
    # Expression := SimpleExpression [ Relation SimpleExpression ]

    if not is_simple_expression():
        return False

    get_token()

    if is_relation():
        get_token()

        return is_simple_expression()

    return True


def is_simple_expression():
    # SimpleExpression := Term { AddOperator Term }

    if is_term():
        get_token()

        while is_add_operator():
            get_token()

            if is_term():
                get_token()
            else:
                return False
    else:
        return False

    return True


def is_term():
    # Term := Factor { MulOperator Factor }

    if is_factor():
        previous_tokens = copy.deepcopy(tokens)
        get_token()

        while is_mul_operator():
            get_token()

            if is_factor():
                get_token()
            else:
                return False
        tokens.clear()
        tokens.extend(previous_tokens)
    else:
        return False

    return True


def is_factor():
    # Factor :=  integer | decimal | identifier | ( Expression ) | ~ Factor

    if is_integer(tokens[0]) or is_decimal(tokens[0]) or is_identifier(tokens[0]):
        return True

    if tokens[0] == "(":
        get_token()

        if is_expression():
            get_token()

            return tokens[0] == ")"
    elif tokens[0] == "~":
        return is_factor()

    return False


def is_assignment():
    # Assignment := identifier is Expression !

    if is_identifier(tokens[0]):
        get_token()

        if tokens[0] == "is":
            get_token()

            if is_expression():
                get_token()

                return tokens[0] == "!"
    return False


def is_fwd_statement():
    # FwdStatement := forward ( Expression )!
    if tokens[0] == "forward":
        get_token()

        if tokens[0] == "(":
            get_token()

            if is_expression():
                get_token()

                if tokens[0] == ")":
                    get_token()

                    return tokens[0] == "!"

    return False


def is_rot_statement():
    # RotStatement = rotate (  Expression )!

    if tokens[0] == "rotate":
        get_token()

        if tokens[0] == "(":
            get_token()

            if is_expression():
                get_token()

                if tokens[0] == ")":
                    get_token()

                    return tokens[0] == "!"

    return False


def is_if_statement():
    # IfStatement := if ( Expression ) StatementSequence [ else StatementSequence ] endif

    if tokens[0] == "if":
        get_token()

        if tokens[0] == "(":
            get_token()

            if is_expression():
                get_token()

                if tokens[0] == ")":
                    get_token()

                    if is_statement_sequence():
                        get_token()

                        if tokens[0] == "else":
                            # Hit option else part
                            get_token()

                            if is_statement_sequence():
                                get_token()

                                return tokens[0] == "endif"

                        else:
                            return tokens[0] == "endif"

    return False


def is_loop_statement():
    # LoopStatement = while ( Expression ) StatementSequence endw

    if tokens[0] == "while":
        get_token()

        if tokens[0] == "(":
            get_token()

            if is_expression():
                get_token()

                if tokens[0] == ")":
                    if is_statement_sequence():
                        get_token()

                        return tokens[0] == "endw"

    return False


def is_statement():
    # Statement := [ Assignment | IfStatement | LoopStatement | FwdStatement | RotStatement ]

    temp_tokens = copy.deepcopy(tokens)
    if is_assignment():
        return True

    tokens.clear()
    tokens.extend(temp_tokens)

    if is_if_statement():
        return True

    tokens.clear()
    tokens.extend(temp_tokens)

    if is_loop_statement():
        return True

    tokens.clear()
    tokens.extend(temp_tokens)

    if is_fwd_statement():
        return True

    tokens.clear()
    tokens.extend(temp_tokens)

    if is_rot_statement():
        return True

    tokens.clear()
    tokens.extend(temp_tokens)

    return tokens[0] in {"endw", "blorp", "else", "endif"}


def is_statement_sequence():
    # StatementSequence = Statement { Statement }

    if is_statement():
        get_token()

        while is_statement():
            get_token()

        return True
    else:
        return False


def is_routine_declaration():
    # RoutineDeclaration := prog identifier blip [ StatementSequence ] blorp

    if tokens[0] == "prog":
        get_token()

        if is_identifier(tokens[0]):
            get_token()

            if tokens[0] == "blip":
                get_token()

                if is_statement_sequence():
                    get_token()

                    return tokens[0] == "blorp"
                return tokens[0] == "blorp"

    return False


def is_routine_sequence():
    # RoutineSequence := RoutineDeclaration { RoutineDeclaration }

    if is_routine_declaration():
        get_token()

        while is_routine_declaration():
            get_token()

        return True

    return False


def get_token():
    # Remove the desired tokens[0] from the front
    if len(tokens) > 0:
        tokens.pop(0)


def is_integer(word):
    state = 1

    for current_char in word:
        if state == 1:
            if current_char in string.digits:
                state = 3
            elif current_char in ['+'" or word == "'-']:
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
        # No period" or word == "automatically not a decimal
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


def is_keyword(word):
    return word == "=" or word == "+" or word == "-" or word == "*" or word == "/" or word == " or" or word == "and" \
           or word == "~" or word == "(" or word == ")" or word == "<" or word == ">" or word == "= " or word == "!" \
           or word == "forward" or word == "rotate" or word == "if" or word == "endif" or word == "else" \
           or word == "while" or word == "endw" or word == "prog" or word == "blip" or word == "blorp"


def is_identifier(word):
    state = 1

    # Keywords can't be identifiers or hex numbers
    if is_keyword(word):
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


def main():
    """inputs = input().split(" ")

    for a_token in inputs:
        a_token = a_token.strip("\n")

        if a_token != "":
            tokens.append(a_token)"""

    tokens_literal = ["prog", "main", "blip", "x", "is", "2", "+", "2", "!", "forward", "(", "x", "*", "100", ")", "!", "blop"]

    for a_token in tokens_literal:
        tokens.append(a_token)
    """for line in sys.stdin:
        for a_token in line.split(" "):
            a_token = a_token.strip("\n")

            if a_token != "":
                tokens.append(a_token)
                print(a_token)

    print(tokens)"""

    if is_routine_sequence():
        print("CORRECT")
    else:
        print("INVALID!")

if __name__ == "__main__":
    main()
