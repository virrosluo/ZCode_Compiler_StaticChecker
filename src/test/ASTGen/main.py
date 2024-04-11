import ASTGenExpect 
import os

INPUT_PATH = "..//CheckerSuite.py"
SOLUTION_FOLDER = "..//solutions"

if __name__ == '__main__':

    print("[+] Reading Code File...")
    code_data = ASTGenExpect.read_genFile(INPUT_PATH)

    print("[+] Parsing Code File...")
    fn_dict = ASTGenExpect.parse_functions(code_data)

    print("[+] Appending Expect To Function...")
    for fn_name, fn_info in fn_dict.items():
        fn_dict[fn_name] = ASTGenExpect.append_expect(fn_info, SOLUTION_FOLDER)

    print("[+] Writing out Code File...")
    with open('CheckerSuite.py', 'w') as f:
        f.write("""import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):\n""")
        
        for fn_name, fn_info in fn_dict.items():
            f.write(ASTGenExpect.fn2str(fn_name, fn_info) + "\n\n")