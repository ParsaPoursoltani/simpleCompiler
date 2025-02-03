class SimpleLangInterpreter:
    def __init__(self):
        # Initialize a dictionary to store variables and their values
        self.variables = {}

    def parse_line(self, line):
        # Remove leading and trailing whitespace
        line = line.strip()
        # Check the type of statement and call the appropriate handler
        if line.startswith('int ') or line.startswith('str '):
            self._parse_declaration(line)
        elif line.startswith('print '):
            self._parse_print(line)
        else:
            self._parse_assignment(line)

    def _parse_declaration(self, line):
        # Split the line into tokens
        tokens = line.split(' ')
        var_type = tokens[0]
        var_name = tokens[1]
        # Initialize the variable with a default value based on its type
        self.variables[var_name] = 0 if var_type == 'int' else ""
        
        # If there's an assignment, parse it
        if len(tokens) > 3 and tokens[2] == '=':
            value = ' '.join(tokens[3:])
            self._parse_assignment(f"{var_name} = {value}")

    def _parse_assignment(self, line):
        # Split the line into variable name and expression
        var_name, expr = line.split('=')
        var_name = var_name.strip()
        expr = expr.strip()

        # Check if the variable has been declared
        if var_name not in self.variables:
            print(f"Error: Variable '{var_name}' not declared.")
            return

        # Evaluate the expression and update the variable's value
        result = self._evaluate_expression(expr)
        self.variables[var_name] = result

    def _parse_print(self, line):
        # Extract the expression to be printed
        expr = line[6:].strip()
        # Evaluate the expression and print the result
        result = self._evaluate_expression(expr)
        print(result)

    def _evaluate_expression(self, expr):
        try:
            # Evaluate numeric expressions using eval
            result = eval(expr, {}, self.variables)
            return result
        except NameError as e:
            # Handle variables by looking them up in the dictionary
            var_name = expr
            return self.variables.get(var_name, f"Error: Undefined variable '{var_name}'")
        except:
            # Handle string literals
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
            elif expr.startswith("'") and expr.endswith("'"):
                return expr[1:-1]
            else:
                return f"Error: Invalid expression '{expr}'"

    def run(self, code):
        # Split the input code into lines and parse each line
        lines = code.strip().split('\n')
        for line in lines:
            self.parse_line(line)

def run_from_file():
    # Prompt the user to enter the filename
    filename = input("Enter the name of the file to execute: ").strip()
    try:
        with open(filename, 'r') as file:
            code = file.read()

        interpreter = SimpleLangInterpreter()
        interpreter.run(code)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

# Run the interpreter with input from the console
run_from_file()