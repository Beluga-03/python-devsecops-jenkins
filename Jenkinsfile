pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Beluga-03/python-devsecops-jenkins.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-devsecops-app .'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'pytest > result.log || true'
                archiveArtifacts artifacts: 'result.log', allowEmptyArchive: true
            }
        }

        stage('Static Analysis (Bandit)') {
            steps {
                sh 'bandit -r . || true'
            }
        }

        stage('Dependency Scan (Safety)') {
            steps {
                sh 'safety check || true'
            }
        }

        stage('Image Scan (Trivy)') {
            steps {
                sh 'trivy image flask-devsecops-app || true'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker-compose up -d || true'
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished ✅'
        }
    }
}
