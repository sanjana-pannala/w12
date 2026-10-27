
pipeline {
    agent any

    stages {

        stage('Install Dependencies and Run Selenium Tests') {
            steps {
                echo 'Installing Python dependencies'
                bat 'python -m pip install -r requirements.txt'

                echo 'Starting Flask application'
                bat 'start /B python app.py'

                echo 'Waiting for Flask application to start'
                bat 'ping 127.0.0.1 -n 6 > nul'

                echo 'Running pytest'
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat 'docker build -t sanjana26122005/mysecondapp:seleniumtestimage .'
            }
        }

        stage('Docker Login and Push') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'dockerhub-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_TOKEN'
        )]) {
            bat 'docker login -u %DOCKER_USER% --password-stdin < nul'
        }
    }
}

        stage('Check Kubernetes') {
            steps {
                echo 'Checking Jenkins Windows account'
                bat 'whoami'

                echo 'Checking Kubernetes context'
                bat 'kubectl config current-context'

                echo 'Checking deployment permissions'
                bat 'kubectl auth can-i create deployments'

                echo 'Checking Kubernetes nodes'
                bat 'kubectl get nodes'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying application to Kubernetes'
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml --validate=false'
                bat 'kubectl rollout status deployment/kubedemoapp-deployment --timeout=120s'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the console logs.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}
