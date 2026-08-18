import ast
import sys
from io import StringIO
import builtins
import time
import resource
from contextlib import contextmanager
import threading

class CodeExecutionError(Exception):
    pass

class Sandbox:
    def _init_(self, memory_limit=50*1024*1024, time_limit=2):  # 50MB memory, 2 seconds time limit
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.allowed_modules = {
            'math', 'random', 'datetime', 'collections', 
            'itertools', 'functools', 're'
        }
        # Define safe builtins
        self.safe_builtins = {
            name: getattr(builtins, name)
            for name in ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytes',
                        'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter',
                        'float', 'frozenset', 'hex', 'int', 'isinstance', 'issubclass',
                        'len', 'list', 'map', 'max', 'min', 'oct', 'ord', 'pow',
                        'range', 'repr', 'reversed', 'round', 'set', 'slice',
                        'sorted', 'str', 'sum', 'tuple', 'zip']
        }

    def check_ast(self, tree):
        """Validate AST for potentially dangerous operations"""
        for node in ast.walk(tree):
            # Prevent imports outside allowed modules
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                module = node.names[0].name.split('.')[0]
                if module not in self.allowed_modules:
                    raise CodeExecutionError(f"Import of '{module}' is not allowed")
            
            # Prevent attribute access on forbidden objects
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    if node.value.id in ['os', 'sys', 'subprocess']:
                        raise CodeExecutionError(f"Access to '{node.value.id}' module is forbidden")

    def limit_resources(self):
        """Set resource limits for memory and CPU"""
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
        resource.setrlimit(resource.RLIMIT_CPU, (self.time_limit, self.time_limit))

    @contextmanager
    def capture_output(self):
        """Capture stdout and stderr"""
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def create_restricted_globals(self):
        """Create a restricted globals dictionary"""
        restricted_globals = {
            '_builtins_': self.safe_builtins,
            'print': print
        }
        return restricted_globals

    def run_code(self, code_str):
        """Execute code in sandbox environment"""
        try:
            # Parse and validate code
            tree = ast.parse(code_str)
            self.check_ast(tree)
            
            # Compile code
            compiled_code = compile(tree, '<string>', 'exec')
            
            # Prepare restricted environment
            restricted_globals = self.create_restricted_globals()
            restricted_locals = {}
            
            # Create a thread for execution with timeout
            result = {'output': '', 'error': None}
            
            def execute():
                try:
                    with self.capture_output() as (out, err):
                        exec(compiled_code, restricted_globals, restricted_locals)
                        result['output'] = out.getvalue()
                except Exception as e:
                    result['error'] = str(e)
            
            thread = threading.Thread(target=execute)
            thread.daemon = True
            
            # Run with timeout
            thread.start()
            thread.join(timeout=self.time_limit)
            
            if thread.is_alive():
                raise CodeExecutionError("Execution timed out")
            
            if result['error']:
                raise CodeExecutionError(result['error'])
                
            return result['output']
            
        except SyntaxError as e:
            raise CodeExecutionError(f"Syntax error: {str(e)}")
        except Exception as e:
            raise CodeExecutionError(str(e))

def run_in_sandbox(code_str):
    sandbox = Sandbox()
    try:
        output = sandbox.run_code(code_str)
        return {'success': True, 'output': output}
    except CodeExecutionError as e:
        return {'success': False, 'error': str(e)}