# MarkdownImageUploader

For people who are used to write in markdown, generating public url for your own image is a problem, so this repository offers a simple tool for you to upload image to github repository and generate url of the image, it works like this

1. select the image that you want to upload
2. commit and push it to the github repository and get the public url of it

Following is an example

<img src="/imgs/upload.gif?raw=true">

## Requirements

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed and is available in the PATH environment
- privilege to the repository for uploading your images

## How to use

Make sure the requirements is satisfied, for the first time to use MarkdownImagesUploader, you need to configure your github repository address and local repository path, like the following, then the information will be recorded in the `config` directory under the path of the program.

<img src="/imgs/configure.gif?raw=true">

Windows users can download (MarkdownImageUploader_win_x64.exe)[https://github.com/WuLC/MarkdownImageUploader/releases/MarkdownImageUploader_win_x64.exe], it should be working on win7_x64 and win10_x64, which I have tested. 

For Linux or Mac users, install (PySimpleGUI)[https://github.com/PySimpleGUI/PySimpleGUI] with `pip install PySimpleGUI`, then run the script `python main.py` as a background program. But PySimpleGUI doesn't seem to work quite well with mac, and I'm not sure whether this work with mac.