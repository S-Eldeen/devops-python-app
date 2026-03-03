pipeline {
    agent any
    environment {
        SLACK_WEBHOOK_URL = credentials('slack-webhook') // خزنه كـ Secret Text في Jenkins
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
                sh 'docker build --no-cache -t devops-python-app .'
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

    post {
        success {
            script {
                def lastCommit = sh(
                    returnStdout: true,
                    script: "git log -1 --pretty=format:'%h by %an on %ad'"
                ).trim()

                slackSend(
                    channel: '#devops-alerts',
                    color: 'good',
                    message: "✅ Build SUCCESS for ${env.JOB_NAME} #${env.BUILD_NUMBER}\nLast commit: ${lastCommit}"
                )
            }
        }
        failure {
            script {
                def lastCommit = sh(
                    returnStdout: true,
                    script: "git log -1 --pretty=format:'%h by %an on %ad'"
                ).trim()

                slackSend(
                    channel: '#devops-alerts',
                    color: 'danger',
                    message: "❌ Build FAILED for ${env.JOB_NAME} #${env.BUILD_NUMBER}\nLast commit: ${lastCommit}"
                )
            }
        }
    }
}