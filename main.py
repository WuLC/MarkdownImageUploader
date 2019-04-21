# -*- coding: utf-8 -*-
# Created on Sun Apr 21 2019 15:54:34
# Author: WuLC
# EMail: liangchaowu5@gmail.com

import os
import pickle
import shutil
import subprocess

import PySimpleGUI as sg

     
# sg.Popup('Results', 'The value returned from PopupGetFile', text)

def load_configuration():
    file_path = './config.pkl'
    if not os.path.exists(file_path):
        return ' '*100, ' '*100
    with open(file_path, 'rb') as rf:
        config = pickle.load(rf)
    return config['github_repo'], config['local_repo']


def save_configuration(github_repo, local_repo):
    file_path = './config.pkl'
    data = {'github_repo': github_repo, 'local_repo': local_repo}
    with open(file_path, 'wb') as wf:
        pickle.dump(data, wf)


def configure_github_repo_address():
    text = sg.PopupGetText('Input the address starts with git@', 'Input the address of your github repository')
    if text == None:
        return 
    if text.startswith('git@'):
        return text
    else:
        sg.Popup('address {0} is not legal'.format(text))


def configure_local_repo_path():
    text = sg.PopupGetFolder('Browse to select the path of your local repository')      
    if text == None:
        return
    else:
        return text


def commit_and_push(github_repo, local_repo):
    repo_dir_name = github_repo.split('/')[-1].rstrip('.git')
    repo_dir_path = os.path.join(local_repo, repo_dir_name).replace('\\', '/')

    layout = [
        [sg.Text('Choose image file', size=(20, 1)), sg.InputText(), sg.FileBrowse()],
        [sg.Text('Commit message', size=(20, 1)), sg.InputText()],
        [sg.Submit('commit and push'), sg.Cancel()]
        ]
    window = sg.Window('Commit and push image')
    event, values = window.Layout(layout).Read()
    window.Close()
    # copy image, commit and push
    src_img_path, commit_message = values
    img_name = src_img_path.split('/')[-1]
    if src_img_path:
        shutil.copy(src_img_path, repo_dir_path)
    commands = 'cd {0} && git add * && git commit -m {1} && git push origin master'.format(repo_dir_path, commit_message)
    command = ['cd', 'C:/users/435', '&&', 'dir']

def main():
    github_repo, local_repo = load_configuration()
    layout = [
        [sg.Button('configure_github_repo_address', size=(25, 1)), 
        sg.Text('Your github repository address', size=(24, 1)), 
        sg.Text(github_repo, key = '__remote_repo__', justification = 'left')],      
        [sg.Button('configure_local_repo_path', size=(25, 1)), 
        sg.Text('Your local repository path', size=(24, 1)), 
        sg.Text(local_repo, key = '__local_repo__', justification = 'left')], 
        [sg.Text('_'  * 80)],           
        [sg.Button('commit & push', size=(20, 1))]
    ]

    window = sg.Window('Markdown Image Uploader').Layout(layout)

    while True:
        event, values = window.Read()
        if event == 'configure_github_repo_address':
            github_repo = configure_github_repo_address()
            if github_repo and github_repo.strip():
                window.Element('__remote_repo__').Update(github_repo)
        if event == 'configure_local_repo_path':
            local_repo = configure_local_repo_path()
            if local_repo and local_repo.strip():
                window.Element('__local_repo__').Update(local_repo)
        if event == 'commit & push':
            commit_and_push(github_repo, local_repo)
        if event is None:
            if github_repo != None and local_repo != None:
                save_configuration(github_repo, local_repo)
            break  
    window.Close()


if __name__ == '__main__':
    main()