import json
import os

from utils import flatten_nested_dict, remove_desc_funcs, debug, openrouter_request

class ProjectGenerator:
    def __init__(self, request):
        self.request = request
        self.style = {
            'python': {
                'arch': "",#"Classes and methods should all be kept relatively short - below 200 lines for classes and 30 lines for methods.
                        #""",
                'general': """When behavior is complicated or unclear, comment it thoroughly.
                            Make sure that every part of methods (arguments, return, internal variables) are type-annotated.
                            Ensure that class variables are only created in __init__, and use type annotations. Methods or variables only accessed from within the class should start with "__".
                            """,
            }
        }
        self.project_prompt = None
        self.project_scale = None
        self.project_tree_string_initial = None
        self.project_tree_json_initial = None
        self.project_tree_string = None
        self.project_tree_json = None

        self.lang = None

        self.directory = "generated_code/"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # TODO
        self.callable_tools = ['validate', 'find_example', 'get_docs', 'create_test']

    def generate_project(self, prompt, lang='python'):
        self.project_prompt = prompt
        self.lang = lang
        self.project_scale = self.request(
            f"""For the following {self.lang} project, estimate the scale of the project. 
            E.g. if the project is 'fibonnaci calculator', the scale would be something like 'Single function'.
            If the project is 'snake game' the scale might be 'A class or two with a handful of methods'.
            If the project is 'social media website' the scale would be 'Many classes.'
            Please be very succinct - no more than about 10-20 words.
            {self.style[self.lang]['arch']}

            Project: {self.project_prompt}""")
        debug("Project scale:", self.project_scale)
        
        self.project_tree_string_initial = self.request(
            f"""For the following {self.lang} project, with the given scale, generate a high-level tree for the project, in JSON format.
            It should start with main. Assume that each entry will be a class. Don't worry about getting every required class, just the important ones.
            Each entry/class should be the key in an object, with the value being an object with all the entry's dependencies. No dependencies = empty object.
            Example: {{"main": {{"class1": {{"class2": {{}}}}, "class3": {{}}}}}}
            Please return only valid JSON like the example above, no other text.
            
            {self.style[self.lang]['arch']}
                    
            Project: {self.project_prompt}
            Scale: {self.project_scale}""", type='json')
        try:
            debug("Initial project tree:", self.project_tree_string_initial)
            self.project_tree_json_initial = json.loads(self.project_tree_string_initial)
        except:
            raise Exception("Initial project tree is malformed json")
        
        self.project_tree_string = self.request(
            f"""Flesh out the following high-level project tree according to the project description.
            Each class should have "desc" and "functions". 
            "desc" should be a succinct description (<50 words) of what the class does.
            "funcs" should be an object where keys are function names and values are very short (<15 words) descriptions of what the function does.
            Don't worry about getting every required function, just the important ones.
            Classes will also have their dependencies as keys (directly - like {{"Class1": "Class2": {{..}}}}), and the dependencies' properties (desc, funcs, and any dependencies) as values.
            You can also add new classes if absolutely needed.
            Please return only valid JSON, no other text.

            {self.style[self.lang]['arch']}
            
            Project descriptioon: {self.project_prompt}
            High-level tree: {self.project_tree_string_initial}""", type='json')
        
        try:
            debug("Final project tree:", self.project_tree_string)
            self.project_tree_json = json.loads(self.project_tree_string)
        except:
            raise Exception("Final project tree is malformed json")
        
        all_classes = flatten_nested_dict(self.project_tree_json)
        debug("All classes:", all_classes)
        class_code = remove_desc_funcs(all_classes)
        debug("Class code:", class_code)
        for classname in all_classes:
            if classname == "dependencies":
                debug("skipped dependencies classname")
                continue # TODO fix this bodge
            try:
                class_code[classname] = self.generate_class(name=classname, desc=all_classes[classname]['desc'], funcs=all_classes[classname]['funcs'])
            except:
                raise Exception(f"Error generating class {classname} - no desc and/or funcs found")
            with open(f"{self.directory}{classname}.py", "w") as f:
                f.write(class_code[classname])

        # for classname in class_code:
        #     with open(f"{self.directory}{classname}.py", "w") as f:
        #         f.write(class_code[classname])
        # TODO bring back saving at one time once more mature
        # TODO {'filename': 'description} main is always guaranteed and is generated last
        # TODO dependency tree, build up from the bottom

    def generate_class(self, name, desc, funcs):
        generated_funcs = {}
        init = self.request(
            f"""Based on the following {self.lang} class description and function list, generate the class definition and constructor.
            Make sure to include in the constructor any class variables that are needed.
            Don't worry about imports.
            {self.style[self.lang]['general']}
            
            Please return only valid {self.lang} code, no other text.
            
            Class name: {name}
            Class description: {desc}
            Methods: {funcs}
            """)
        for func in funcs:
            try:
                generated_funcs[func] = self.generate_method(name=func, desc=funcs[func], class_desc=desc, class_init=init)
            except:
                raise Exception(f"Error generating method {func} - no desc found")
            
        code = init
        for f in generated_funcs:
            code += f

        code = self.request(
            f"""Generate the required imports for the following {self.lang} class.
            Do not copy any of the provided code - only give me the imports.

            Please return only valid {self.lang} code, no other text.

            Code: {code}
            """) + code

        debug(f"Generated class {name}:", code)
        return code


    def generate_method(self, name, desc, class_desc, class_init):
        func = self.request(
            f"""Based on the following {self.lang} method description, class description, and class definition+constructor, generate the method definition.
            Don't worry about imports.
            {self.style[self.lang]['general']}

            Please return only valid {self.lang} code, no other text.

            Method name: {name}
            Method description: {desc}
            Class description: {class_desc}
            Class definition+constructor: {class_init}
            """)
        debug(f"Generated method {name}:", func)
        return func
    
g = ProjectGenerator(request=openrouter_request)
g.generate_project("Sieve of Erastothenes")

#print(openrouter_request("hi"))