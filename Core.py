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

def run_prompt():
    """This function gets called if only one
    argument gets passed in the command-line.
    It continuously prompts the user to enter a
    line of lox code. Control-Z terminates the program.
    """
    scnr = Scanner([])
    while(True):
        try:
            line = input("> ")
            scnr.set_source([line])
            token_list = scnr.get_tokens()
            if scnr.lox_error == False:
                parser = Parser(token_list)
                abstract_syntax_tree = parser.parse()
                if parser.lox_error == False:
                    interpreter = Interpreter(abstract_syntax_tree)
                    resolver = Resolver(interpreter)
                    resolver.resolve(abstract_syntax_tree)
                    if resolver.lox_error == False:
                        interpreter.interpret(abstract_syntax_tree)
            scnr.lox_error = False
        except EOFError:
            break
        except SystemExit:
            break

if len(sys.argv) > 2:
    print("Usage: plox [script]")
    exit(64)
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
else:
    run_prompt()