import regex as re
from kolibri.data.ressources import resources
from pathlib import Path
from kdmt.file import read_json_file

patterns_file=resources.get(str(Path('modules', 'regexes', 'defaults.json'))).path
patterns=read_json_file(patterns_file)


# Programmatically compile regex patterns and put them in the global scope
__g = globals()


def compile_patterns_in_dictionary(dictionary):
    """
    Replace all strings in dictionary with compiled
    version of themselves and return dictionary.
    """
    for name, regex_str in dictionary.items():
        print(name)
        if isinstance(regex_str, dict) and ("value" in regex_str) and ("flags" in regex_str):
            dictionary[name] = re.compile(regex_str["value"], eval(regex_str["flags"]))
        if isinstance(regex_str, str):
            dictionary[name] = re.compile(regex_str)
        elif isinstance(regex_str, dict) and "value" not in regex_str:
            compile_patterns_in_dictionary(regex_str)
    return dictionary

for (name, regex_variable) in patterns.items():
    print(name)
    if isinstance(regex_variable, str):
        # The regex variable is a string, compile it and put it in the
        # global scope
        __g[name] = re.compile(regex_variable)
    elif isinstance(regex_variable, dict):
        # The regex variable is a dictionary, convert all regex strings
        # in the dictionary to their compiled versions and put the variable
        # in the global scope
        __g[name] = compile_patterns_in_dictionary(regex_variable)




