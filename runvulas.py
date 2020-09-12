import os

os.chdir('/home/nasifimtiaz/Desktop/openmrs-module-fhir-1.20.0')


from datetime import datetime

start = datetime.now()

commands=[
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

for c in commands:
	os.system(c)

end=datetime.now()

print(start, end, start-end)
