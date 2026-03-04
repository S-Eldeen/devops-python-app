pipeline {
    agent any
    
    environment {
        // تأكد من وجود الـ Credentials دي في Jenkins كـ Secret Text
        SLACK_WEBHOOK_URL = credentials('slack-webhook') 
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
        always {
            script {
                // 1. جلب بيانات آخر Commit
                def lastCommit = sh(
                    returnStdout: true,
                    script: "git log -1 --pretty=format:'%h by %an on %cd' --date=short"
                ).trim()

                // 2. تحديد سبب الـ Build (Manual vs GitHub)
                def causes = currentBuild.getBuildCauses()
                def buildTrigger = "Automated/Other"

                if (causes.toString().contains('UserIdCause')) {
                    buildTrigger = "Jenkins Build Now (Manual)"
                } else if (causes.toString().contains('GitHubPushCause') || causes.toString().contains('SCMTriggerCause')) {
                    buildTrigger = "GitHub Push"
                }

                // 3. تحديد حالة الـ Build والألوان لـ Slack
                def statusEmoji = currentBuild.currentResult == 'SUCCESS' ? '✅' : '❌'
                def slackColor = currentBuild.currentResult == 'SUCCESS' ? '#36a64f' : '#ff0000'

                // 4. تجهيز الـ Payload (استخدام attachments لشكل احترافي)
                def payload = """
                {
                  "channel": "#jenkins-notification",
                  "attachments": [
                    {
                      "color": "${slackColor}",
                      "title": "${statusEmoji} Build ${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                      "text": "*Triggered by:* ${buildTrigger}\\n*Last Commit:* ${lastCommit}\\n*Build URL:* ${env.BUILD_URL}",
                      "mrkdwn_in": ["text"]
                    }
                  ]
                }
                """

                // 5. إرسال الإشعار عن طريق ملف مؤقت لتجنب مشاكل الـ Shell Quotes
                writeFile file: 'slack_payload.json', text: payload
                sh "curl -X POST -H 'Content-type: application/json' --data @slack_payload.json ${SLACK_WEBHOOK_URL}"
                
                // مسح الملف المؤقت بعد الإرسال
                sh "rm slack_payload.json"
            }
        }
    }
}