import re
import os

def read_genFile(path: str) -> str:
    with open(path, 'r') as f:
        data = f.read()

    return data

def parse_functions(code: str) -> dict:
    def remove_empty_str(lst:list[str]) -> list[str]: return [i for i in lst if i != '']

    function_pattern = r'def\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*:|input\s*=\s*"""(.*?)"""|expect\s*=\s"""*(.*?)"""|self.assertTrue\s*\(\s*TestChecker.test\s*\(\s*input\s*,\s*expect\s*,\s*(.*?)\)\s*\)'
    function_defs = re.findall(function_pattern, code, re.DOTALL)

    if len(function_defs) % 4 != 0: 
        raise Exception("The input does not follow the format")

    num_functions = int(len(function_defs) / 4)

    function_dict = {}
    for i in range(num_functions):
        try:
            [fn_name, fn_param] = remove_empty_str(function_defs[4*i + 0])
            [input_str] = remove_empty_str(function_defs[4*i + 1])
            [expect_str] = remove_empty_str(function_defs[4*i + 2])
            [tc_num] = remove_empty_str(function_defs[4*i + 3])
        except Exception as e:
            print("Parse item have some unexpected value in list: ", e)
        function_dict[fn_name] = {'fn_param': fn_param, 'input_str': input_str, 'expect_str': expect_str, 'tc_num': tc_num}

    return function_dict

def append_expect(fn_info: dict, solution_folder: str) -> dict:
    with open(
        os.path.join(solution_folder, fn_info['tc_num'] if '.txt' in fn_info['tc_num'] else fn_info['tc_num'] + '.txt')
        , 'r') as f:
        expect = f.read()
        expect = expect.replace('\\', '\\\\')

    fn_info['expect_str'] = expect
    return fn_info

def fn2str(fn_name:str, fn_info:dict) -> str:
    output = f"""\tdef {fn_name}({fn_info['fn_param']}):
\t\tinput = \"\"\"{fn_info['input_str']}\"\"\"
\t\texpect = \"\"\"{fn_info['expect_str']}\"\"\"
\t\tself.assertTrue(TestChecker.test(input,expect,{int(fn_info['tc_num'])}))"""
    return output