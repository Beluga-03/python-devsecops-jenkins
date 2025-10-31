pipeline {
    agent any

    environment {
        // Docker image configuration
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        IMAGE_TAG = 'latest'
        // Python virtual environment
        VENV_DIR = 'venv'
    }

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


        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        echo "Running Bandit security analysis..."
                        bandit -r . -f json -o bandit-report.json || true
                        bandit -r . -ll || true
                        echo "Bandit scan completed"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }


        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        echo "Checking for vulnerable dependencies..."
                        safety check --json > safety-report.json || true
                        safety check || true
                        echo "Safety check completed"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'safety-report.json', allowEmptyArchive: true
                }
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
