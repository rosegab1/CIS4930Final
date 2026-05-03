pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker compose up --build -d'
                }
            }
        }

        stage('Verify') {
            steps {
                echo "Verifying..."
            }
        }

        stage('Deploy') {
            steps {
                echo "Testing..."
            }
        }
    }
}