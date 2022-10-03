pipeline {
    agent { dockerfile true }
    stages {
        stage('Executar Extrator'){
            steps {
                sh 'python main.py'
            }
        }
    }
}