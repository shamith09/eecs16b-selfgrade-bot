from os import scandir, remove

for file in scandir('out'):
    remove(file.path)