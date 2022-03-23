from os import scandir, remove

try:
    for file in scandir('out'):
        remove(file.path)
    print('Emptied the out folder!')
except:
    print('There is no out folder to empty!')