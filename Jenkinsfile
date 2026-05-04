pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build/Deploy') {
            steps {
                script {
                    sh 'docker-compose up --build -d'
                }
            }
        }

        stage('Verify') {
            steps {
                sh "curl -f http://localhost:5001"
            }
        }

    }
}
