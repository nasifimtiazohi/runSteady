import os, sys
import subprocess, shlex
def get_projects():
    projectPaths=[]
    path='/Users/nasifimtiaz/Desktop/openmrsCopyRepos'
    os.chdir(path)
    lines = subprocess.check_output(shlex.split('ls'), encoding='437').split('\n')[:-1]
    for line in lines:
        if line=='openmrs-owa-sysadmin':
            continue
        projectPaths.append(path+'/'+line+'/')
        
    return projectPaths 
if __name__=='__main__':
    projects = get_projects()
    
    for project in projects:
        print(project)
        os.chdir(project)
        os.system('git pull')
        os.system('git add .')
        os.system('git commit -m "adding vulas profile"')
        os.system('git push')