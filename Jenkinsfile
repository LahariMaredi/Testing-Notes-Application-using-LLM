pipeline {
agent any
environment {
    GROQ_API_KEY = credentials('GROQ_API_KEY')
}

stages {

    stage('Checkout Code') {
        steps {
            git branch: 'main',
                url: 'https://github.com/LahariMaredi/Testing-Notes-Application-using-LLM.git'
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
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }
    }

    stage('Archive AI Analysis') {
        steps {
            archiveArtifacts(
                artifacts: 'reports/**/*.md',
                fingerprint: true,
                allowEmptyArchive: true
            )
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
            archiveArtifacts(
                artifacts: 'report.html,allure-results/**,allure-report/**,reports/**,screenshots/**,logs/**',
                fingerprint: true,
                allowEmptyArchive: true
            )
        }
    }
}

post {
    always {
        archiveArtifacts(
            artifacts: 'report.html,allure-results/**,allure-report/**,reports/**',
            allowEmptyArchive: true
        )
    }

    success {
        echo 'Build completed successfully.'
    }

    failure {
        echo 'Build failed. Check AI Failure Analysis reports.'
    }
}

}
