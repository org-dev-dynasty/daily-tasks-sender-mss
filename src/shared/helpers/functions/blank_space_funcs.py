import os
import re

def ensure_blank_line_after_functions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    inside_function = False

    for line in lines:
        if inside_function and (line.strip().startswith('def ') or line.strip().startswith('class ')):
            new_lines.append('\n')
            inside_function = False

        new_lines.append(line)
        
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            inside_function = True

    # Para garantir que a última função do arquivo também tenha uma linha em branco
    if inside_function:
        new_lines.append('\n')

    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def format_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                ensure_blank_line_after_functions(os.path.join(root, file))

# Use a função no seu diretório do projeto
format_directory('./src/')

print(os.listdir('./src/'))

print("Formatação concluída.")

