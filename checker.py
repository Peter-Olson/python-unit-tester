import os
import ast
import inspect
from os import listdir
from os.path import isfile, join

import P2_CHECKER_CONNECT_FOUR
IMPORT_NAME = P2_CHECKER_CONNECT_FOUR
module_name = "P2_CHECKER_CONNECT_FOUR"

"""
    Checker Program

    Checker is used for checking student python files and running
    unit tests for student-written functions / programs

    @author Peter Olson
    @version 2.13.25
"""

# ---------------------------------------------------------------------------------------------
# Convert .py to .txt. Collect function names in a list.
# --> Run functions using getattr + parameters. Probably want to decorate correct functions
# --> to run using some identifiable token, e.g. foo_<original_function_name>, search for 'foo'
# Still requires running import file... amend by pushing all code into a block requiring the
# __name__ to be __main__, which would be false when running a script from a different .py file
# ---------------------------------------------------------------------------------------------

# Globals for functions
LIST_DELIMITER = ","  # Used to separate elements of a list
DATA_SEPARATOR = "|"  # Used to separate parameter values
ROW_SEPARATOR = "$"  # Used to separate rows
SET_AND_DICT_START = "{"  # Used to find beginning of set or dictionary
DICT_IDENTIFIER = ":"  # Used to differentiate between sets and dictionaries
SET_AND_DICT_END = "}"  # Used to find end of set or dictionary
TUPLE_START = "("  # Used to find beginning of tuple
TUPLE_END = ")"  # Used to find end of tuple
EXPECTED_IDENTIFIER = "EXPECTED"  # Used for expected output
# All 'foo_' functions are tested...
# Those without are not searched for
FUNCTION_NAME_IDENTIFIER = "foo_"
UNIT_TEST_TEXT_FILE_ROOT = "unit_tests_"


# Classes
class BColors:
    """
        Defines the colors for use in text output for the console
    """
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Functions


def fill_list(list_1d, arg_line):
    """
    Given a string with elements separated by a delimiter,
    fill a list with the elements

    :param list_1d: The list to fill
    :param arg_line: The arguments to put in the list, separated by
        LIST_DELIMITER
    """
    str_list = arg_line.split(LIST_DELIMITER)
    for token in str_list:
        list_1d.append(token)


def fill_2d_list(list_2d, arg_line):
    """
    Given a string with rows separated by a delimiter (ROW_SEPARATOR,
    and elements separated by a delimiter (LIST_DELIMITER),
    fill a 2D list with the elements

    :param list_2d: The 2D list to fill
    :param arg_line: The arguments to put into the 2D list, which are separated
        by ROW_DELIMITER and LIST_DELIMITER
    """
    row_text_list = arg_line.split(ROW_SEPARATOR)
    for row in row_text_list:
        row_list = []
        fill_list(row_list, row)
        list_2d.append(row_list)


def make_dct_from_text(data, args_obj_list):
    """
    Make a dictionary from text and put it in a list

    :param data: The text to convert to a dictionary
    :param args_obj_list: The list to put the dictionary into
    """
    dct = eval(data.replace("'", "\""))
    args_obj_list.append(dct)


def make_tuple_from_text(data, args_obj_list):
    """
    Make a tuple from text and put it in a list

    :param data: The data to convert to a tuple
    :param args_obj_list: The list to add the tuple to
    """
    # Convert text to a tuple using eval
    if LIST_DELIMITER in data:
        a_tuple = eval(data.replace("'", "\""))
        args_obj_list.append(a_tuple)
    # Tuples of size 1 are auto-converted from being
    # tuples to just converting to the element inside
    # so, must manually convert for size 1
    else:
        element = data[1:len(data)-1]
        a_tuple = (eval(element),)
        args_obj_list.append(a_tuple)


def make_set_from_text(data, args_obj_list):
    """
    Make a set from text and put it into a list

    :param data: The text to convert to a set
    :param args_obj_list: The list to add the set to
    """
    a_set = eval(data.replace("'", "\""))
    args_obj_list.append(a_set)


def make_1d_list_from_text(data, args_obj_list):
    """
    Make a 1d list from text and add it to a list

    :param data: The text to convert to a list
    :param args_obj_list: The list to add the list to
    """
    row_list = []
    fill_list(row_list, data)
    args_obj_list.append(row_list)


def make_2d_list_from_text(data, args_obj_list):
    """
    Make a 2D list from text and add it to a list

    :param data: The text to convert to a 2D list
    :param args_obj_list: The list to add the 2D list to
    """
    grid_list = []
    fill_2d_list(grid_list, data)
    args_obj_list.append(grid_list)


def _is_expected_line_data(line_data):
    """
    Determines if the text has the EXPECTED_IDENTIFIER in it or not

    :param line_data: The line to search in
    :return: True if EXPECTED_IDENTIFIER is in the text, False otherwise
    """
    return EXPECTED_IDENTIFIER in line_data


def _data_is_dct_or_set(line_data):
    """
    Determines if the text represents a dictionary or a set, or neither

    :param line_data: The text to check if the data represents a dictionary or
        a set, or neither
    :return: True if the data represents a dictionary or a set, False otherwise
    """
    return line_data.startswith(SET_AND_DICT_START) and \
        line_data.endswith(SET_AND_DICT_END)


def _data_is_tuple(line_data):
    """
    Determines if the text represents a tuple or not

    :param line_data: The text to check if it represents a tuple
    :return: True if the text represents a tuple, False otherwise
    """
    return line_data.startswith(TUPLE_START) and \
        line_data.endswith(TUPLE_END)


def _data_is_2d_list(line_data):
    """
    Determnes if the text represents a 2D list or not

    :param line_data: The text to check to see if it represents a 2D list
    :return: True if the text represents a 2D list, False otherwise
    """
    return ROW_SEPARATOR in line_data


def _data_is_1d_list(line_data):
    """
    Determine if the text represents a 1D list or not

    :param line_data: The text to check
    :return: True if the text represents a 1D list, False otherwise
    """
    return LIST_DELIMITER in line_data


def is_list(value):
    """
    Determine if the value is a list or not

    :param value: The value to check
    :return: True if the value is a list, False otherwise
    """
    return isinstance(value, list)


def is_2d_list(value):
    """
    Determine if the value is a 2D list or not

    :param value: The value to check
    :return: True if the value is a 2D list, False otherwise
    """
    return is_list(value) and isinstance(value[0], list)


def _convert_text_to_dct_or_sets(line_data, obj_list):
    """
    Convert the text to a dictionary or a set and add it to a list

    :param line_data: The text to convert
    :param obj_list: The list to add the dictionary or set to
    """
    #  Dictionaries
    if DICT_IDENTIFIER in line_data:
        make_dct_from_text(line_data, obj_list)
    #  Sets
    else:
        make_set_from_text(line_data, obj_list)


def _convert_line_data_to_list(line_data, obj_list):
    """
    Convert the text to the correct data type and add it to a list

    :param line_data: The text to convert
    :param obj_list: The list to add the converted data to
    """
    #  Dictionaries or Sets
    if _data_is_dct_or_set(line_data):
        _convert_text_to_dct_or_sets(line_data, obj_list)
    # Tuples
    elif _data_is_tuple(line_data):
        make_tuple_from_text(line_data, obj_list)
    #  2D Lists
    elif _data_is_2d_list(line_data):
        make_2d_list_from_text(line_data, obj_list)
    #  1D Lists
    elif _data_is_1d_list(line_data):
        make_1d_list_from_text(line_data, obj_list)
    # Everything else
    else:
        obj_list.append(line_data)


def _convert_line_data(line_data, args_obj_list, expected_list):
    """
    Convert text to the correct data type and add it to the argument object
    list or the expected object list

    :param line_data: The text to convert
    :param args_obj_list: The list containing argument values
    :param expected_list: The list containing expected values
    """
    # Convert argument text data and add to argument object list
    if not _is_expected_line_data(line_data):
        _convert_line_data_to_list(line_data, args_obj_list)
    #  Same thing, but for expected values
    else:
        expected_data = line_data.replace(EXPECTED_IDENTIFIER + " ", "")
        _convert_line_data_to_list(expected_data, expected_list)


def get_unit_tests(text_file_name):
    """
    Get the unit test input data and the expected values for all of the tests
    of a unit test text file

    :param text_file_name: The name of the unit test text file, which should have
        the format 'unit_tests_(p/h)#_#.txt'
    :return: The list of function arguments
    :return: The list of expected values
    """
    # Delimiters / Tokens for scraping data
    function_args = []
    expected_list = []

    text_file = open(text_file_name, "r")
    text_lines = text_file.readlines()

    #  Go through each line
    for text_line in text_lines:
        # Get list of parameters
        text_line = text_line.replace("\n", "")
        args_obj_list = []
        args_list = text_line.split(DATA_SEPARATOR)

        #  Go through each parameter
        for arg_num in range(0, len(args_list)):
            line_data = args_list[arg_num]
            _convert_line_data(line_data, args_obj_list, expected_list)

        #  Add list of arguments to the function arguments
        if EXPECTED_IDENTIFIER not in text_line:
            function_args.append(args_obj_list)

    return function_args, expected_list


# Round any float values or list of float values to only two decimal places. Leaves any other
# data unchanged
def round_any(value):
    """
    Round any float values or list of float values to only two decimal places.
    Leaves any other data unchanged

    :param value: A non-float, a float, or a list which may contain floats
    :return: The same value, but with all float values round to two decimal
        places
    """
    if isinstance(value, float):
        value = round(value, 2)
    elif isinstance(value, list):
        # Empty list
        if len(value) <= 0:
            return value
        # 2D list
        if isinstance(value[0], list):
            # Round decimals
            if isinstance(value[0][0], float):
                for row in range(0, len(value)):
                    for col in range(0, value[row]):
                        value[row][col] = round(value[row][col], 2)
        # 1D list
        else:
            # Round decimals
            if isinstance(value[0], float):
                for value_index in range(0, len(value)):
                    value[value_index] = round(value[value_index], 2)
    return value


def convert_str_list_to_type(str_list):
    """
    Convert a list of string literals to their proper data types using
    ast.literal_eval()

    :param str_list: A string representing a list
    """
    # Convert 1D lists
    if not isinstance(str_list[0], list):
        for list_index in range(0, len(str_list)):
            # Empty list
            if str_list[list_index] == '':
                str_list = []
                return str_list
            str_list[list_index] = ast.literal_eval(str_list[list_index])
    # Convert 2D lists
    else:
        convert_str_2d_list_to_type(str_list)


def convert_str_2d_list_to_type(str_list):
    """
    Convert 2D lists representing a string to their proper data types
    using ast.literal_eval()

    :param str_list: The string representing a 2D list
    """
    for row_index in range(0, len(str_list)):
        for col_index in range(0, len(str_list[row_index])):
            str_list[row_index][col_index] = ast.literal_eval(str_list[row_index][col_index])


def contains_explicit_return(f):
    """
    Determines whether a function contains an explicit return statement or not

    :param f: The function to check
    :return: True if the function contains an explicit return statement,
        False otherwise
    """
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))


def get_py_file_by_name(_only_files, _module_name):
    """
    Get the py file name based on the module name

    :param _only_files: The list of files in the current directory
    :param _module_name: The module name of the py file
    :return: The file string name for the .py file, or None if it is not found
    """
    for file in _only_files:
        file_name = os.path.splitext(file)

        # Only check .py files
        if ".py" not in file_name:
            continue

        # In the below if statement, there used to be a check to not check any
        # files with 'Solutions' in the title
        '''and "Solutions" not in file_name[0]'''

        # 'CHECKER' must be in the name, and _module_name must be in the file
        # name, and .txt cannot be the file type
        if "CHECKER" in file_name[0] and _module_name in file_name and ".txt" not in file_name[1]:
            py_file_str = file_name[0] + file_name[1]
            return py_file_str

    # The file was not found
    return None


def _find_correct_encoding(_py_file_name):
    """
    Find the correct encoding for the .py file by trying a bunch of different
    encodings

    :param _py_file_name: The name of the .py file
    :return: The lines of the .py file
    :return: The scanner object reading the file
    """
    # The list of encodings to check
    encoding_list = ['mbcs', 'utf8', 'utf_8', 'utf_16', 'cp437', 'utf16',
                     'ascii', 'big5', 'big5hkscs', 'cp037', 'cp273',
                     'cp424', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850',
                     'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860',
                     'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866',
                     'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950',
                     'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250',
                     'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255',
                     'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004',
                     'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030',
                     'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2',
                     'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                     'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3',
                     'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7',
                     'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11',
                     'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
                     'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048',
                     'mac_cyrillic', 'mac_greek', 'mac_iceland',
                     'mac_latin2', 'mac_roman', 'mac_turkish',
                     'ptcp154', 'shift_jis', 'shift_jis_2004',
                     'shift_jisx0213', 'utf_32', 'utf_32_be', 'utf_32_le',
                     'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8_sig']

    encoding_list_index = 0
    has_correct_char_decode = False
    py_file_lines = ""
    file_reader = None

    # Keep checking encodings until the correct one is found
    while not has_correct_char_decode:
        try:
            file_reader = open(_py_file_name, "r", encoding=encoding_list[encoding_list_index])
            py_file_lines = file_reader.readlines()
        except UnicodeDecodeError:
            encoding_list_index += 1
        else:
            has_correct_char_decode = True
            # print("debug: encoding is", encoding_list[encoding_list_index])

    return py_file_lines, file_reader


def get_lines_from_py_file(_py_file_name):
    """
    Get the lines from the .py file.

    If the .py file cannot be read, there may be an issue finding the correct
    encoding for the file. See _find_correct_encoding()

    :param _py_file_name: The name of the .py file to read
    :return: The list of string lines from the .py file
    """
    file_reader = None

    # Find the correct encoding
    try:
        file_reader = open(_py_file_name, "r")
        py_file_lines = file_reader.readlines()
    except UnicodeDecodeError:
        py_file_lines, file_reader = _find_correct_encoding(_py_file_name)
    else:
        # print("debug: no encoding")
        pass
    finally:
        if file_reader is None:
            print("No suitable encoding found for this file.")
            exit()

    return py_file_lines


def get_function_list(_lines):
    """
    Get the list of function names to test from the list of lines
    from the .py file

    :param _lines: The list of string lines from a .py file
    :return: The list of function names to be tested based on the
        FUNCTION_NAME_IDENTIFIER
    """
    function_name_list = []
    for line in _lines:
        function_header_identifier = "def "
        if function_header_identifier in line:
            # Get function name
            start_pos = line.find("def ") + len(function_header_identifier)
            end_pos = line.find("(", start_pos)
            function_name = line[start_pos:end_pos].strip()

            # Only functions containing the FUNCTION_NAME_IDENTIFIER are
            # checked by checker
            if FUNCTION_NAME_IDENTIFIER in function_name:
                function_name_list.append(function_name)

    return function_name_list


def convert_unit_test_value(unit_test_value):
    """
    Convert the unit test value to its correct data type

    :param unit_test_value: The unit test value to convert
    :return: The converted unit test value
    """
    # Check for iterables
    if isinstance(unit_test_value, dict) or \
            isinstance(unit_test_value, set) or \
            isinstance(unit_test_value, tuple):
        pass  # These are already in their correct format
    # Check non-list values
    elif not isinstance(unit_test_value, list):
        # Do not add value. Used for functions with no parameters
        if isinstance(unit_test_value, str) and len(unit_test_value) == 0:
            return

        try:
            unit_test_value = ast.literal_eval(unit_test_value)
        except ValueError:
            print("Conversion error")
            exit()
    # Convert elements inside list to their proper type
    else:
        convert_str_list_to_type(unit_test_value)

    return unit_test_value


def convert_list_arguments(_list_args):
    """
    Convert list argument data to their proper data type values

    :param _list_args: The list of arguments to be passed into the function
    """
    for unit_test_data_list_index in range(0, len(_list_args)):
        for unit_test_value_index in range(0, len(_list_args[unit_test_data_list_index])):
            unit_test_value = _list_args[unit_test_data_list_index][unit_test_value_index]
            unit_test_value = convert_unit_test_value(unit_test_value)
            _list_args[unit_test_data_list_index][unit_test_value_index] = unit_test_value


def _reformat_string_unit_test_values(unit_test_value):
    """
    Reformat string unit test values to their correct data type

    :param unit_test_value:
    :return:
    """
    # Already in correct format
    if isinstance(unit_test_value, dict) or \
            isinstance(unit_test_value, set) or \
            isinstance(unit_test_value, tuple):
        pass
    # Convert strings to lower case, except for string values that represent
    # booleans and None
    elif isinstance(unit_test_value, str):
        if unit_test_value != 'True' and unit_test_value != 'False' and \
                unit_test_value != 'None':
            unit_test_value = unit_test_value.lower()

    return unit_test_value


def convert_expected_unit_test_value(unit_test_value):
    """
    Convert expected unit test values to their proper data type

    :param unit_test_value: The unit test value to convert
    :return: The converted unit test value
    """
    # Convert non-lists
    if not isinstance(unit_test_value, list):
        # Skip iterables, which are in the correct format
        if isinstance(unit_test_value, dict) or \
                isinstance(unit_test_value, set) or \
                isinstance(unit_test_value, tuple):
            pass
        # Convert numbers
        elif unit_test_value.lstrip('-').replace('.', '', 1).isdigit():
            unit_test_value = ast.literal_eval(unit_test_value)
        # Convert boolean and None values
        elif unit_test_value == 'True' or unit_test_value == 'False' or unit_test_value == 'None':
            unit_test_value = ast.literal_eval(unit_test_value)
        # else, if we do have a string, do not call ast.literal_eval, which cannot convert
        # strings to strings apparently, which is stupid
    # Convert elements inside list to their proper type
    else:
        # Check for empty lists
        if len(unit_test_value) == 0:
            unit_test_value = []
        elif len(unit_test_value) == 1 and \
                (unit_test_value[0] == '' or
                 unit_test_value[0] == ""):
            unit_test_value = []
            convert_str_list_to_type(unit_test_value)
        elif len(unit_test_value) == 2 and \
                (unit_test_value[1] == '' or
                 unit_test_value[1] == ""):
            unit_test_value.pop(1)
            if unit_test_value[0] == '' or unit_test_value[0] == "":
                unit_test_value = []
            if len(unit_test_value) > 0:
                convert_str_list_to_type(unit_test_value)
        else:
            convert_str_list_to_type(unit_test_value)

    return unit_test_value


def convert_expected_value_list(_expected_value_list):
    """
    Convert the expected value list's data to the correct data types

    :param _expected_value_list: The list of expected values
    """
    for unit_test_value_index in range(0, len(_expected_value_list)):
        unit_test_value = _expected_value_list[unit_test_value_index]

        # Reformat strings
        unit_test_value = _reformat_string_unit_test_values(unit_test_value)

        # Convert unit test value to correct data type
        unit_test_value = convert_expected_unit_test_value(unit_test_value)

        # Round and set values to expected value list
        expected_value_correct_data_type = round_any(unit_test_value)
        _expected_value_list[unit_test_value_index] = expected_value_correct_data_type


def update_has_return_values_list(_function_obj, _has_return_values):
    """
    Update the has return value list, which keeps track of which functions have
    return statements or not

    :param _function_obj: The function object to check
    :param _has_return_values: The boolean list that keeps track of which
        functions have return statements or not
    """
    if contains_explicit_return(_function_obj):
        _has_return_values.append(True)
    else:
        _has_return_values.append(False)


def update_shallow_copy_list(
        _function_num, _has_return_values, _shallow_copy, _args):
    """
    Save copies of the argument data for functions that do not have return
    statements

    :param _function_num: The function number / ordinal
    :param _has_return_values: The boolean list that keeps track of which
        functions have return statements or not
    :param _shallow_copy: The list of argument data for functions that do not
        have return statements
    :param _args: The argument values that need to be added to the shallow copy
        list for functions that do not have return statements
    """
    if _has_return_values[_function_num]:  # Grab list of non-lists
        _shallow_copy.append(_args)
    else:  # Grab the first list in the list of arguments
        for arg_list in _args:
            if isinstance(arg_list, list):
                _shallow_copy.append(_args[0])
                break


def get_actual_value(_args):
    """
    Get the actual value that is returned after running the function and passing
    in the correct arguments

    :param _args: The arguments to be passed into the function
    :return: The actual return value that is returned after running the function
        with the arguments given
    """
    # Functions with no parameters
    if len(args) == 1 and isinstance(args[0], str) and args[0] == "":
        _actual_value = function_obj()
    # Functions with parameters
    else:
        # Remove any empty strings, which come from lists with only one element
        for arg in args:
            if isinstance(arg, list) and len(arg) == 2 and \
                    isinstance(arg[1], str) and arg[1] == "":
                arg.pop(1)
        # Run the function with the arguments; * expands into args
        _actual_value = function_obj(*args)

    return _actual_value


def convert_actual_value_to_correct_data_type(_actual_value):
    """
    Convert the actual return value to the correct data type

    :param _actual_value: The actual return value to be converted
    :return: The converted actual return value
    """
    if isinstance(_actual_value, str):
        _actual_value = _actual_value.lower()
        try:
            _actual_value = ast.literal_eval(_actual_value)
        except ValueError:
            corrected_str = "\'" + _actual_value + "\'"
            _actual_value = ast.literal_eval(corrected_str)

    return _actual_value


def _get_actual_value_for_functions_without_return(
        _has_return_values, _problem_number, _shallow_copy_problem_set, _unit_test_number,
        _actual_result):
    """
    Get the actual return value for functions that do not have a return
    statement

    :param _has_return_values: The boolean list that keeps track of which
        functions do not have return statements
    :param _problem_number: The problem number being looked at
    :param _shallow_copy_problem_set: The 2D list of all problem numbers and
        their unit test final argument values for functions that do not have a
        return statement
    :param _unit_test_number: The current unit test ordinal
    :param _actual_result: The actual return value after running a function
    :return: The actual return value, pulled from the shallow copy lists for
        functions that do not have return statements, or the same value that
        was passed for functions that do have return statements
    """
    # Compare expected input and input state instead
    if not has_return_values[problem_number]:
        _actual_result = shallow_copy_problem_set[problem_number][_unit_test_number]

    return _actual_result


def reformat_str_2d_list_to_2d(nested_list):
    """
    Reformat a string 2D list to be visualized across multiple lines instead
    of being in a single line

    :param nested_list: The 2D list to reformat
    :return: The reformatted 2D list, which now appears across multiple lines,
        forming a box / rectangular shape
    """
    nested_list_str = str(nested_list)
    nested_list_str = nested_list_str.replace("],", "],\n")

    return nested_list_str


def print_test_pass(_unit_test_number, _function_name_sans_foo, _expected_result,
                    _actual_result, _points_per_problem, _points_per_unit_test):
    """
    Print the results when a test passes

    :param _unit_test_number: The current test number
    :param _function_name_sans_foo: The name of the function being tested,
        without 'foo' in the name
    :param _expected_result: The expected result based off the unit test files
    :param _actual_result: The actual return value, based on what is returned
        when running the function with the unit test arguments
    :param _points_per_problem: The points given per problem
    :param _points_per_unit_test: The points given per unit test
    :return: The updated points per problem value
    """
    # Reformat 2D lists to have a box shape instead of appearing all on one line
    if is_2d_list(_expected_result):
        print("Unit test #", _unit_test_number, " for ", _function_name_sans_foo,
              " function:\n", f"{BColors.OK_GREEN}Passed!{BColors.END_C}",
              "\nExpected:")
        _expected_result_2d_str = reformat_str_2d_list_to_2d(_expected_result)
        print(_expected_result_2d_str)
        print("Found:")
        _actual_result_2d_str = reformat_str_2d_list_to_2d(_actual_result)
        print(_actual_result_2d_str)
    else:
        print("Unit test #", _unit_test_number, " for ", _function_name_sans_foo,
              " function:\n", f"{BColors.OK_GREEN}Passed!{BColors.END_C}",
              " Expected: ", _expected_result,
              ", Found: ", _actual_result, sep='')

    _points_per_problem += _points_per_unit_test

    return _points_per_problem


def print_test_fail(_unit_test_number, _function_name_sans_foo, _expected_result,
                    _actual_result, _score, _points_per_unit_test):
    """
    Print the results when a test fails.

    :param _unit_test_number: The current test number
    :param _function_name_sans_foo: The name of the function being tested,
        without 'foo' in the name
    :param _expected_result: The expected result based off the unit test files
    :param _actual_result: The actual return value, based on what is returned
        when running the function with the unit test arguments
    :param _score: The score of the assignment
    :param _points_per_unit_test: The points per each unit test
    :return: The updated score value
    """
    # Reformat 2D lists to have a box shape instead of appearing all on one line
    if is_2d_list(_expected_result):
        print("Unit test #", _unit_test_number, " for ", _function_name_sans_foo,
              " function:\n", f"{BColors.FAIL}Fail!{BColors.END_C}",
              "\nExpected:")
        _expected_result_2d_str = reformat_str_2d_list_to_2d(_expected_result)
        print(_expected_result_2d_str)
        print("Found:")
        _actual_result_2d_str = reformat_str_2d_list_to_2d(_actual_result)
        print(_actual_result_2d_str)
    else:
        print("Unit test #", _unit_test_number, " for ", _function_name_sans_foo,
              " function:\n", f"{BColors.FAIL}Fail!{BColors.END_C}",
              " Expected: ", _expected_result, ", Found: ", _actual_result,
              sep='')

    _score -= _points_per_unit_test

    return _score


def print_unit_test_results(
        _total_unit_tests, _points_per_unit_test, _points_per_problem,
        _function_name_sans_foo, _expected_return_values, _actual_return_values,
        _problem_number, _has_return_values, _shallow_copy_problem_set,
        _score, _max_score_per_function):
    """
    Print the unit tests results, whether each test passed or failed

    :param _total_unit_tests: The total number of unit tests
    :param _points_per_unit_test: The total points per unit test
    :param _points_per_problem: The number of points per problem
    :param _function_name_sans_foo: The name of the function, excluding 'foo'
    :param _expected_return_values: The list of expected return values for the
        unit tests
    :param _actual_return_values: The list of actual return values when running
        the functions using arguments from the unit tests
    :param _problem_number: The problem number being looked at
    :param _has_return_values: The boolean list that keeps track of which
        functions do not have return statements
    :param _shallow_copy_problem_set: The list of lists keeping track of the
        argument data for functions that do not have return statements
    :param _score: The score of the assignment
    :param _max_score_per_function: The maximum score per function
    :return: The final score after running all of the unit tests
    """
    # Print the name of the function being tested
    print("#", _problem_number, f"{BColors.WARNING} {_function_name_sans_foo}{BColors.END_C}",
          " tests:", sep='')

    # Run each unit test and display the results
    for unit_test_number in range(0, _total_unit_tests):
        # Get expected result and actual result
        expected_result = _expected_return_values[_problem_number][unit_test_number]
        actual_result = _actual_return_values[_problem_number][unit_test_number]

        # Update the actual result if the problem does not have a return value
        actual_result = _get_actual_value_for_functions_without_return(
            _has_return_values, _problem_number, _shallow_copy_problem_set, unit_test_number,
            actual_result)

        # Fix data structure types for functions that have two or more return values
        if type(actual_result) is not type(expected_result):
            actual_result = list(actual_result)

        # Print test results
        if actual_result == expected_result:
            _points_per_problem = print_test_pass(
                unit_test_number, _function_name_sans_foo, expected_result, actual_result,
                _points_per_problem, _points_per_unit_test)
        else:
            _score = print_test_fail(
                unit_test_number, _function_name_sans_foo, expected_result, actual_result,
                _score, _points_per_unit_test)

    # Print the overall score for the problem unit test set
    print("\n#", _problem_number, f"{BColors.OK_BLUE} score: {BColors.END_C}",
          round(_points_per_problem, 2), "/", round(_max_score_per_function, 2),
          "\n", sep='', end='\n')

    return _score


# Get files in current directory "C:\\Users\\Teacher Loaner\\PycharmProjects\\Checker"
mypath = os.getcwd()
only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Get correct unit test files
assignment_name = input("Enter the assignment being tested:\n"
                        "(p# for project, h# for homework) - Eg. p2\n")
UNIT_TEST_TEXT_FILE_ROOT += assignment_name.lower() + "_"

# Find correct file (assuming only this file and one other .py file are in the directory),
# along with the unit test files and any other directories, such as venv
py_file_name = get_py_file_by_name(only_files, module_name)

# Read file and grab correct function names with the specified token
lines = get_lines_from_py_file(py_file_name)

# Get the function names in a list
function_list = get_function_list(lines)

# Test functions using unit tests that are read from the unit test text files
# Save results of expected return values vs actual result values found when
# running functions
# debug: print(function_list)
index = 0
has_return_values = []

# Holds the final values of the inputs after the function is run
shallow_copy_problem_set = []

# Holds the list of expected and actual return values for the different unit tests
expected_return_values = []
actual_return_values = []

# Go through all functions in program that start with FUNCTION_NAME_IDENTIFIER
for function_num in range(0, len(function_list)):
    # Keeps track of whether the function has a return
    no_return = False

    # Get the function name and unit test file name
    function_name_instance = function_list[function_num]
    unit_test_text_file_name = UNIT_TEST_TEXT_FILE_ROOT + str(index) + ".txt"

    # list_args is a 2D list, expected_value_list is a 1D list
    list_args, expected_value_list = get_unit_tests(unit_test_text_file_name)
    expected_return_values.append(expected_value_list)
    function_obj = getattr(IMPORT_NAME, function_name_instance)

    # If function does not have a return statement, make copy of original
    # arguments and compare to arguments after the function has been run
    update_has_return_values_list(function_obj, has_return_values)

    # Convert arguments to their proper data type
    # Convert list arguments
    convert_list_arguments(list_args)

    # Convert expected values
    convert_expected_value_list(expected_value_list)

    # Run all unit tests
    actual_value_list = []
    shallow_copy = []
    original_input_values = []

    # Get return values from running functions using arguments from unit test files
    for args in list_args:
        update_shallow_copy_list(function_num, has_return_values, shallow_copy, args)

        # Get the value returned from running the function
        actual_value = get_actual_value(args)
        actual_value = round_any(actual_value)  # Round to 2 decimal places, if it is a decimal

        # Convert actual value to correct data type
        actual_value = convert_actual_value_to_correct_data_type(actual_value)
        actual_value_list.append(actual_value)

    actual_return_values.append(actual_value_list)
    shallow_copy_problem_set.append(shallow_copy)

    index += 1

# Check expected unit test results verses actual unit test results
score = 100
max_score_per_function = 100 / len(expected_return_values)

# Missing function
missing_problems_margin = 0
if len(expected_return_values) != len(actual_return_values):
    score -= max_score_per_function
    missing_problems_margin += len(expected_return_values) - len(actual_return_values)

# Score each problem based on unit tests
for problem_number in range(0, len(expected_return_values) - missing_problems_margin):
    total_unit_tests = len(expected_return_values[problem_number])
    points_per_unit_test = max_score_per_function / total_unit_tests
    points_per_problem = 0
    function_name_sans_foo = function_list[problem_number].replace("foo_", "")

    # Print results of unit test
    score = print_unit_test_results(
        total_unit_tests, points_per_unit_test, points_per_problem, function_name_sans_foo,
        expected_return_values, actual_return_values, problem_number,
        has_return_values, shallow_copy_problem_set, score, max_score_per_function)

# Print final score results
student_name = py_file_name.split(".")[0]
score = round(score, 2)
print(student_name, f"{BColors.OK_BLUE} score: {BColors.END_C}", score, sep='')
