pipeline {
    agent any

    environment {
        // اسم الصورة الخاصة بك على دكر هاب
        DOCKER_IMAGE = "seifeldeen/jenkins:python-app"
    }

    stages {
        stage('Clone Repo') {
            steps {
                // جينكنز يقوم بعمل كلوون تلقائياً، لكن لا بأس من تأكيد الفرع
                git branch: 'main', url: 'https://github.com/S-Eldeen/devops-python-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // بناء الصورة محلياً داخل جينكنز
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // ستحتاج لإضافة Credentials في جينكنز باسم docker-hub-creds
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop devops-container || true
                docker rm devops-container || true
                docker run -d -p 5001:5000 --name devops-container ${DOCKER_IMAGE}
                '''
            }
        }
    }
}