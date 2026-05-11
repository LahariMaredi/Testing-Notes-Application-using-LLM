pipeline {
    agent any

    environment {
        // Inject GROQ_API_KEY from Jenkins Credentials
        GROQ_API_KEY = credentials('GROQ_API_KEY')
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/LahariMaredi/Testing-Notes-Application-using-LLM.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests (Parallel)') {
            steps {
                // GROQ_API_KEY is automatically passed as environment variable
                bat 'venv\\Scripts\\python -m pytest -n 4 --alluredir=allure-results --html=report.html --self-contained-html'
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML(target: [
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'report.html, allure-results/**, screenshots/**, logs/**', fingerprint: true
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html, allure-results/**', allowEmptyArchive: true
        }
    }
}