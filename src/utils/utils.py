# Python Imports
from os import listdir
from os.path import isfile, join

# Obtain the contents of a file as a single string
def get_file_contents(filename):
    contents = None
    with open(filename, "r") as f:
        contents = f.read()
    return contents

# Obtain a list of the relatve path of every js file contained in the given directory
def get_all_js_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    directories = [d for d in listdir(directory) if not isfile(join(directory, d))]

    js_files = []
    for f in files:
        if f[-3:] == ".js":
            js_files.append(join(directory, f))

    for d in directories:
        js_files.extend(get_all_js_files(join(directory, d)))

    return js_files

def remove_comments_and_strings(contents):

    # Handle edge case
    contents = contents + "\n"

    # Identify comments and strings and record their locations
    in_single_quotes = False
    in_double_quotes = False
    in_single_comment = False
    in_multi_comment = False
    things_to_remove = []
    is_quote = []
    for i in range(1, len(contents)):
        if contents[i-1:i+1] == "//":
            if not in_single_quotes and not in_double_quotes and not in_multi_comment and not in_single_comment:
                in_single_comment = True
                things_to_remove.append([i-1,-1])
        elif contents[i] == "\n":
            if in_single_comment:
                in_single_comment = False
                things_to_remove[-1][-1] = i - 1
        elif contents[i-1:i+1] == "/*":
            if not in_single_quotes and not in_double_quotes and not in_single_comment and not in_multi_comment:
                in_multi_comment = True
                things_to_remove.append([i-1,-1])
        elif contents[i-1:i+1] == "*/":
            if in_multi_comment:
                in_multi_comment = False
                things_to_remove[-1][-1] = i
        elif contents[i] == "\"" and contents[i-1] != "\\":
            if in_double_quotes:
                in_double_quotes = False
                things_to_remove[-1][-1] = i
            elif not in_single_quotes and not in_single_comment and not in_multi_comment:
                in_double_quotes = True
                is_quote.append(len(things_to_remove))
                things_to_remove.append([i,-1])
        elif contents[i] == "\'" and contents[i-1] != "\\":
            if in_single_quotes:
                in_single_quotes = False
                things_to_remove[-1][-1] = i
            elif not in_double_quotes and not in_multi_comment and not in_single_comment:
                in_single_quotes = True
                is_quote.append(len(things_to_remove))
                things_to_remove.append([i,-1])

    # Remove identified comments and strings in reverse order, adding quotes for... quotes
    for i in range(len(things_to_remove) -1, -1, -1):
        start_index, end_index = things_to_remove[i]
        if i in is_quote:
            # print("Removing Quote: " + contents[start_index:end_index+1])
            contents = contents[:start_index] +"\"\"" + contents[end_index + 1:]
        else:
            # print("Removing Comment: " + contents[start_index:end_index+1])
            contents = contents[:start_index] + contents[end_index + 1:]

    return contents

def get_loop_bodies(contents):

    # Get the relevant strings
    for_loops = []
    while_loops = []
    to_cut_out = []

    # handle contents that start with loops
    contents = "      " + contents

    i = 7
    while (i < len(contents)):
        if contents[i-4:i] == "for(" or contents[i-5:i] == "for (" or contents[i-7:i] == "while (" or contents[i-6:i] == "while(":
            
            # This is the start of a loop
            # Find where conditions end
            depth = 1
            end_of_conditions = -1
            for j in range(i, len(contents)):
                if contents[j] == "(":
                    depth += 1
                elif contents[j] == ")":
                    depth -= 1
                    if depth == 0:
                        end_of_conditions = j
                        break
            
            # Find where loop body ends
            depth = 0
            end_of_body = -1
            for j in range(end_of_conditions, len(contents)):
                if contents[j] == "{":
                    depth += 1
                elif contents[j] == "}":
                    depth -= 1
                    if depth == 0:
                        end_of_body = j
                        break

            # Cut out the loop body
            body = contents[end_of_conditions+1 : end_of_body].strip()
            body = body[1:].strip()

            print("-----------------------")
            print(body)
            print("-----------------------")

            # Handle loop type specifics
            if contents[i-4:i] == "for(":
                for_loops.append(body)
                to_cut_out.append((i-4,end_of_body))
            elif contents[i-5:i] == "for (":
                for_loops.append(body)
                to_cut_out.append((i-5,end_of_body))
            elif contents[i-7:i] == "while (":
                while_loops.append(body)
                to_cut_out.append((i-7,end_of_body))
            elif contents[i-6:i] == "while(":
                while_loops.append(body)
                to_cut_out.append((i-6,end_of_body))

            # Adjust outer loop
            i = end_of_body
        
        i += 1
    # Cut out loop bodies
    to_cut_out.reverse()
    for start_index, end_index in to_cut_out:
        contents = contents[:start_index] + ";" + contents[end_index + 1:]

    return (contents, for_loops, while_loops)

def count_expects(contents, for_iteration_guess, while_iteration_guess):

    # Get loop bodies and cut them out
    contents, for_loops, while_loops = get_loop_bodies(contents)

    # Count expects that do not occur in loops
    expect_count = len(contents.split("expect(")) - 1

    # Add counts that do occur in loops
    for body in for_loops:
        expect_count += for_iteration_guess * count_expects(body, for_iteration_guess, while_iteration_guess)
    for body in while_loops:
        expect_count += while_iteration_guess * count_expects(body, for_iteration_guess, while_iteration_guess)
    
    return expect_count

def get_expect_count(file_path, for_iteration_guess, while_iteration_guess):
    
    # Load file
    contents = get_file_contents(file_path)

    # Preprocess contents
    contents = remove_comments_and_strings(contents)
    contents = " ".join(contents.split())

    # count expects
    return count_expects(contents, for_iteration_guess, while_iteration_guess)

if __name__ == "__main__":
    print(get_expect_count("../test_test.js", 5, 5))