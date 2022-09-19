import os,sys
from log import log as log
from tqdm import tqdm
import time
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from tinytag import TinyTag
from colorama import init, Fore, Back, Style
import math

path = '.'

def convertSeconds(duration):
    videolength = duration/60
    if "." in str(videolength):
        seconds = videolength % 1
        videolength = round(videolength,1)
    return str(videolength) + " minutes"        
def retrieveMetadata(file):
    
    checkFiles = []
    parser = createParser(file)
    # fileSize = tag.filesize/(1024*1024)
    if not parser:
        log('e','Unable to parse')
        log('e', 'File < ' + file + ' > may stil be downloading check it ')
        checkFiles.append(file)
    with parser:
        try:
            metadata = extractMetadata(parser) 
            checkFiles = None
            # print (metadata)
        except Exception as err:
            log('e',"Metadata extraction error: %s" % err )
            metadata = None
    if not metadata:
        log('e', 'Unable to extract metadata')
        log('e', 'File < ' + file + ' > could stil be downloading check it ')
        checkFiles.append(file)
    # print (metadata.exportPlaintext()[1])
    for line in metadata.exportPlaintext():
         print( line)
    return metadata, checkFiles
        
def convFileSize(fileSize):
    # fileSize = 1201026675
    KB = 1024
    MB = math.pow(KB,2)
    # print (MB)
    GB = math.pow(KB,3)
    # print (GB)
    TB= math.pow(KB,4)
    # print (TB)
    
    if fileSize > KB and fileSize < MB:
        return str(fileSize) + 'KB'
    elif fileSize > MB and fileSize < GB:
        fileSize = round(fileSize/MB,3)
        return  str(fileSize) + 'MB'
    elif fileSize > GB and fileSize < TB:
        fileSize = round(fileSize/GB,3)
        return  str(fileSize) + 'GB'
    # elif fileSize > GB and fileSize < TB:
    #     fileSize = round(fileSize/TB,3)
    #     return  str(fileSize) + 'TB'
    
def openFolder(folder,c):
    # elements = 'ele'
    # seagate = 'sea'
    # toshiba = 'tosh'
    # seagateV = 'seav'
    # toshibaV = 'toshv'
    # appProjects = 'app'
    # documents = 'doc'
    # downloads = 'down'
    
    elementP = 'E:\Film420\TorrentData'
    seagatep = 'L:\Stuff'
    toshibaP = r'I:\Users\Tyler'
    seagateVP = 'F:\Stuff\Film420'
    toshibaVP = r'I:\Users\Tyler\Documents\FrostWire\Torrent Data'
    appProjectsP = r'C:\Users\Larry OG\Documents\Apps'
    documentsp = r'C:\Users\Larry OG\Documents'
    downloadsP = r"C:\Users\Larry OG\Downloads"
    
    if folder == "1" and c ==  'o':
        os.startfile(elementP)
        # return welcome()
    elif folder == '1' and c != 'o':
        return elementP
    elif folder == '2' and c ==  'o':
        os.startfile(seagatep)
        # return welcome()
    elif folder == '2'and c != 'o':
        return seagatep
    elif folder == '3' and c ==  'o':
        os.startfile(toshibaP)
        # return welcome()
    elif folder == '3'and c != 'o':
        return toshibaP
    elif folder == '4' and c ==  'o':
        os.startfile(seagateVP)
        # return welcome()
    elif folder == '4'and c != 'o':
        return seagateVP
    elif folder == '5' and c ==  'o':
        os.startfile(toshibaVP)
        # return welcome()
    elif folder == '5'and c != 'o':
        return toshibaVP
    elif folder == '6' and c ==  'o':
        os.startfile(appProjectsP)
        # return welcome()
    elif folder == '6'and c != 'o':
        return appProjectsP
    elif folder == '7' and c ==  'o':
        os.startfile(documentsp)
        # return welcome()
    elif folder == '7'and c != 'o':
        return documentsp
    elif folder == '8' and c ==  'o':
        os.startfile(downloadsP)
        # return welcome()
    elif folder == '8'and c != 'o':
        return downloadsP
    elif c ==  'o':
        os.startfile(folder)
    return welcome()
    
        
def getFolder (c):
    log('m', "Enter the correspnding number to choose a preset path")
    log('m', "[ 1 ] Elements \n" +
        '[ 2 ] Seagate \n' +
        '[ 3 ] Toshiba \n' +
        '[ 4 ] Seagate flicks \n' +
        '[ 5 ] Toshiba flicks \n' +
        '[ 6 ] App Projects \n' +
        '[ 7 ] Docuents \n' +
        '[ 8 ] Downloads \n')
    
    paths = []
    amount = ''
    if c ==  'o':
        amount = input("How many folders would you like to open?\n")
    if amount == '1' or c == 's':
        location = input('Enter the path or choose preset path: \n')
        path = openFolder(location,c)
        paths.append(path)
        if c == 'o':   
            openFolder(path,c)
            return welcome()
    elif amount == '2' or c =='t':
        path1 = input('Enter the first path or choose preset path: \n')
        path2 = input('Enter the second path or choose preset path: \n')
        paths.append(path1)
        paths.append(path2)
        for i in paths:
            
            location = i 
            log('i', location)
            path = openFolder(location,c)
            log('i', str(path))
            paths[paths.index(i)] = path
            # paths.append(path)
        if c == 'o':
            openFolder(path1)
            openFolder(path2)
            return welcome()
    elif amount == '3':
        path1 = input('Enter the first path or choose preset path: \n')
        path2 = input('Enter the second path or choose preset path: \n')
        path3 = input('Enter the second path or choose preset path: \n')
        if c == 'o':
            paths.append(path1)
            paths.append(path2)
            paths.append(path3)
            for i in paths:
                openFolder(i)
                return welcome()
    print()
    return paths

def walkDir(path):
    searchStr = input("Please enter search string: ")
    results = []
    badFiles = []
    allData = []
    checkFiles = []
    metadataDict = {}
    folderExists = False
    # pyparser = pyprobe.VideoFileParser(ffprobe="C:/Windows/Python37/Lib/site-packages/ffprobe.py", includeMissing=True, rawMode=False)

    for root, subdirs, files in tqdm(os.walk(path)):
        if searchStr.lower() in root.lower(): 
            folderExists = True
            # log('m',' -------------\nfolder: ' + root)
        for filename in files:
            if searchStr.lower() in filename.lower() and '.nfo' not in filename.lower() :
                # if folderExists:
                full_path = os.path.join(root,filename)
                    # log('i', full_path)
                # else:
                    # full_path = os.path.join(path,filename)
                # try:
                #     #log('m', '[' +str(len(results)+1) + '] ' + full_path.encode('utf-8').decode('ascii'))
                #     log('s', 'Booyah')
                # except UnicodeError as err:
                #     log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                #     log('m', full_path.encode('utf-8').decode('utf-8'))
                results.append(full_path)               
                try:
                    (metadata,check) = retrieveMetadata(full_path)
                    tag = TinyTag.get(full_path)
                    fileType = metadata.exportPlaintext()[8]
                    if None != check:
                        checkFiles.append(check)
                    
                    if "video" in fileType: 
                        
                        fileSize = convFileSize(tag.filesize)
                        duration = convertSeconds(tag.duration) 
                        dimensions = (metadata.exportPlaintext()[2],metadata.exportPlaintext()[3]) 
                        data = (filename,full_path,fileSize, fileType,duration,dimensions)
                        metadataDict = {
                        'name' : filename,
                        'path' : full_path,
                        'type' : fileType,
                        'size' : fileSize,
                        'duration' : duration,
                        'dimensions' : dimensions
                        }
                        allData.append(metadataDict)
                        # log('s', str(metadataDict))
                except Exception as err:
                    if 'Input size is nul' in str(err):
                        log('e',str(err))
                        log('e', 'File < ' + full_path + ' > may have 0 bytes check file' )
                        badFiles.append(full_path)
                        break
    if len(badFiles) > 0:
        log('e', 'There are ' + str(len(badFiles)) +' files you may need to look at are: ')
        for i in badFiles:
            log('e', i)
    # for i in checkFiles:
    #     if None == i:
    #         checkFiles.remove(i)
    if len(checkFiles) > 0:
        log('e', 'There are ' + str(len(checkFiles)) +' files you may need to look at because they may be downloading they are: ')
        for i in checkFiles:
            print (i)
    for i in results:
       log('m','[' + str(results.index(i)+1) + ']' + i)
    for r in allData:
        log('m', '[' + str(allData.index(r)+1) + ']' + str(r) + '\n')
    
    log('s',"----------------\n"+ str(len(results))+ ' results found!')

def welcome():
    print( Fore.CYAN + "Welcome to my searcher")
    choice = input('Enter ( s ) if you want to search a directory\n'+
                   "Enter ( t ) if you would like to search 2 directories: \n"+
                   "Enter ( d ) if you would like to check for duplicates in 2 directories: \n" +
                   "Enter ( o ) if you would like to open folder(s) \n"+
                   "Enter ( c ) if you would like to cancel\n")
    # Make a choice to search based on resolution 
    if choice == 's':
        # path = input('Enter the path you would like to search in:')
        paths = getFolder(choice)
        log('i', paths[0])
        walkDir(paths[0])
    elif choice == 'c':
        exit(0)

if __name__ == '__main__':
    welcome()