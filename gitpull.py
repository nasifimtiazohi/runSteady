import sys, os
from lxml import etree as ET
import pandas as pd
import time


def readPom(file):
    pom = ET.parse(file)
    items= pom.find('//{http://maven.apache.org/POM/4.0.0}properties')
    items=items[1:]
    hm={}
    for idx, item in enumerate(items):
        if item.tag is ET.Comment:
            continue
    
        artifact= item.tag.replace('{http://maven.apache.org/POM/4.0.0}','').replace('Version','').strip().lower()
        hm[artifact]={}
        version=item.text.strip()
        if artifact == 'openmrs':
            group='org.openmrs'
            repoName='openmrs-core'
        elif artifact == 'event':
            group='org.openmrs'
            repoName='openmrs-module-'+artifact
        elif artifact == 'uitestframework':
            group='org.openmrs.contrib'
            repoName='openmrs-contrib-'+artifact
        elif artifact == 'sysadmin':
            group = 'npm'
            repoName = 'openmrs-owa-'+artifact
        else:
            group='org.openmrs.module'
            repoName='openmrs-module-'+artifact
        
        hm[artifact]['version']=version
        hm[artifact]['group']=group
        hm[artifact]['repo']=repoName

    return hm
def getRepoReleaseMapping():
    projects = readPom('/Users/nasifimtiaz/Desktop/vulnerable-dependency-detection-comparison/distro_information/pom.xml')
    hm={}
    
    for k  in projects.keys():
        repo = projects[k]['repo']
        release = projects[k]['version']
        hm[repo]=release
        
    assert len(projects) == len(hm)
    return hm

if __name__=='__main__':
    os.chdir('/home/simtiaz/openmrsCopyRepos')
    hm=getRepoReleaseMapping()
    for repo in hm.keys():
        if repo=='openmrs-owa-sysadmin':
            continue
        release=hm[repo]
        repoName= repo+'-'+release
        os.system('git clone https://github.com/nasifimtiazohi/{}.git'.format(repoName))
        