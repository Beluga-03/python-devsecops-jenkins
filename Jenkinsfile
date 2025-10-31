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
        stage('Checkout') {
            steps {
                echo '========== Checking out code from GitHub =========='
                checkout scm
                sh 'ls -la'
                sh 'git branch'
                sh 'git log -1'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '========== Setting up Python virtual environment =========='
                script {
                    sh '''
                        python3 --version
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        python3 --version
                        pip --version
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========== Installing Python dependencies =========='
                script {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install pbr
                        pip install -r requirements.txt
                        echo "Installed packages:"
                        pip list
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo '========== Running pytest tests =========='
                script {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pytest test_app.py -v --junitxml=test-results.xml || true
                    '''
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                echo '========== Running Bandit security scan =========='
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
                echo '========== Checking dependencies with Safety =========='
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

        stage('Build Docker Image') {
            steps {
                echo '========== Building Docker image =========='
                script {
                    sh '''
                        echo "Building Docker image..."
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "Docker images:"
                        docker images | grep ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                echo '========== Scanning Docker image with Trivy =========='
                script {
                    sh '''
                        echo "Scanning image for vulnerabilities..."
                        trivy image --format json --output trivy-report.json ${IMAGE_NAME}:${IMAGE_TAG} || true
                        trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG} || true
                        echo "Trivy scan completed"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo '========== Deploying application =========='
                script {
                    // Stop any existing containers
                    sh 'docker compose down || true'
                    
                    // Deploy the application
                    sh '''
                        echo "Starting application with Docker Compose..."
                        docker compose up -d
                        echo "Waiting for application to be ready..."
                        sleep 10
                        docker compose ps
                    '''
                    
                    // Verify deployment
                    sh '''
                        echo "Verifying application is running..."
                        curl -f http://localhost:5000/health || (echo "Health check failed!" && exit 1)
                        echo "Application deployed successfully!"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo '========== Pipeline Completed =========='
            echo "Build Status: ${currentBuild.result ?: 'SUCCESS'}"
            echo "Build Duration: ${currentBuild.durationString}"
        }
        success {
            echo '========== Pipeline Succeeded =========='
            echo 'All stages completed successfully!'
            echo 'Application is running at: http://localhost:5000'
        }
        failure {
            echo '========== Pipeline Failed =========='
            echo 'Check the logs above for errors'
            // Cleanup on failure
            sh 'docker compose down || true'
        }
        unstable {
            echo '========== Pipeline Unstable =========='
            echo 'Some tests or security checks failed'
        }
    }
}
