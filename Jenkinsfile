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
            def buildUser = env.BUILD_USER ?: "Unknown"

            // الحالة ولون الرسالة
            def slackColor = currentBuild.currentResult == 'SUCCESS' ? 'good' : 'danger'
            def statusEmoji = currentBuild.currentResult == 'SUCCESS' ? '✅' : '❌'

            // Slack Notification باستخدام curl
            def payload = """
            {
              "channel": "#jenkins-notification",
              "text": "${statusEmoji} Build ${currentBuild.currentResult} for ${env.JOB_NAME} #${env.BUILD_NUMBER}\nTriggered by: ${buildUser}\nLast commit: ${lastCommit}"
            }
            """

            sh "curl -X POST -H 'Content-type: application/json' --data '${payload}' ${SLACK_WEBHOOK_URL}"
        }
    }
}
}