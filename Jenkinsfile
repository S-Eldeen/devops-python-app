pipeline {

agent any

environment {

SLACK_WEBHOOK_URL = credentials('slack-webhook')

VERSION = "${env.BUILD_NUMBER}"

APP_NAME = "devops-python-app"

}

stages {

stage('Clean Workspace') {

steps {

deleteDir()

}

}

stage('Checkout Code') {

steps {

git branch: 'main',

url: 'https://github.com/S-Eldeen/devops-python-app.git'

}

}

stage('Build Docker Image') {

steps {

sh '''

docker build --no-cache -t ${APP_NAME}:${VERSION} .

docker tag ${APP_NAME}:${VERSION} ${APP_NAME}:latest

'''

}

}

stage('Prepare Kubernetes Deployment') {

steps {

sh '''

sed 's/VERSION/'${VERSION}'/g' deployment.yaml > deployment-final.yaml

'''

}

}

stage('Deploy to Kubernetes') {

steps {

sh '''

kubectl apply -f deployment-final.yaml || kubectl create -f deployment-final.yaml

kubectl apply -f service.yaml

kubectl rollout restart deployment/${APP_NAME}

kubectl rollout status deployment/${APP_NAME}

'''

}

}

stage('Health Check') {

steps {

sh '''

kubectl get pods

kubectl get svc

kubectl rollout history deployment/${APP_NAME}

'''

}

}

}

post {

success {

script {

def lastCommit = sh(

returnStdout: true,

script: "git log -1 --pretty=format:'%h by %an on %cd' --date=short"

).trim()

def payload = """

{

"attachments":[

{

"color":"#36a64f",

"title":"✅ Build SUCCESS ${env.JOB_NAME} #${VERSION}",

"text":"Version: ${VERSION}\\nCommit: ${lastCommit}\\nURL: ${env.BUILD_URL}"

}

]

}

"""

writeFile file: 'slack.json', text: payload

sh """

curl -X POST -H 'Content-type: application/json' \

--data @slack.json \

${SLACK_WEBHOOK_URL}

"""

}

}

failure {

script {

def payload = """

{

"attachments":[

{

"color":"#ff0000",

"title":"❌ Build FAILED ${env.JOB_NAME}",

"text":"URL: ${env.BUILD_URL}"

}

]

}

"""

writeFile file: 'slack.json', text: payload

sh """

curl -X POST -H 'Content-type: application/json' \

--data @slack.json \

${SLACK_WEBHOOK_URL}

"""

}

}

}

}