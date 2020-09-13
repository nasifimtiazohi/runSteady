import os, sys
import subprocess, shlex
import xml.etree.ElementTree as ET 
ET.register_namespace('',"http://maven.apache.org/POM/4.0.0")
ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")


fullProfile = ET.fromstring('''<profiles>
	<profile>
        <id>vulas</id>
        <activation>
            <property>
                <name>vulas</name>
            </property>
        </activation>
        <properties>
            <vulas.version>3.1.10-SNAPSHOT</vulas.version>
            <vulas.shared.backend.serviceUrl>http://localhost:8033/backend/</vulas.shared.backend.serviceUrl>
            <vulas.core.space.token>9237B647D37B9176837CB401EE2922F6</vulas.core.space.token>
            <vulas.core.appContext.group>${project.groupId}</vulas.core.appContext.group>
            <vulas.core.appContext.artifact>${project.artifactId}</vulas.core.appContext.artifact>
            <vulas.core.appContext.version>${project.version}</vulas.core.appContext.version>
        </properties>
        <build>
            <plugins>
                <plugin>
                    <groupId>com.sap.research.security.vulas</groupId>
                    <artifactId>plugin-maven</artifactId>
                    <version>${vulas.version}</version>
                    <configuration>
                        <layeredConfiguration>
                            <vulas.shared.backend.serviceUrl>${vulas.shared.backend.serviceUrl}</vulas.shared.backend.serviceUrl>
                            <vulas.core.space.token>${vulas.core.space.token}</vulas.core.space.token>

                            <vulas.core.appContext.group>${vulas.core.appContext.group}</vulas.core.appContext.group>
                            <vulas.core.appContext.artifact>${vulas.core.appContext.artifact}</vulas.core.appContext.artifact>
                            <vulas.core.appContext.version>${vulas.core.appContext.version}</vulas.core.appContext.version>

                            <vulas.shared.tmpDir>${project.build.directory}/vulas/tmp</vulas.shared.tmpDir>
                            <vulas.core.uploadDir>${project.build.directory}/vulas/upload</vulas.core.uploadDir>
                            <vulas.core.app.sourceDir>${project.build.directory}/classes,${project.basedir}/src/main/java,${project.basedir}/src/main/python</vulas.core.app.sourceDir>

                            <!-- vulas:instr : Instruments JAR/WAR files found in source dir,
                                and writes to target dir. Files in include dir are put into /WEB-INF/lib
                                of output WARs. Files in lib dir are part of the class path when instrumenting. -->
                            <vulas.core.instr.sourceDir>${project.build.directory}</vulas.core.instr.sourceDir>
                            <vulas.core.instr.targetDir>${project.build.directory}/vulas/target</vulas.core.instr.targetDir>
                            <vulas.core.instr.includeDir>${project.build.directory}/vulas/include</vulas.core.instr.includeDir>
                            <vulas.core.instr.libDir>${project.build.directory}/vulas/lib</vulas.core.instr.libDir>
                            <vulas.core.instr.writeCode>false</vulas.core.instr.writeCode>
                            <vulas.core.instr.instrumentorsChoosen>com.sap.psr.vulas.monitor.trace.SingleTraceInstrumentor</vulas.core.instr.instrumentorsChoosen>
                            <vulas.core.instr.searchRecursive>false</vulas.core.instr.searchRecursive>
                            <vulas.core.monitor.periodicUpload.enabled>false</vulas.core.monitor.periodicUpload.enabled>
                            <vulas.core.instr.maxStacktraces>10</vulas.core.instr.maxStacktraces>

                            <!-- vulas:a2c/t2c : Performs static call graph analysis -->
                            <vulas.reach.wala.callgraph.reflection>NO_FLOW_TO_CASTS_NO_METHOD_INVOKE</vulas.reach.wala.callgraph.reflection>
                            <vulas.reach.timeout>60</vulas.reach.timeout>

                            <!-- vulas:report -->
                            <vulas.report.exceptionExcludeBugs></vulas.report.exceptionExcludeBugs>
                            <vulas.report.reportDir>${project.build.directory}/vulas/report</vulas.report.reportDir>
                        </layeredConfiguration>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
    </profiles>''')
singleProfile=ET.fromstring('''<profile>
        <id>vulas</id>
        <activation>
            <property>
                <name>vulas</name>
            </property>
        </activation>
        <properties>
            <vulas.version>3.1.10-SNAPSHOT</vulas.version>
            <vulas.shared.backend.serviceUrl>http://localhost:8033/backend/</vulas.shared.backend.serviceUrl>
            <vulas.core.space.token>9237B647D37B9176837CB401EE2922F6</vulas.core.space.token>
            <vulas.core.appContext.group>${project.groupId}</vulas.core.appContext.group>
            <vulas.core.appContext.artifact>${project.artifactId}</vulas.core.appContext.artifact>
            <vulas.core.appContext.version>${project.version}</vulas.core.appContext.version>
        </properties>
        <build>
            <plugins>
                <plugin>
                    <groupId>com.sap.research.security.vulas</groupId>
                    <artifactId>plugin-maven</artifactId>
                    <version>${vulas.version}</version>
                    <configuration>
                        <layeredConfiguration>
                            <vulas.shared.backend.serviceUrl>${vulas.shared.backend.serviceUrl}</vulas.shared.backend.serviceUrl>
                            <vulas.core.space.token>${vulas.core.space.token}</vulas.core.space.token>

                            <vulas.core.appContext.group>${vulas.core.appContext.group}</vulas.core.appContext.group>
                            <vulas.core.appContext.artifact>${vulas.core.appContext.artifact}</vulas.core.appContext.artifact>
                            <vulas.core.appContext.version>${vulas.core.appContext.version}</vulas.core.appContext.version>

                            <vulas.shared.tmpDir>${project.build.directory}/vulas/tmp</vulas.shared.tmpDir>
                            <vulas.core.uploadDir>${project.build.directory}/vulas/upload</vulas.core.uploadDir>
                            <vulas.core.app.sourceDir>${project.build.directory}/classes,${project.basedir}/src/main/java,${project.basedir}/src/main/python</vulas.core.app.sourceDir>

                            <!-- vulas:instr : Instruments JAR/WAR files found in source dir,
                                and writes to target dir. Files in include dir are put into /WEB-INF/lib
                                of output WARs. Files in lib dir are part of the class path when instrumenting. -->
                            <vulas.core.instr.sourceDir>${project.build.directory}</vulas.core.instr.sourceDir>
                            <vulas.core.instr.targetDir>${project.build.directory}/vulas/target</vulas.core.instr.targetDir>
                            <vulas.core.instr.includeDir>${project.build.directory}/vulas/include</vulas.core.instr.includeDir>
                            <vulas.core.instr.libDir>${project.build.directory}/vulas/lib</vulas.core.instr.libDir>
                            <vulas.core.instr.writeCode>false</vulas.core.instr.writeCode>
                            <vulas.core.instr.instrumentorsChoosen>com.sap.psr.vulas.monitor.trace.SingleTraceInstrumentor</vulas.core.instr.instrumentorsChoosen>
                            <vulas.core.instr.searchRecursive>false</vulas.core.instr.searchRecursive>
                            <vulas.core.monitor.periodicUpload.enabled>false</vulas.core.monitor.periodicUpload.enabled>
                            <vulas.core.instr.maxStacktraces>10</vulas.core.instr.maxStacktraces>

                            <!-- vulas:a2c/t2c : Performs static call graph analysis -->
                            <vulas.reach.wala.callgraph.reflection>NO_FLOW_TO_CASTS_NO_METHOD_INVOKE</vulas.reach.wala.callgraph.reflection>
                            <vulas.reach.timeout>60</vulas.reach.timeout>

                            <!-- vulas:report -->
                            <vulas.report.exceptionExcludeBugs></vulas.report.exceptionExcludeBugs>
                            <vulas.report.reportDir>${project.build.directory}/vulas/report</vulas.report.reportDir>
                        </layeredConfiguration>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>''')
def get_projects():
    projectPaths=[]
    path='/Users/nasifimtiaz/Desktop/openmrsCopyRepos'
    os.chdir(path)
    lines = subprocess.check_output(shlex.split('ls'), encoding='437').split('\n')[:-1]
    for line in lines:
        if line=='openmrs-owa-sysadmin':
            continue
        projectPaths.append(path+'/'+line)
        
    return projectPaths 

def getProfiles(root):
    p = None
    for n in list(root):
        if 'profiles' in n.tag:
            p=n
            break
    return p


def checkIfProfileExists(profiles):
    for n in list(profiles):
        for i in list(n):
            if i.tag=='{http://maven.apache.org/POM/4.0.0}id' and i.text=='vulas':
                return True
    return False

if __name__=='__main__':
    projects = get_projects()
    
    for project in projects:
        file=project+'/pom.xml'
        print(file)
        tree= ET.parse(file)
        root = tree.getroot()
        profiles = getProfiles(root)
        if not profiles:
            root.append(fullProfile)
        else:
            if not checkIfProfileExists(profiles):
                profiles.append(singleProfile)
        tree.write(file)    
        