import regex as re
from kolibri.data.ressources import resources
from pathlib import Path
from kdmt.file import read_json_file

patterns_file=resources.get(str(Path('corpora', 'gazetteers', 'default', 'regexes.json'))).path
patterns=read_json_file(patterns_file)


# Programmatically compile regex patterns and put them in the global scope
__g = globals()


def compile_patterns_in_dictionary(dictionary):
    """
    Replace all strings in dictionary with compiled
    version of themselves and return dictionary.
    """
    for key, value in dictionary.items():
        if isinstance(value, str):
            dictionary[key] = re.compile(value)
        elif isinstance(value, dict):
            compile_patterns_in_dictionary(value)
    return dictionary

for (name, regex_variable) in patterns.items():

    if isinstance(regex_variable, str):
        # The regex variable is a string, compile it and put it in the
        # global scope
        __g[name] = re.compile(regex_variable)
    elif isinstance(regex_variable, dict):
        # The regex variable is a dictionary, convert all regex strings
        # in the dictionary to their compiled versions and put the variable
        # in the global scope
        __g[name] = compile_patterns_in_dictionary(regex_variable)




