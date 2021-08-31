LING 473, Project 3 (Karl Haraldsson)
Readme

"fas.py" is a script implements the assigned syllable-breaker FSA. It includes three functions: process_file, process_lines, and create_cat2chars. process_file takes three arguments: (1) the path to the text file category.txt, which relates each character to its category; (2) the path to the text file input.txt, which is the Thai text we will process; and (3) the name of the output file for processed text. It applies the other two functions in order to process the text.

create_cat2chars takes as an input a list of characters with their categories (from category.txt). It outputs a dictionary relating the two.

process_lines takes a string of lines from the input.txt file, the fsa dictionary, and the cat2chars dictionary as arguments. It operationalizes the FSA, looping through each line and character in the file. The logic here is identical to the pseudo code. Unless altered, the loop I created added an extraneous space at the end of each line (in accordance with a syllable-break). This is because the function was moving from state 9 back to state 0. Instead of checking the next character in the FSA, I chose to use a "blunt object," re.replace(), to remove trailing spaces (spaces put between the final Thai character and \n).


You can run fas.py using "python3 fas.py my_category_file my_input_file".

"run.sh" is a bash file to run "fas.py". You can run it by "./run.sh" or "sh run.sh".