import os
import ast
import re
from typing import Dict, List, Tuple, Optional

class PyCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []
        self.current_class = None

    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        self.classes.append({
            'name': node.name,
            'line': node.lineno,
            'methods': []
        })
        # Visit all child nodes (including methods)
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        # Extract function signature with parameters
        func_info = {
            'name': node.name,
            'line': node.lineno,
            'params': self._get_function_params(node)
        }
        
        # If inside a class, it's a method
        if self.current_class:
            for cls in self.classes:
                if cls['name'] == self.current_class:
                    cls['methods'].append(func_info)
        else:
            # It's a standalone function
            self.functions.append(func_info)
        
        # Continue visiting any nested functions
        self.generic_visit(node)

    def _get_function_params(self, node):
        """Extract function parameters with any default values"""
        params = []
        
        # Handle args
        for arg in node.args.args:
            param_str = arg.arg
            params.append(param_str)
            
        # Handle default values for args
        defaults = node.args.defaults
        if defaults:
            default_offset = len(node.args.args) - len(defaults)
            for i, default in enumerate(defaults):
                arg_idx = default_offset + i
                params[arg_idx] = f"{params[arg_idx]}={ast.unparse(default).strip()}"
        
        # Handle varargs (*args)
        if node.args.vararg:
            params.append(f"*{node.args.vararg.arg}")
            
        # Handle keyword-only args
        for kwarg in node.args.kwonlyargs:
            params.append(kwarg.arg)
            
        # Handle kw defaults
        for i, (arg, default) in enumerate(zip(node.args.kwonlyargs, node.args.kw_defaults)):
            if default is not None:
                params[len(node.args.args) + (1 if node.args.vararg else 0) + i] = f"{arg.arg}={ast.unparse(default).strip()}"
        
        # Handle kwargs (**kwargs)
        if node.args.kwarg:
            params.append(f"**{node.args.kwarg.arg}")
            
        return params


def process_python_file(file_path: str) -> Dict:
    """Process a single Python file and extract its class and function information."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        tree = ast.parse(content)
        visitor = PyCodeVisitor()
        visitor.visit(tree)
        
        return {
            'file_path': file_path,
            'classes': visitor.classes,
            'functions': visitor.functions
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {
            'file_path': file_path,
            'error': str(e),
            'classes': [],
            'functions': []
        }


def scan_directory(directory: str = '.') -> List[Dict]:
    """Recursively scan directory for Python files and extract information."""
    results = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                result = process_python_file(file_path)
                if result:
                    results.append(result)
                    
    return results


def write_mapping_file(results: List[Dict], output_file: str = 'python_code_mapping.txt'):
    """Write the mapping information to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("PYTHON CODE MAPPING\n")
        f.write("==================\n\n")
        
        for result in results:
            f.write(f"FILE: {result['file_path']}\n")
            f.write("=" * (len(result['file_path']) + 6) + "\n\n")
            
            if 'error' in result:
                f.write(f"ERROR: {result['error']}\n\n")
                continue
            
            # Write classes and their methods
            for cls in result['classes']:
                f.write(f"CLASS: {cls['name']} (line {cls['line']})\n")
                f.write("-" * (len(cls['name']) + 14) + "\n")
                
                for method in cls['methods']:
                    params_str = ", ".join(method['params'])
                    f.write(f"  METHOD: {method['name']}({params_str}) (line {method['line']})\n")
                
                f.write("\n")
            
            # Write standalone functions
            if result['functions']:
                f.write("FUNCTIONS:\n")
                f.write("----------\n")
                
                for func in result['functions']:
                    params_str = ", ".join(func['params'])
                    f.write(f"  {func['name']}({params_str}) (line {func['line']})\n")
                
            f.write("\n\n")


if __name__ == "__main__":
    print("Scanning directory for Python files...")
    results = scan_directory()
    
    output_file = "python_code_mapping.txt"
    write_mapping_file(results, output_file)
    
    print(f"\nProcessed {len(results)} Python files.")
    print(f"Mapping information written to {output_file}")
