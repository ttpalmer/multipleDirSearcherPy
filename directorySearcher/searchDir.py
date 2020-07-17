import os,sys
from tqdm import tqdm
path = '.'
comparePath = '.'

def search(path):
    
    fileCounter = 0
    for filePath in walkdir(path):
        fileCounter += 1
    for filePath in tqdm(walkdir(path), total= fileCounter, unit="files"):
        print

def myFunc(e):
    return e['folder']


def walkdir(path):
    searchStr = input("Please enter search string: ")
    results =[]
    for root, dirs, files in os.walk(path):
       # for name in files:
        if searchStr in root.lower(): 
            print('--\nfolder: ' + root)
            results.append(root)
       
        for filename in files:
            if searchStr in filename.lower():
                full_path = os.path.join(root, filename)
                print('--\nfile : ' + filename.encode("utf-8").decode("ascii"))
                results.append(full_path)
                #print('--\nfile: %s (full path: %s)' % (filename, full_path ) )
                #print
    print ('--\nI have found', len(results), 'results!')
    print('--\n')
    for i in sorted(results):
        print ('--\n', i.encode("utf-8"))

def walk2dir(path1, path2):
    searchStr = input("Please enter search string: ")
    results1 = [] 
    results2 = []
    tResults = []
    for root, dirs, files in os.walk(path1):
        if searchStr in root.lower():
            print('--\nfolder: ' + root)
            results1.append(root)
            tResults.append(root)
        for filename in files:
            if searchStr in filename.lower():
                full_path = os.path.join(root,filename)
                print('--\nfile: ' + filename.encode("utf-8").decode("utf-8"))
                results1.append(full_path)
                tResults.append(full_path)
    print ('--\nI have found', len(results1), 'results in ',path1 )
    print('--\n')
    for i in sorted(results1):
        print ('--\n', i.encode("utf-8"))
    
    for root, dirs, files in os.walk(path2):
        if searchStr in root.lower():
            print('--\nfolder: ' + root)
            results2.append(root)
            tResults.append(root)
        for filename in files:
            if searchStr in filename.lower():
                full_path = os.path.join(root,filename)
                
                print('--\nfile: ' + filename.encode("utf-8").decode("utf-8"))
                results2.append(full_path)
                tResults.append(full_path)
    print ('--\nI have found', len(results2), 'results in ',path2 )
    print ('--\nI have found', len(tResults), 'total results ' )
    print('--\n')
    for i in sorted(results2):
        print ('--\n', i.encode("utf-8"))
    
    if results1 in tResults:
        print(results1)
    else:
        print('There are no duplicates')

def compare2Dirs():
    path = input("Input the path you would like to search: ")
    comparePath = input("Input the path you would like to compare: ")
    walk2dir(path,comparePath)
    nSearch = input('Would like another search in the directories? Press y for yes, n for no and r for new directories: ' )
    while nSearch == 'y':
        walk2dir(path,comparePath)


def welcome():
    print("Welcome to my searcher")
    choice = input("Type s if you want to search a folder or\n" +
    "press c if you want to compare two folders:")
    print
    if choice == 's':
        path = input("Input the path you would like to search: ")
        walkdir(path)
    elif choice == 'c':
        compare2Dirs()
        # path = input("Input the path you would like to search: ")
        # comparePath = input("Input the path you would like to compare: ")
        # walk2dir(path,comparePath)
        # nSearch = input('Would like another search in the directories? Press y for yes, n for no and r for new directories: ' )
        # if nSearch == 'y':
        #     walk2dir(path,comparePath)

if __name__ == '__main__':
    welcome()