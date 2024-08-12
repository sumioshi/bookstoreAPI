import os

def export_structure_and_code(directory, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}{os.path.basename(root)}/\n')
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                f.write(f'{sub_indent}{file}\n')
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as code_file:
                        for line in code_file:
                            f.write(f'{sub_indent}{line}')
                except Exception as e:
                    f.write(f'{sub_indent}Could not read file: {e}\n')
                f.write('\n')

directory_to_export = r'C:\bookstoreAPI'  # Use uma string bruta para o caminho
output_file = 'project_structure_with_code.txt'

export_structure_and_code(directory_to_export, output_file)
print(f"Estrutura do projeto e códigos exportados para {output_file}")
