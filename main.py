#!/usr/bin/python3

from genericpath import isdir
import os
import zipfile
import shutil
import re

def resetFolder(folder: str):
    if os.path.isdir(folder):
        shutil.rmtree(folder)

    os.makedirs(folder)

def extractZipFiles(iconZipFolder: str, iconFolder: str):
    zipFiles = os.listdir(iconZipFolder)

    for zipFile in zipFiles:
        zipFilePath = iconZipFolder + '/' + zipFile
        if (zipfile.is_zipfile(zipFilePath)):
            with zipfile.ZipFile(zipFilePath, 'r') as zipRef:
                zipRef.extractall(iconFolder)

    shutil.rmtree(os.path.join(iconFolder, '__MACOSX'))

def extractGroupFromFile(file: str):
    return file.split('-')[1]

def extractNameFromFile(file: str):
    name = '-'.join(file.split('-')[2::])
    name = re.sub(r'--\d+x\d+', '', name)
    name = re.sub(r'\.SVG', '.svg', name)

    return name

def restructureFiles(files: list[str], inputFolder: str, outputFolder: str):
    for file in files:
        group = extractGroupFromFile(file)
        name = extractNameFromFile(file)

        filePath = os.path.join(inputFolder, file)
        newFilePath = os.path.join(outputFolder, group, name)
        folderPath = os.path.dirname(newFilePath)

        if not os.path.isdir(folderPath):
            os.makedirs(folderPath)

        shutil.copy(filePath, newFilePath)

if __name__ == '__main__':
    unorganizedIconsFolder = 'unorganized-icons'
    iconZipFolder = 'icon-zip-folders'
    iconsFolder = 'icons'

    resetFolder(unorganizedIconsFolder)
    resetFolder(iconsFolder)
    extractZipFiles(iconZipFolder, unorganizedIconsFolder)

    for root, dirs, files in os.walk(unorganizedIconsFolder):
        if root == unorganizedIconsFolder:
            continue

        restructureFiles(
            files,
            root,
            os.path.join(iconsFolder, root.split('/')[1])
        )

    shutil.rmtree(unorganizedIconsFolder)
