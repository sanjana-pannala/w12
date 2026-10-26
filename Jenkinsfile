
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
                bat 'docker login -u sanjana26122005 -p Sanjana@12'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying application to Kubernetes'
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
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
