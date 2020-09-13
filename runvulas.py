import os
import subprocess, shlex
from datetime import datetime

def get_projects():
    projectPaths=[]
    path = '/home/simtiaz/openmrsCopyRepos'
    os.chdir(path)
    
    lines = subprocess.check_output(shlex.split('ls'), encoding='437').split('\n')[:-1]
    for line in lines:
        projectPaths.append(path+'/'+line)
    
    assert len(projectPaths) == 43
    return projectPaths 

    

def run(path):
    project= path.split('/')[-1]
    print("project name is", project, path)
    
    commands=[
        'mvn -Dvulas vulas:cleanSpace',
        'mvn -Dvulas compile vulas:app',
        'export MAVEN_OPTS="-Xmx8g -Xms2g"',
        'mvn -Dvulas compile vulas:a2c',
        'mvn -Dvulas vulas:prepare-vulas-agent test vulas:upload -Dmaven.test.failure.ignore=true',
        'mvn package',
        'mvn -Dvulas vulas:instr',
        'mvn -Dvulas vulas:t2c',
        'mvn -Dvulas vulas:upload',
        'mvn -Dvulas vulas:report'
    ]
    
    os.chdir(path)
    
    file = open('{}log.txt'.format(project),'w+')
    
    start = datetime.now()
    file.write(datetime.now())
    for c in commands:
        os.system(c)
        file.write(datetime.now())
    end=datetime.now()
    file.write(end-start)
    
    os.system('mv ./target/vulas/report/vulas-report.json /home/simtiaz/runSteady/{}-vulas.json'.format(project))

    file.close()
if __name__=='__main__':
    paths = get_projects()
    for path in paths:
        run(path)
        break
