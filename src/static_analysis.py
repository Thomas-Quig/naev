# Python Imports

# naev Imports
from utils.static import *
from utils.general import *

# 3rd Party Imports
import numpy as np

# Assumes that content has already been preprocessed
def get_exported_variables(contents):
    exported_variables = []

    # Get the relevant strings
    variable_export_strings = contents.split("export let")[1:] + contents.split("export var")[1:]
    for i in range(0, len(variable_export_strings)):
        variable_export_strings[i] = variable_export_strings[i].split(";")[0]

    # Parse them dang strings
    for export_string in variable_export_strings:
        variables = export_string.split(",")
        for variable in variables:
            exported_variables.append(variable.split("=")[0].strip())

    return exported_variables

# Assumes that content has already been preprocessed
# Returns dictionary of functions with the structure {function_name : [param1, param2, ..., paramn]}
def get_exported_functions(contents):
    exported_functions = {}
    
    # Get the relevant strings
    function_export_strings = contents.split("export function")[1:]
    for i in range(0, len(function_export_strings)):
        cur_string = function_export_strings[i]
        depth = 1
        for j in range(cur_string.find("(") + 1, len(cur_string)):
            if cur_string[j] == "(":
                depth += 1
            elif cur_string[j] == ")":
                depth -= 1
                if depth == 0:
                    function_export_strings[i] = cur_string[:j]
                    break

    # Parse them dang strings
    for export_string in function_export_strings:
        function_name, params_string = export_string.split("(", 1)
        function_name = function_name.strip()
        exported_functions[function_name] = []

        params = params_string.split(",")
        for param in params:
            exported_functions[function_name].append(param.split("=")[0].strip())
    
    return exported_functions

# Assumes that content has already been preprocessed
# Assumes no class nesting
# Assumes maximum semicolon usage
# Assumes upfront declarations are one per line
# Assumes no generator methods
# Assumes no async
# Assumes no function declaration nesting
# returns dictionary of classes with the structure {class_name : ([property1, property2, ..., propertyn], {function_name : [param1, param2, ..., paramn]})}
def get_exported_classes(contents):
    exported_classes = {}

    # Get the relevant strings
    class_export_strings = contents.split("export class")[1:]
    for i in range(0, len(class_export_strings)):
        cur_string = class_export_strings[i]
        depth = 1
        for j in range(cur_string.find("{") + 1, len(cur_string)):
            if cur_string[j] == "{":
                depth += 1
            elif cur_string[j] == "}":
                depth -= 1
                if depth == 0:
                    class_export_strings[i] = cur_string[:j]
                    break

    # Parse them dang strings
    for class_string in class_export_strings:
        class_name, class_body = class_string.split("{", 1)
        class_name = class_name.strip()
        class_body = class_body.strip()
        exported_classes[class_name] = ([],{})

        # Extract the static things and remove them from the class body
        static_strings = class_body.split("static ")[1:]
        for static_string in static_strings:

            # Remove prefixed get or set if it is a getter or a setter
            cur_string = static_string
            add_to_end_index = 0
            if cur_string[:4] == "get " or cur_string[:4] == "set ":
                cur_string = cur_string[4:]
                add_to_end_index = 4

            end_index = -1
            # Decide if this is a static method or property
            # It is a method if the first non alphanumeric character that is not '_' we encounter is a '(', property otherwise
            for i in range(0, len(cur_string)):
                if not (cur_string[i].isalnum() or cur_string[i] == "_"):
                    if cur_string[i] == "(":    
                        
                        # This is a static method
                        method_name = "static " + cur_string[:i]
                        exported_classes[class_name][1][method_name] = []

                        # Extract the params
                        params = []
                        depth = 1
                        for j in range(i+1, len(cur_string)):
                            if cur_string[j] == "(":
                                depth += 1
                            elif cur_string[j] == ")":
                                depth -= 1
                                if depth == 0:
                                    params = cur_string[i+1:j].split(",")
                                    break
                        for param in params:
                            param_name = param.split("=")[0].strip()
                            if param_name != "":
                                exported_classes[class_name][1][method_name].append(param_name)

                        # Determine where the method ends
                        depth = 1
                        for j in range(cur_string.find("{") + 1, len(cur_string)):
                            if cur_string[j] == "{":
                                depth += 1
                            elif cur_string[j] == "}":
                                depth -= 1
                                if depth == 0:
                                    end_index = j
                                    break
                    else:   
                        
                        # This is a static property
                        property_name = "static " + cur_string[:i]
                        exported_classes[class_name][0].append(property_name)
                        end_index = cur_string.find(";")
                    break
            
            # Remove this static thing from the class body
            class_body = class_body.replace("static " + static_string[:end_index + add_to_end_index + 1], "", 1)

        # Christ that was a nightmare
        # Now we detect all the upfront field declarations, which occur before ANY function definition
        statements = class_body.split(";")
        num_statements_to_remove = 0
        for statement in statements:
            statement = statement.strip() + ";"
            if len(statement) == 1:
                num_statements_to_remove += 1
                continue
            
            # Check if it is a getter or a setter method
            if statement[:4] == "get " or statement[:4] == "set ":
                break

            # Check if this is a method
            is_method = False
            for i in range(0, len(statement)):
                if not(statement[i].isalnum() or statement[i] == "_" or statement[i] == "#"):   # '#' is only included here because private fields are allowed to be prefixed with it
                    if statement[i] == "(":
                        # This is a method
                        is_method = True
                    break
            if is_method:
                break

            # Check if we should ignore this field
            if statement[0] == "#" or statement[0] == "_":
                num_statements_to_remove += 1
                continue

            # If we are here, we should add this field
            num_statements_to_remove += 1
            for i in range(0, len(statement)):
                if not(statement[i].isalnum() or statement[i] == "_"):
                    exported_classes[class_name][0].append(statement[:i])
                    break
        
        # Now we remove all the upfront statements
        if num_statements_to_remove == 1:
            class_body = class_body.replace(statements[0] + ";", "")
        else:
            class_body = class_body.replace(";".join(statements[:num_statements_to_remove]), "")

        # Now we do the method crawl
        i = 0
        while(i < len(class_body)):
            if class_body[i].isalnum() or class_body[i] == "_":
                
                # This is the start of a method name
                # Obtain the name
                params_start = -1
                for j in range(i, len(class_body)):
                    if class_body[j] == "(":
                        params_start = j
                        break
                method_name = class_body[i:params_start]
                exported_classes[class_name][1][method_name] = []

                # Extract the params
                params = []
                depth = 1
                params_end = -1
                for j in range(params_start+1, len(class_body)):
                    if class_body[j] == "(":
                        depth += 1
                    elif class_body[j] == ")":
                        depth -= 1
                        if depth == 0:
                            params = class_body[params_start+1:j].split(",")
                            params_end = j
                            break
                for param in params:
                    param_name = param.split("=")[0].strip()
                    if param_name != "":
                        exported_classes[class_name][1][method_name].append(param_name)

                # Obtain the method body
                depth = 0
                body_end = -1
                for j in range(params_end + 1, len(class_body)):
                    if class_body[j] == "{":
                        depth += 1
                    elif class_body[j] == "}":
                        depth -= 1
                        if depth == 0:
                            body_end = j
                            break
                method_body = class_body[params_end + 1 : body_end].strip()

                # Get any created fields from the method body
                field_strings = method_body.split("this.")[1:]
                for field_string in field_strings:
                    for j in range(0, len(field_string)):
                        if not (field_string[j].isalnum() or field_string[j] == "_"):
                            if field_string[j] != "(":
                                exported_classes[class_name][0].append(field_string[:j])
                            break

                # Skip over this method as i iterates
                i = body_end

            i += 1

        # Remove duplicates
        exported_classes[class_name] = (sorted(list(set(exported_classes[class_name][0]))), exported_classes[class_name][1])

    # This sucks
    return exported_classes

# Returns the same as compare, but is limited to comparing one file across the versions
def compare_files(lower_version_contents, higher_version_contents):

    # Do some preprocessing
    lower_version_contents = remove_comments_and_strings(lower_version_contents)
    lower_version_contents = " ".join(lower_version_contents.split())
    higher_version_contents = remove_comments_and_strings(higher_version_contents)
    higher_version_contents = " ".join(higher_version_contents.split())

    # Compare exported variables
    lower_exported_variables = get_exported_variables(lower_version_contents)
    higher_exported_variables = get_exported_variables(higher_version_contents)
    variable_delta = 0
    variable_ct = len(lower_exported_variables)
    for variable in lower_exported_variables:
        if variable not in higher_exported_variables:
            variable_delta += 1

    # Compare exported functions
    # Note that the param delta excludes parameters of functions that are missing altogether.
    lower_exported_functions = get_exported_functions(lower_version_contents)
    higher_exported_functions = get_exported_functions(higher_version_contents)
    function_delta = 0
    function_ct = len(lower_exported_functions)
    function_param_delta = 0
    function_param_ct = 0
    for function in lower_exported_functions:
        if function not in higher_exported_functions:
            function_delta += 1
        else:
            function_param_ct += len(lower_exported_functions[function])
            for param in lower_exported_functions[function]:
                if param not in higher_exported_functions[function]:
                    function_param_delta += 1

    # Compare exported classes
    lower_exported_classes = get_exported_classes(lower_version_contents)
    higher_exported_classes = get_exported_classes(higher_version_contents)
    class_delta = 0
    class_ct = len(lower_exported_classes)
    class_function_delta = 0
    class_function_ct = 0
    class_function_param_delta = 0
    class_function_param_ct = 0
    class_property_delta = 0
    class_property_ct = 0
    for class_name in lower_exported_classes:
        if class_name not in higher_exported_classes:
            class_delta += 1
        else:
            class_property_ct += len(lower_exported_classes[class_name][0])
            for class_property in lower_exported_classes[class_name][0]:
                if class_property not in higher_exported_classes[class_name][0]:
                    class_property_delta += 1

            class_function_ct += len(lower_exported_classes[class_name][1])
            for function in lower_exported_classes[class_name][1]:
                if function not in higher_exported_classes[class_name][1]:
                    class_function_delta += 1
                else:
                    class_function_param_ct += len(lower_exported_classes[class_name][1][function])
                    for param in lower_exported_classes[class_name][1][function]:
                        if param not in higher_exported_classes[class_name][1][function]:
                            class_function_param_delta += 1

    return [[class_ct, class_delta], 
            [class_property_ct, class_property_delta], 
            [class_function_ct, class_function_delta], 
            [class_function_param_ct, class_function_param_delta], 
            [variable_ct, variable_delta], 
            [function_ct, function_delta], 
            [function_param_ct, function_param_delta]]

# This function analyzes the code of two versions of the same package to attempt to determine
# if they are functionally equivalent. It analyzes them according to this rubric:
# - We only check something if it is exported when it is initially defined
#     - We check that classes exported in the lower version are also exported in the higher version
#     - properties
#         - We ignore properties whose name is prefixed with '_' or '#'
#         - We check that all non-static properties declared at the top of the class in the lower version are still present in the higher version
#         - We check that all static properties declared at the top of the class in the lower version are still present in the higher version
#         - We check that any property of the form 'this.*' on the left side of an assignment in any function in the lower version is still present in the higher version
#     - functions
#         - we ignore functions whose name is prefixed with '_' or '#'
#         - We check that all required parameters are the same across both versions
# - Variables
#     - We check that variables exported in the lower version are also exported in the higher version
# - Functions
#     - We check that functions exported in the lower version are also exorted in the higher version
#     - We check that all required parameters are the same across both versions.
# @param lower_version_directory The root directory of the lower package version
# @param higher_version_directory The root directory of the higher package version
# @return This function returns a tuple of the form [[A, a], [B, b], [C, c], [D, d] [E, e], [F, f], [G, g]] where each letter represents a type of thing that was checked.
# The upper case letters represent the total number of that type of thing that were analyzed, while the lowercase letters represent the number of that type 
# of thing that were detected as different. A = clsses, B = class properties, C = class functions, D = class function parameters, E = variables, F = functions, G = function parameters
# ASSUMPTIONS: The maximum number of semicolons are used, the export statement is always prefixed to the definition of the thing being exported, exports are not renamed
# Assumes no generator methods
# Assumes no async
# Assumes no function declaration nesting
def compare(lower_version_directory, higher_version_directory):
    
    # Load lower version for parsing
    lower_version_files = {}
    for filepath in get_all_js_files(lower_version_directory):
        lower_version_files[filepath.split("/")[-1]] = (get_file_contents(filepath))

    # Load higher version for parsing
    higher_version_files = {}
    for filepath in get_all_js_files(higher_version_directory):
        higher_version_files[filepath.split("/")[-1]] = (get_file_contents(filepath))
    
    # Sum the deltas of every file
    deltas = np.zeros((7,2), dtype=np.int64)
    for filename in lower_version_files:
        if filename in higher_version_files:
            deltas += compare_files(lower_version_files[filename], higher_version_files[filename])
        else:
            deltas += compare_files(lower_version_files[filename], "")

    return deltas.tolist()

def get_equivalence_score(lower_version_directory, higher_version_directory):

    # Get deltas
    deltas = compare(lower_version_directory, higher_version_directory)
    class_ct, class_delta = deltas[0]
    class_property_ct, class_property_delta = deltas[1]
    class_function_ct, class_function_delta = deltas[2]
    class_function_param_ct, class_function_param_delta = deltas[3]
    variable_ct, variable_delta = deltas[4]
    function_ct, function_delta = deltas[5]
    function_param_ct, function_param_delta = deltas[6]

    # Compute score
    equivalence_score = 1.0
    if class_delta > 0:
        equivalence_score -= 0.1
        equivalence_score -= (class_delta / class_ct) * 0.5
    if class_property_delta > 0:
        equivalence_score -= 0.05
        equivalence_score -= (class_property_delta / class_property_ct) * 0.5
    if class_function_delta > 0:
        equivalence_score -= 0.05
        equivalence_score -= (class_property_delta / class_property_ct) * 0.5
    if class_function_param_delta > 0:
        equivalence_score -= (class_function_param_delta / class_function_param_ct) * 0.5
    if variable_delta > 0:
        equivalence_score -= (variable_delta / variable_ct) * 0.3
    if function_delta > 0:
        equivalence_score -= 0.2
        equivalence_score -= (function_delta / function_ct) * 0.3
    if function_param_delta > 0:
        equivalence_score -= (function_param_delta / function_param_ct) * 0.3

    return equivalence_score

if __name__ == "__main__":
    print(get_equivalence_score("../test_lower_version", "../test_higher_version"))