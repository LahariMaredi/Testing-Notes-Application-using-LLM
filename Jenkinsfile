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
                bat 'venv\\Scripts\\python -m pytest -n 4 --alluredir=allure-results --html=report.html --self-contained-html'
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat 'allure generate allure-results -o allure-report --clean'
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'report.html, allure-report/**, screenshots/**, logs/**', fingerprint: true
            }
        }
    }
}
