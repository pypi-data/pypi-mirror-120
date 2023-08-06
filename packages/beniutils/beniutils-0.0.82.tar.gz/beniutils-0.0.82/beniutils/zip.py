import os
from zipfile import ZIP_DEFLATED, ZipFile

from . import getAllFileAndFolderList, makeFolder


def zipFile(toFile, fileFolderOrAry, rename=None):
    makeFolder(os.path.dirname(toFile))
    ary = fileFolderOrAry
    if type(ary) != list:
        ary = [fileFolderOrAry]
    rename = rename or (lambda x: os.path.basename(x))
    with ZipFile(toFile, 'w', ZIP_DEFLATED) as f:
        for file in sorted(ary):
            fname = rename(file)
            f.write(file, fname)


def zipFileForFolder(toFile, folder, rename=None, filterFun=None):
    if not folder.endswith(os.path.sep):
        folder += os.path.sep
    rename = rename or (lambda x: x[len(folder):])
    ary = getAllFileAndFolderList(folder)
    if filterFun:
        ary = list(filter(filterFun, ary))
    zipFile(toFile, ary, rename)


def zipFileExtract(file, toFolder=None):
    toFolder = toFolder or os.path.dirname(file)
    with ZipFile(file) as f:
        for subFile in sorted(f.namelist()):
            try:
                # zipfile 代码中指定了cp437，这里会导致中文乱码
                encodeSubFile = subFile.encode('cp437').decode('gbk')
            except:
                encodeSubFile = subFile
            toFile = os.path.join(toFolder, encodeSubFile)
            toFile = toFile.replace('/', os.path.sep)
            f.extract(subFile, toFolder)
            # 处理压缩包中的中文文件名在windows下乱码
            if subFile != encodeSubFile:
                os.renames(os.path.join(toFolder, subFile), toFile)
