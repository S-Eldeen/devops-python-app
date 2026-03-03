pipeline {
    agent any
    environment {
        SLACK_WEBHOOK_URL = credentials('slack-webhook') // خزنه كـ Secret Text في Jenkins
    }
    stages {

        stage('Clean Workspace') {
            steps { deleteDir() }
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
        always {
            script {
                // آخر commit
                def lastCommit = sh(
                    returnStdout: true,
                    script: "git log -1 --pretty=format:'%h by %an on %cd' --date=short"
                ).trim()

                // مين عمل Build
                def buildUser = ''
                def causes = currentBuild.rawBuild.getCauses()
                for (cause in causes) {
                    buildUser += cause.shortDescription + "\n"
                }

                // Slack Notification
                def slackColor = currentBuild.currentResult == 'SUCCESS' ? 'good' : 'danger'
                def statusEmoji = currentBuild.currentResult == 'SUCCESS' ? '✅' : '❌'

                slackSend(
                    webhookUrl: env.SLACK_WEBHOOK_URL,
                    channel: '#devops-alerts',
                    color: slackColor,
                    message: "${statusEmoji} Build ${currentBuild.currentResult} for ${env.JOB_NAME} #${env.BUILD_NUMBER}\n" +
                             "Triggered by:\n${buildUser}\n" +
                             "Last commit: ${lastCommit}"
                )
            }
        }
    }
}