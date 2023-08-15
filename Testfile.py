"""
>>> run_file("Tests/test1.lox")
4
5
6
7
8
9
10
2
done
>>> run_file("Tests/test2.lox")
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Too many potatoes.
>>> run_file("Tests/test3.lox")
No words left
Not lonely
Lonely
Nathan
Not lonely
Lonely
Joel
Nah
Lonely
>>> run_file("Tests/test4.lox")
[line 6] Unexpected character. $
>>> run_file("Tests/test5.lox")
[line 22] Error at '}': Expect expression.
>>> run_file("Tests/test6.lox")
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Potato
Too many potatoes.
>>> run_file("Tests/test7.lox")
[line 25] Error at end: Expect ';' after value.
>>> run_file("Tests/test8.lox")
Potato
Potato
Potato
Potato
Potato
Too many potatoes.
>>> run_file("Tests/test9.lox")
[line 5] Error at 'b': Expect ';' after expression.
[line 13] Error at 'if': Expect ';' after variable declaration.
[line 20] Error at '}': Expect ';' after expression.
[line 25] Error at end: Expect ';' after value.
>>> run_file("Tests/test10.lox")
>>> run_file("Tests/test11.lox")
Undefined variable 'c'
[line 5]
>>> run_file("Tests/test12.lox")
Undefined variable 'c'
[line 6]
>>> run_file("Tests/test13.lox")
Operands must be two numbers or two strings.
[line 8]
>>> run_file("Tests/test14.lox")
Operands must be numbers.
[line 8]
>>> run_file("Tests/test15.lox")
Operand must be a number.
[line 8]
>>> run_file("Tests/test16.lox")
[line 2] Error at ';': Expect ')' after expression.
>>> run_file("Tests/test17.lox")
[line 1] Error at 'true': Expect '(' after 'if'.
[line 4] Error at 'print': Expect ')' after if condition.
>>> run_file("Tests/test18.lox")
[line 3] Error at 'var': Expect '(' after 'for'.
[line 5] Error at ';': Expect ')' after for clauses.
[line 8] Error at end: Expect ';' after loop condition.
>>> run_file("Tests/test19.lox")
[line 3] Error at ';': Expect variable name.
[line 5] Error at 'print': Expect ';' after variable declaration.
[line 6] Error at '=': Invalid assignment target.
[line 8] Error at end: Expect ';' after expression.
[line 8] Error at end: Expect '}' after block.
>>> run_file("Tests/test20.lox")
[line 1] Error at 'true': Expect '(' after 'while'.
[line 3] Error at ';': Expect ')' after condition.
"""
import sys
from Scanner import Scanner
from Interpreter import Interpreter
from Parser import Parser
from Resolver import Resolver

def run_file(file_path):
    """This function is executed when two
    arguments are passed in the command-line.
    The second argument is a file path to open and
    read all its lines. An exception is raised if the
    file path is not found.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > 0 and lines[0][-1] == '\n':
                lines.append("")
            scnr = Scanner(lines)
            token_list = scnr.get_tokens()
            if scnr.lox_error == False:
                parser = Parser(token_list)
                abstract_syntax_tree = parser.parse()
                if parser.lox_error == False:
                    interpreter = Interpreter(abstract_syntax_tree)
                    resolver = Resolver(interpreter)
                    resolver.resolve(abstract_syntax_tree)
                    if resolver.lox_error == False:
                        interpreter.interpret(interpreter.tree)
    except FileNotFoundError:
        print("File Not Found")
    except SystemExit:
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()