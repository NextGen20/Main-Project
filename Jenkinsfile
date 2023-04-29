
pipeline {
    agent any

    stages {
        stage('Install Docker') {
            steps {
                sh 'curl -fsSL https://get.docker.com -o get-docker.sh'
            }
        }

        stage('Git Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/NextGen20/Main-Project.git'
            }
        }

        stage('Build & Run Image') {
            steps {
                sh 'docker build -t flaskproject/myproject:latest .'
                sh 'docker run --name flaskapp1 -d -p 5000:5000 flaskproject/myproject:latest'
            }
        }
    }

    post {
        always {
            sh 'sudo docker stop $(sudo docker ps -aq)'
            sh 'sudo docker rm $(sudo docker ps -aq)'
        }
    }
}
