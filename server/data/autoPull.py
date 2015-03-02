#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'andycall'

import subprocess, os, logging, time, data

responsitories = data.responsitories


def pathConver(responsitories):
    paths = {}
    for repo in responsitories:
        repo = unicode(repo, 'utf-8')
        path = repo.split('/')[-1]
        name = repo.split('??')[0]
        responsitoriy = repo.split("??")[-1]                
        if len(name) > 0 and len(responsitoriy) > 0 :
            if (path.endswith('.git')):
                path = path.rsplit('.git')[0]
            paths[name] = []
            paths[name].append(path)      
            paths[name].append(responsitoriy)
    
    return paths


def checkIfGit(str):
    if '.git' in str and os.path.isdir(str):
        return True
    else:
        return False


# def find(path):
# if not os.path.exists(path):
#         return

#     dir_list = os.listdir(path)

#     for dir in dir_list:
#         new_path = os.path.join(path, dir)
#         if(checkIfGit(new_path)):
#             paths.append(new_path.replace('/.git', ''))
#         else:
#             if os.path.isdir(new_path):
#                 find(new_path)

def RunPull(paths):
    now_path = os.path.abspath('.')
    log_path = os.path.join(now_path, 'log')
    now_time = unicode(time.strftime('%Y-%m-%d %H:%m', time.localtime(time.time())), 'ascii')
    
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    
    with open(os.path.join(log_path, 'error.log'), 'a') as f:
        f.write('--------------- ' + now_time + ' ----------------\n')
    
    for folder in paths:
        i = os.path.join(now_path.decode('utf-8'), (folder + '-' + paths[folder][0]))
        responsitory = paths[folder][1]
        name = folder
        try:
            os.chdir(i)
            now_branch = subprocess.check_output(['git', 'branch']).split(' ')[-1].strip('\n') or 'master'
            now_origin = subprocess.check_output(['git', 'remote']).strip('\n') or 'origin'
            print 'git is going to pull ' + responsitory
            output = subprocess.check_output(['git', 'pull', now_origin, now_branch])
            with open(os.path.join(log_path.decode('utf-8'), u'{name}.log'.format(name=name)), 'a') as f:
                f.write("---------- " +
                        now_time.encode('utf-8') +
                        ' ' +
                        name.encode('utf-8') +
                        ' ------------\n' +
                        output.encode('utf-8') +
                        '\n')
        except subprocess.CalledProcessError, e:
            logging.exception(e)
            with open(os.path.join(now_path, 'log/error.log'), 'a') as f:
                f.write("Failed :" + name.encode('utf-8') + '\n')

def initGit(paths):
    for folder in paths:
        p = os.path.join(now_path.decode('utf-8'), (folder + '-' + paths[folder][0]))
        if not os.path.exists(p):
            os.mkdir(p)
            os.chdir(p)
            subprocess.call(["git", "init"])
            subprocess.call(["git", "remote", "add", "origin", paths[folder][1]])

if __name__ == "__main__":
    now_path = os.path.abspath(".")
    paths = pathConver(responsitories)
    initGit(paths)
    os.chdir(now_path)
    RunPull(paths)
