
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sailaya/student-record-system:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Check') {
            steps {
                bat '"C:\\Users\\megav\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
                bat '"C:\\Users\\megav\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m py_compile app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'docker logout >NUL 2>&1'
                    bat 'powershell -NoProfile -NonInteractive -Command "$env:DOCKERHUB_TOKEN | docker login --username $env:DOCKERHUB_USER --password-stdin"'
                    bat 'docker push %DOCKER_IMAGE%'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withEnv(['KUBECONFIG=C:\\Users\\megav\\.kube\\config']) {
                    bat 'kubectl config current-context'
                    bat 'kubectl get nodes'
                    bat 'kubectl apply -f deployment.yaml'
                    bat 'kubectl apply -f service.yaml'
                    bat 'kubectl rollout status deployment/student-record-deployment --timeout=120s'
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
