import os,sys
from log import log as log
from tqdm import tqdm
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import pyprobe
from ffprobe import FFProbe
from tinytag import TinyTag
from colorama import init, Fore, Back, Style
import math

path = '.'
comparePath = '.'


def walkDir(path):
    searchStr = input("Please enter search string: ")
    results = []
    badFiles = []
    allData = []
    checkFiles = []
    metadataDict = {}
    folderExists = False
    # pyparser = pyprobe.VideoFileParser(ffprobe="C:/Windows/Python37/Lib/site-packages/ffprobe.py", includeMissing=True, rawMode=False)
    for root, subdirs, files in os.walk(path):
        if searchStr.lower() in root.lower(): 
            folderExists = True
            # log('m',' -------------\nfolder: ' + root)
        for filename in files:
            if searchStr.lower() in filename.lower():
                # if folderExists:
                full_path = os.path.join(root,filename)
                    # log('i', full_path)
                # else:
                    # full_path = os.path.join(path,filename)
                try:
                    log('m', '[' +str(len(results)+1) + '] ' + full_path.encode('utf-8').decode('ascii'))
                except UnicodeError as err:
                    log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                    log('m', full_path.encode('utf-8').decode('utf-8'))
                results.append(full_path)               
                try:
                    (metadata,check) = retrieveMetadata(full_path)
                    tag = TinyTag.get(full_path)
                    fileType = metadata.exportPlaintext()[8]
                    if None != check:
                        checkFiles.append(check)
                    
                    if "video" in fileType: 
                        
                        fileSize = convFileSize(tag.filesize)
                        duration = tag.duration 
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
    log('s',"----------------\n"+ str(len(results))+ ' results found!')
    
        
def checkDuplicates(path1,path2):
    results1 = []
    results2 = []
    tresults = []
    data1 = []
    data2 = []
    data3 = []
    badFiles = []
    checkFiles = []
    for root, subdirs, files in tqdm(os.walk(path1)):
        
        for filename1 in files:
            if ".MP4" in filename1.upper() or ".MOV" in filename1.upper() or ".WMV" in filename1.upper() or ".VID" in filename1.upper() or ".AVI" in filename1.upper() or ".TORRENT" in filename1.upper() :
                full_path1 = os.path.join(root,filename1)
                try:
                    log('i', full_path1.encode('utf-8').decode('ascii'))
                except UnicodeError as err:
                    log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                    log('i', full_path1.encode('utf-8').decode('utf-8'))
                results1.append(full_path1)
                tresults.append(full_path1)
                try:
                    (metadata, check) = retrieveMetadata(full_path1)
                    checkFiles.append(check)
                    fileType1 = metadata.exportPlaintext()[8]
                    tag = TinyTag.get(full_path1)
                    if "video" in fileType1:
                        
                    
                        dimensions1 = (metadata.exportPlaintext()[2],metadata.exportPlaintext()[3])
                        duration1 = tag.duration
                        fileSize1 = convFileSize(tag.filesize)
                        data = (filename1,full_path1,fileSize1, fileType1,duration1,dimensions1)
                        data1.append(data)
                        data3.append(data)
                        log('i', str(data1).encode('utf-8').decode('ascii'))
                    elif 'torrent' in fileType1:
                        # tag = TinyTag.get(full_path1)
                        fileSize1 = convFileSize(tag.filesize)
                        dlSize1 = metadata.exportPlaintext()[2]
                        tdata = (filename1, full_path1,fileType1,dlSize1)
                except Exception as err:
                    if 'Input size is nul' in str(err):
                        log('e', str(err))
                        log('e', 'File < ' + full_path1.encode('utf-8').decode('ascii') + ' > may have 0 bytes check file' )
                        badFiles.append(full_path1)
                        break
                    
    for root, subdirs, files in tqdm(os.walk(path2)):
        results2.append(root)
        tresults.append(root)
        for filename2 in files:
            if ".MP4" in filename2.upper() or ".MOV" in filename2.upper() or ".WMV" in filename2.upper() or ".VID" in filename2.upper() or ".AVI" in filename2.upper() or ".TORRENT" in filename1.upper():
                full_path2 = os.path.join(root,filename2)
                try:
                    log('i', full_path2.encode('utf-8').decode('ascii'))
                except UnicodeError as err:
                    # log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                    log('i', full_path1.encode('utf-8').decode('utf-8'))
                results2.append(full_path2)
                tresults.append(full_path2)
                try:
                    (metadata, check) = retrieveMetadata(full_path2)
                    checkFiles.append(check)   
                    tag = TinyTag.get(full_path2)
                    if "video" in fileType1:
                        duration2 = tag.duration
                        fileSize2 = convFileSize(tag.filesize)
                        fileType2 = metadata.exportPlaintext()[8]
                        dimensions2 = (metadata.exportPlaintext()[2],metadata.exportPlaintext()[3])
                        data = (filename2,full_path2,fileSize2, fileType2,duration2,dimensions2)
                        data2.append(data)
                        data3.append(data)
                        log('i', str(data2).encode('utf-8').decode('ascii'))
                    elif 'torrent' in fileType1:
                        # tag = TinyTag.get(full_path1)
                        fileSize1 = convFileSize(tag.filesize)
                        dlSize1 = metadata.exportPlaintext()[2]
                        tdata = (filename1, full_path1,fileType1,dlSize1)
                except Exception as err:
                    if 'Input size is nul' in str(err):
                        log('e',str(err))
                        log('e', 'File < ' + full_path2.encode('utf-8').decode('ascii') + ' > may have 0 bytes check file' )
                        badFiles.append(full_path2)
                        break
                # if metadata.exportPlaintext() is None:
                #     log('e' , 'File < ' + full_path1 + ' > may stil be downloading check it ')
                # else:
                #     checkFiles.append(check)
                #     tag = TinyTag.get(full_path1)
                #     duration2 = tag.duration
                #     fileSize2 = convFileSize(tag.filesize)
                #     fileType2 = metadata.exportPlaintext()[8]
                #     dimensions2 = (metadata.exportPlaintext()[2],metadata.exportPlaintext()[3])
                #     data2 = (filename2,full_path2,fileSize2, fileType2,duration2,dimensions2)
            # data3. (filename1,full_path2,fileSize2, fileType2,duration2,dimensions2)
    (simNm,simSz,simdur) = compareFiles(data3)
    log('s', " I found " + str(len(results1)) + ' total results in ' + full_path1)
    log('s', " I found " + str(len(results2)) + ' total results in ' + full_path2)
    if len(simNm) > 0:
        log('s', 'Their may be ' + str(len(simNm)) + ' files similar based on name they are: ')
        for i in simNm:
            log('i', i.encode('utf-8').decode('ascii'))
    if len(simSz) > 0:
        log('s', 'Their may be ' + str(len(simSz)) + ' files similar based on name they are: ')
        for i in simSz:
            log('i', i.encode('utf-8').decode('ascii'))
    if len(simdur) > 0:
        log('s', 'Their may be ' + str(len(simdur)) + ' files similar based on name they are: ')
        for i in simdur:
            log('i', i.encode('utf-8').decode('ascii'))
    if len(badFiles) > 0:
        log('e', 'There are ' + str(len(badFiles)) +' files you may need to look at because they may have 0 bytes they are: ')
        for i in badFiles:
            print (i.encode('utf-8').decode('ascii'))
    if len(checkFiles) > 0:
        log('e', 'There are ' + str(len(checkFiles)) +' files you may need to look at because they may be downloading they are: ')
        for i in checkFiles:
            print (i.encode('utf-8').decode('ascii'))

def compareFiles(data):
    for i in data:
        md = i
        data.pop(i)
        filename1 = md[0]
        filename2 = i[0]
        path1 = md[1]
        path2 = i[1]
        fsize1 = md[2]
        fsize2 = i[2]
        ftype1 = md[3]
        ftype2 = i[3]
        duration1 = md[4]
        duration2 = i[4]
        dimensions1 = md[5]
        dimensions2 = i[5]
        simNm = []
        simSz = []
        simTp = []
        simdur = []
        simDm = []
        simFiles = False
        print(filename1)
        
        if filename1 in filename2 or filename2 in filename1 :
            log('s', "File: " + path1 + " and " + path2 + "maybe be the same based on filename")
            simNm.append(path1,path2)
        elif fsize1 == fsize2 and ftype1 == ftype2 and dimensions1 == dimensions2:
            log('s', "File: " + path1 + " and " + path2 + "maybe be the same based on file size")
            simSz.append(path1,path2)
        elif duration1 == duration2:
            log('s', "File: " + path1 + " and " + path2 + "maybe be the same based on length of video")
            simdur.append(path1,path2)
    
    log('i' , "Found no possible similar files")
    return simNm, simSz,simdur
    
        
def convertSeconds(duration):
    videolength = duration/60
    if "." in str(videolength):
        seconds = videolength % 1
        videolength = round(videolength,1)
    return videolength        
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
        log('e', 'File < ' + file + ' > may stil be downloading check it ')
        checkFiles.append(file)
    # print (metadata.exportPlaintext()[1])
    # for line in metadata.exportPlaintext():
    #     print( line)
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

def walk2Dirs(path1,path2):
    searchStr = input("Please enter search string: ")
    results1 = []
    results2 = []
    tresults = []
    data1 = []
    data2 = []
    data3 = []
    badFiles = []
    checkFiles = []
    metadataDict = {}
    folderExists = False
    allData = []
    for root, subdirs, files in os.walk(path1):
        if searchStr.lower() in root.lower(): 
            folderExists = True
            # log('m',' -------------\nfolder: ' + root)
        for filename in files:
            if searchStr.lower() in filename.lower():
                if folderExists:
                    full_path = os.path.join(root,filename)
                    # log('i', full_path)
                else:
                    full_path = os.path.join(path1,filename)
                try:
                    log('m', '[' +str(len(results1)+1) + '] ' + full_path.encode('utf-8').decode('ascii'))
                except UnicodeError as err:
                    log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                    log('m', full_path.encode('utf-8').decode('utf-8'))
                results1.append(full_path)
                tresults.append(full_path)               
                try:
                    (metadata,check) = retrieveMetadata(full_path)
                    tag = TinyTag.get(full_path)
                    fileType = metadata.exportPlaintext()[8]
                    if None != check:
                        checkFiles.append(check)
                    
                    if "video" in fileType: 
                        
                        fileSize = convFileSize(tag.filesize)
                        duration = tag.duration 
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
                    
    for root, subdirs, files in os.walk(path2):
        if searchStr.lower() in root.lower(): 
            folderExists = True
            # log('m',' -------------\nfolder: ' + root)
        for filename in files:
            if searchStr.lower() in filename.lower():
                if folderExists:
                    full_path = os.path.join(root,filename)
                    # log('i', full_path)
                else:
                    full_path = os.path.join(path2,filename)
                try:
                    log('m', '[' +str(len(results2)+1) + '] ' + full_path.encode('utf-8').decode('ascii'))
                except UnicodeError as err:
                    log('e', 'May have bad encoding, Trying Again...\n' + str(err))
                    log('m', full_path.encode('utf-8').decode('utf-8'))
                results2.append(full_path)  
                tresults.append(full_path)             
                try:
                    (metadata,check) = retrieveMetadata(full_path)
                    tag = TinyTag.get(full_path)
                    fileType = metadata.exportPlaintext()[8]
                    if None != check:
                        checkFiles.append(check)
                    
                    if "video" in fileType: 
                        
                        fileSize = convFileSize(tag.filesize)
                        duration = tag.duration 
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
                # results2.append(full_path)
    log('s',"----------------\nI have found "+ str(len(results1))+ ' results in '+ path1)
    log('s',"----------------\nI have found "+ str(len(results2))+ ' results in '+ path2)
    log('s',"----------------\nI have found "+ str(len(tresults))+ ' total results!')
    for data in allData:
        log('m','--------------\n'+ '[ ' + str(allData.index(data)+1) + ' ]')
        for i in data:
            log('m', str(i) + ':' + str(data[i]))
def openFolder(folder,c):
    # elements = 'ele'
    # seagate = 'sea'
    # toshiba = 'tosh'
    # seagateV = 'seav'
    # toshibaV = 'toshv'
    # appProjects = 'app'
    # documents = 'doc'
    # downloads = 'down'
    
    elementP = 'J:\Film420\TorrentData'
    seagatep = 'L:\Stuff'
    toshibaP = r'I:\Users\Tyler'
    seagateVP = 'L:\Stuff\FILM 420'
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
    

def compare2Dirs(c):
    # path = input("Input the first path you would like to search: ")
    # path2 = input("Input the second path you would like to search: ")
    paths = getFolder(c)
    log('i', str(paths))
    searching = True
    while searching:
        walk2Dirs(paths[0],paths[1])
        nSearch = input("Would you like another search? \nEnter (y) for YES, (n) for NO, and (nd) for new directories.")
        if nSearch == "y":
            walk2Dirs(paths[0],paths[1])
        elif nSearch == "n":
            searching = False
            break
        elif nSearch == "nd":
            npath = input("Input the first path you would like to search: ")
            npath2 = input("Input the second path you would like to search: ")
            walk2Dirs(npath,npath2)

    welcome()

def welcome():
    print( Fore.CYAN + "Welcome to my searcher")
    choice = input('Enter ( s ) if you want to search a directory\n'+
                   "Enter ( t ) if you would like to search 2 directories: \n"+
                   "Enter ( d ) if you would like to check for duplicates in 2 directories: \n" +
                   "Enter ( o ) if you would like to open folder(s) \n"+
                   "Enter ( c ) if you would like to cancel\n")
    if choice == 's':
        # path = input('Enter the path you would like to search in:')
        paths = getFolder(choice)
        log('i', paths[0])
        walkDir(paths[0])
    elif choice == 't':
        compare2Dirs(choice)
    elif choice == 'd':
        path1 = input("Input the first path you would like to check: ")
        path2 = input("Input the second path you would like to check: ")
        checkDuplicates(path1,path2)
    elif choice == 'o':
        getFolder(choice)
    elif choice == 'c':
        exit(0)

if __name__ == '__main__':
    welcome()
        
