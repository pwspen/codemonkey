uploaded_files = []

inputs, outputs = classify_input_output(uploaded_files)
example_inputs, inputs_to_convert = classify_input_type(inputs, outputs) 
# Figures out if output(s) has a corresponding input, such that it 
# should be used as a source to generate the conversion.
# Just needs to check the first couple lines of each file to see if the 
# values match up to the provided output (in any way that makes sense).
# If so, it is an example_input

# below generates, saves, then imports func Convert(inputs: list[str]) -> outputs: list[str] where the lists are lines.
# Flags: where to put em?
# ditch comments, remove empty lines, keep example example input (if provided) or ditch, etc.
full_example_present = False
if example_inputs:
    example = example_inputs[0]
    full_example_present = True
else:
    full_example_present = False

Convert = generate_converter(example, outputs) # Convert(inputs: list[str]) -> outputs: list[str]
# Generates and returns code for a function that converts the input to the output, given lists of lines.
# Order in lists is very important - assumed to be sequential.
# Either line by line or file by file.

if full_example_present: # Validation check
    validated = False
    while not validated:
        example_output = Convert(example)
        validated = (example_output in outputs)
        if not validated:
            Convert = improve_converter('converterpath.py', example, outputs)

# Hypervisor that takes input, makes call to split task into bulleted list of tasks / files needed for the project, and makes that many LLM calls.
# First gives difficulty rating, then splits it down into a number of bullet points proportional to its complexity.
# This can be scaled based on a user input parameter, for possibly better results.
# Where possible, functions / converters are validated (validator is generated and run by hypervisor).



# Messaging is wrapped in library that counts tokens spent, informing or even asking for permission to proceed every x (settable) tokens spent.


# Goal is a library that can just take a string of texts, do what it was asked, and print its response. So can be used to make either super simple
# terminal interface or UI with single text box and button.

# More LLM calls, the better. Shorter context length seems to be much better when multiple concept / trains of thought
# are involved - no concept pollution.
# Quickly iterating stuff works the best in many cases, so encourage this.
# User gets a setting - 'notify per x tokens' or 'confirm per x tokens spent'. Reasonable defaults are chosen for both.
# The abpove code would be ran only by a sub-process spunt out from the main one.
# Hypervisor would decide which previously-created output files would be relevant to this file, and inject them in sub-prompt.
# Allow for variability even at lower levels - make process iterative and add correctness checks by other AI, saying the program was written by another AI.
# Above is easy to extend by e.g. running npm start and then taking a screenshot and asking if the screenshot matches the description.
# If not, asking to identify the things that should change, iterate again, then running checker again.
# output does what it is supposed to do. If not, iterate again.

# New libraries/packages are installed whenever they are needed, and user is informed as it happens.
# Terminal access so it can do what it wants, with feedback (error) if present
# Program asks user to do something when it's required (e.g. account creation, bill payment)
# Needs set of styles, and advice for what to do in blanks parts of program - idea generation. e.g. if request is "make a game", specifically prompt ideas, not code immediately.

# Eventually, needs way to seek information (as in google search), download it, and use it in generation.
# Wikipedia, github, stackoverflow, readthedocs, etc

# Re-evaluating code after it's done, with reference to its dependencies, and ask if they are correct or need to be updated.
# This propagates up the program's dependency tree.
# Dependency tree (program structure) can be mutated in re-evaluations.

# Thus avoid long range dependency updates (expensive)
