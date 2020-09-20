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

def get_processed_projects():
    paths=[]
    path='/home/simtiaz/runSteady/reports'
    os.chdir(path)
    
    hs=set()
    
    lines = subprocess.check_output(shlex.split('ls'), encoding='437').split('\n')[:-1]
    
    for line in lines:
        s = '-log.txt'
        if line.endswith(s):
           project = line[:-len(s)]
           hs.add(project)
        
        s = '-vulas.json'
        if line.endswith(s):
           project = line[:-len(s)]
           hs.add(project)
    
    return hs

def run(path):
    project= path.split('/')[-1]
    print("processing ", project, path)
    
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
    
    logfileName= '{}-log.txt'.format(project)
    file = open(logfileName,'w+')
    
    start = datetime.now()
    file.write(str(datetime.now())+'\n')
    print(start)

    for c in commands:
        os.system(c)
        #os.system(c + ' > /dev/null 2>&1')
        file.write(str(datetime.now())+'\n')
        print(c, "has ended")
    
    end=datetime.now()
    file.write(str(end-start))
    print(end)
    
    os.system('mv ./target/vulas/report/vulas-report.json /home/simtiaz/runSteady/reports/{}-vulas.json'.format(project))
    file.close()
    os.system('mv ./{} /home/simtiaz/runSteady/reports/{}'.format(logfileName, logfileName))
    
if __name__=='__main__':
    paths = get_projects()
    processed_projects= get_processed_projects()
        
    for path in paths:
        name = path.split('/')[-1]
        print(name,path)
        if name in processed_projects:
            print(name, ' already processed')
            continue
        if 'openmrs-module-coreapps' in name or 'openmrs-module-emrapi' in name:
            print('skipping coreapps as too big in RAM')
            continue

        run(path)
    
