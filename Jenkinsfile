pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git 'YOUR_GITHUB_REPO'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-python-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop devops-container || true
                docker rm devops-container || true
                docker run -d -p 5001:5000 --name devops-container devops-python-app
                '''
            }
        }
    }
}