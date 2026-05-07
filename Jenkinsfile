pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/LahariMaredi/Notes-Testing-App.git'
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
                bat 'venv\\Scripts\\activate && pytest -n 4 --alluredir=allure-results --html=report.html --self-contained-html'
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
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
