import string
import sys

# Jordan Giacone
# CS3500 - Section A
# Homework 3 - Recursive Descent Parser for Robolang
# 11/9/16
# The robolang parser

# Important global variable
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

    # If the next token is in the first set of relation
    if tokens[1] in ["<", ">", "=", "#"]:
        get_token()
        get_token()

        return is_simple_expression()

    return True


def is_simple_expression():
    # SimpleExpression := Term { AddOperator Term }

    if is_term():
        # If token is in first set of addOperator
        while tokens[1] in ["+", "-", "or"]:
            get_token()
            if is_add_operator():
                get_token()

                if not is_term():
                    return False
    else:
        return False

    return True


def is_term():
    # Term := Factor { MulOperator Factor }

    if is_factor():
        # If token is in first set of MulOperator
        while tokens[1] in ["*", "/", "and"]:
            get_token()

            if is_mul_operator():
                get_token()

                if not is_factor():
                    return False
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
        get_token()
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
                        if tokens[1] == "else":
                            get_token()
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
                    get_token()
                    if is_statement_sequence():
                        get_token()

                        return tokens[0] == "endw"

    return False


def is_statement():
    # Statement := [ Assignment | IfStatement | LoopStatement | FwdStatement | RotStatement ]

    # If token is in first set of assignment
    if is_identifier(tokens[0]):
        return is_assignment()
    elif tokens[0] == "if":
        return is_if_statement()
    elif tokens[0] == "while":
        return is_loop_statement()
    elif tokens[0] == "forward":
        return is_fwd_statement()
    elif tokens[0] == "rotate":
        return is_rot_statement()
    # The next token is in the follow set of statement
    elif tokens[0] in {"endw", "blorp", "else", "endif", "while", "rotate", "forward", "if"} \
            or is_identifier(tokens[0]):
        return True

    return False


def is_statement_sequence():
    # StatementSequence = Statement { Statement }

    if is_statement():

        while tokens[1] in ["while", "rotate", "if", "forward"] or is_identifier(tokens[1]):
            get_token()
            if not is_statement():
                return False

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

                if tokens[1] in ["while", "rotate", "if", "forward"] or is_identifier(tokens[1]):
                    get_token()
                    if is_statement_sequence():
                        get_token()

                        return tokens[0] == "blorp"
                    return False
                return tokens[0] == "blorp"

    return False


def is_routine_sequence():
    # RoutineSequence := RoutineDeclaration { RoutineDeclaration }

    if is_routine_declaration():
        # If current token is in first set of routineDeclaration
        while len(tokens) > 1 and tokens[1] in ["prog"]:
            get_token()
            if not is_routine_declaration():
                return False

        return True

    return False


def get_token():
    # Remove the desired tokens[0] from the front
    if len(tokens) > 1:
        tokens.pop(0)
    else:
        print("Error: Ran out of tokens!")
        exit(1)


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
    for line in sys.stdin:
        for a_token in line.split(" "):
            a_token = a_token.strip("\n")
            if a_token != "":
                tokens.append(a_token)

    if is_routine_sequence():
        print("CORRECT")
    else:
        print("INVALID!")

if __name__ == "__main__":
    main()
