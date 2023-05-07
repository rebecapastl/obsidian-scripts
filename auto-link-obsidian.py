from dotenv import load_dotenv
import os

# load env vars
load_dotenv()
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
VAULT_INDEX_FILE = os.getenv("VAULT_INDEX_FILE")

def get_md_file_names(folder, excluded_file=None):
    md_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.md') and file != excluded_file:
                md_files.append(os.path.join(root, file))
    return md_files

def save_file_names(file_names, output_file, folder_path):
    with open(output_file,'w', encoding='utf-8') as file:
        file.write(folder_path + "\n")
        for name in file_names:
            file.write(name + '\n')

def handle_title_case(line, file_names, original_lines, md_file):
    current_file = os.path.splitext(os.path.basename(md_file))[0]
    title = line.strip('#').strip()
    for name in file_names:
        file_name = os.path.splitext(os.path.basename(name))[0]
        if file_name.lower() == title.lower():
            new_line = f'[[{file_name}]] main article.\n'
            modified_line = line
            if new_line not in original_lines and current_file != file_name:
                return modified_line + new_line
    return line

def handle_other_case(line, file_names, md_file):
    current_file = os.path.splitext(os.path.basename(md_file))[0]
    for name in file_names:
        file_name = os.path.splitext(os.path.basename(name))[0]
        if file_name in line and f'[[{file_name}]]' not in line and current_file != file_name:
            line = line.replace(file_name, f'[[{file_name}]]')
    return line

def search_and_highlight_names(file_names):
    for md_file in file_names:
        with open(md_file, 'r', encoding='utf-8') as file:
            original_lines = file.readlines()
        
        modified_lines = []
        for line in original_lines:
            if line.startswith('#'):
                modified_line = handle_title_case(line, file_names, original_lines, md_file)
            else:
                modified_line = handle_other_case(line, file_names, md_file)
            modified_lines.append(modified_line)
        
        with open(md_file, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
        
        print(f'Processed "{md_file}"')


# Replace 'folder_path' with the path to the folder containing the .md files
folder_path = OBSIDIAN_VAULT_PATH

# Replace 'file_to_exclude.md' with the file that represents the vault index, if the vault has an index file
excluded_file = VAULT_INDEX_FILE

# Replace 'output.txt' with the desired name of the output file
output_file = 'temp_file.txt'

md_file_names = get_md_file_names(folder_path, excluded_file)

save_file_names(md_file_names, output_file, folder_path)

search_and_highlight_names(md_file_names)

# Delete the output file
os.remove(output_file)