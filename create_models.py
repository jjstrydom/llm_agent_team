import os
import subprocess

prefix = "Modelfile_"
directory = "."

def find_files_with_prefix(directory, prefix):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(prefix):
                yield os.path.join(root, file)
    return None

for file in find_files_with_prefix(directory, prefix):
    start_loc = file.find(prefix)
    suffix = file[(start_loc + len(prefix)):]
    model_name = f'agent_{suffix}'
    print(model_name)
    args = ['ollama', 'create', model_name, '-f', file]
    subprocess.call(args) 


