pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Executar'){
            steps {
                sh 'python main.py'
            }
        }
    }
}