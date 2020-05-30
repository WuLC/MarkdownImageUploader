# -*- coding: utf-8 -*-
# Created on Sun Apr 21 2019 15:54:34
# Author: WuLC
# EMail: liangchaowu5@gmail.com

import os
import pickle
import shutil
import urllib.parse
import subprocess

import PySimpleGUI as sg


def load_configuration():
    """load the address of github repository and the path of local repository"""
    config_file = './config/config.pkl'
    if not os.path.exists(config_file):
        return ' '*100, ' '*100
    with open(config_file, 'rb') as rf:
        config = pickle.load(rf)
    return config['github_repo'], config['local_repo']


def save_configuration(github_repo, local_repo):
    """save the address of github repository and the path of local repository"""
    config_file = './config/config.pkl'
    if not os.path.exists('./config'):
        os.makedirs('./config/')
    data = {'github_repo': github_repo, 'local_repo': local_repo}
    with open(config_file, 'wb') as wf:
        pickle.dump(data, wf)


def configure_github_repo_address():
    text = sg.PopupGetText('Input the address starts with git@', 'Input the address of your github repository')
    if not (text and text.strip()):
        sg.PopupError('address is empty')
        return 
    if text.startswith('git@'):
        return text
    else:
        sg.PopupError('address {0} is not legal'.format(text))


def configure_local_repo_path():
    text = sg.PopupGetFolder('Browse to select the path of your local repository')      
    if not (text and text.strip()):
        sg.PopupError('local path is empty')
        return 
    else:
        return text


def commit_and_push(github_repo, local_repo):
    loading_image = './imgs/loading.gif'
    repo_name = github_repo.split('/')[-1].rstrip('.git')
    repo_dir_path = os.path.join(local_repo, repo_name).replace('\\', '/')
    if not os.path.exists(repo_dir_path):
        command = 'cd {0} && git clone {1}'.format(local_repo, github_repo)
        try:
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF,
                             message = 'Please wait while cloning your github repository\n{0}\nThis will always show on the top until the task finish'.format(github_repo), 
                             background_color='#336699',
                             text_color = 'white',
                             time_between_frames=100)
            subprocess.run(command.split(), shell=True)
            sg.PopupAnimated(None)
            sg.Popup('Successfully cloning the repository {0}'.format(github_repo))
        except:
            sg.PopupError('Failed to clone the repository, make sure\n(1) git is available in your system\n(2)you have privileges to the repository')
            return
    layout = [
        [sg.Text('Choose image file', size=(20, 1)), sg.InputText(), sg.FileBrowse()],
        [sg.Text('Commit message', size=(20, 1)), sg.InputText()],
        [sg.Submit('Commit and Push'), sg.Cancel()]
        ]
    window = sg.Window('Commit and push image')
    event, values = window.Layout(layout).Read()
    window.Close()
    # print(event, values)
    if event == 'Cancel' or event == None:
        return
    # copy image, commit and push
    src_img_path, commit_message = values[0].strip(), values[1].strip()
    if not (src_img_path and commit_message):
        sg.Popup('img path or commit message is empty, try again')
        return
    if src_img_path:
        shutil.copy(src_img_path, repo_dir_path)
    commands = ['cd', repo_dir_path, '&&',
                'git', 'add', '*',  '&&',
                'git', 'commit', '-m',  commit_message, '&&',
                'git', 'push', 'origin', 'master']
    try:
        sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF,
                            message = 'Please wait while commiting and pushing\nThis will always show on the top until the task finish', 
                            background_color='#336699',
                            text_color = 'white',
                            time_between_frames=100)
        subprocess.run(commands, shell=True)
        sg.PopupAnimated(None)
        sg.Popup('Successfully pushing to the repository {0}\nPress OK to get the link of the image'.format(github_repo))
    except:
        sg.Popup('Error occur, try again')
        return
    img_name = src_img_path.split('/')[-1]
    user_name = github_repo.split('/')[0].split(':')[1]
    img_url = 'https://raw.githubusercontent.com/{0}/{1}/master/{2}'.format(user_name, repo_name, urllib.parse.quote(img_name))
    sg.PopupScrolled(img_url)


def pull(github_repo, local_repo):
    commands = 'cd {0} && git pull'.format(local_repo)
    try:
        sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF,
                            message = 'Please wait while pulling from the remote repository {0}\nThis will always show on the top until the task finish'.format(github_repo), 
                            background_color='#336699',
                            text_color = 'white',
                            time_between_frames=100)
        subprocess.run(commands.split(), shell=True)
        sg.PopupAnimated(None)
        sg.Popup('Successfully pulling from the repository {0}'.format(github_repo))
    except:
        sg.Popup('Error occur, try again')
        return


def main():
    github_repo, local_repo = load_configuration()
    layout = [
        [sg.Button('configure_github_repo_address', size=(25, 1)), 
        sg.Text('Your github repository address:', size=(24, 1)), 
        sg.Text(github_repo, key = '__remote_repo__', justification = 'left', text_color = 'red')],      
        [sg.Button('configure_local_repo_path', size=(25, 1)), 
        sg.Text('Your local repository path:', size=(24, 1)), 
        sg.Text(local_repo, key = '__local_repo__', justification = 'left', text_color = 'red')], 
        [sg.Text('_'  * 120)],           
        [sg.Button('commit & push', size=(20, 1)), sg.Button('pull', size=(20, 1))]
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
            if not (github_repo and github_repo.strip() and local_repo and local_repo.strip()):
                sg.Popup('Configure your github_repo_address and local_repo_path fristly')
                continue
            commit_and_push(github_repo, local_repo)
        if event == 'pull':
            pull(github_repo, local_repo)
        if event is None:
            if github_repo != None and local_repo != None:
                save_configuration(github_repo, local_repo)
            break  
    window.Close()


if __name__ == '__main__':
    main()
    