pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "devops-python-app:latest"
        SLACK_CHANNEL = "#devops-alerts"
        SLACK_CREDENTIALS = "slack-webhook"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code from GitHub..."
                git url: 'https://github.com/S-Eldeen/devops-python-app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                echo "Stopping old container if running..."
                script {
                    sh """
                    if [ \$(docker ps -q -f name=python-app-container) ]; then
                        docker stop python-app-container
                        docker rm python-app-container
                    fi
                    """
                }
            }
        }

        stage('Run New Container') {
            steps {
                echo "Starting new container..."
                script {
                    sh "docker run -d --name python-app-container -p 8080:8080 ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Notify Slack') {
            steps {
                echo "Sending deployment notification to Slack..."
                slackSend(channel: "${SLACK_CHANNEL}", 
                          color: "good", 
                          message: "✅ Python app deployed successfully with image ${DOCKER_IMAGE}", 
                          teamDomain: "your-team-domain", 
                          tokenCredentialId: "${SLACK_CREDENTIALS}")
            }
        }
    }

    post {
        failure {
            slackSend(channel: "${SLACK_CHANNEL}", 
                      color: "danger", 
                      message: "❌ Deployment failed!", 
                      teamDomain: "your-team-domain", 
                      tokenCredentialId: "${SLACK_CREDENTIALS}")
        }
    }
}