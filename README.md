# Python DevSecOps Jenkins Pipeline

A Flask application with integrated DevSecOps practices using Jenkins CI/CD.

## Features
- Flask REST API
- Automated testing with pytest
- Security scanning with Bandit, Trivy, and Safety
- Docker containerization
- Jenkins CI/CD pipeline
- Continuous deployment

## Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run application
python app.py
```

## Security Tools
- **Bandit**: Static code analysis
- **Trivy**: Container vulnerability scanning
- **Safety**: Dependency vulnerability checking

## Pipeline Stages
1. Checkout code from GitHub
2. Setup Python environment
3. Install dependencies
4. Run tests
5. Static code analysis (Bandit)
6. Check dependency vulnerabilities (Safety)
7. Build Docker image
8. Container vulnerability scan (Trivy)
9. Deploy application

## Access Application
- Application: http://localhost:5000
- Health Check: http://localhost:5000/health
- Tasks API: http://localhost:5000/tasks
