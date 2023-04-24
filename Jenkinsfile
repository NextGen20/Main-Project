/* groovylint-disable UnusedVariable */
/* groovylint-disable-next-line CompileStatic */
pipeline {
    agent any
    // agent { label 'slave1' }
    // environment {
    //     /* groovylint-disable-next-line NoDef, VariableName */
    //     def DATE = sh(script: 'echo `date`', returnStdout: true).trim()
    // }

    stages {
        stage('Git_Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/NextGen20/Main-Project.git'
            }
        }
                stage('Build & Run image') {
                    steps {
                sh 'sudo docker build -t flaskproject/myproject:latest .'
                sh 'sudo docker run --name flaskapp1 -d -p 5000:5000 flaskproject/myproject:latest'
                    }
                }
    }
}
//         stage('Unitest & DynamoDB') {
//             steps {
//                 script {
//                     /* groovylint-disable-next-line LineLength */
//                     STATUS_HTTP = sh(script: "curl -I \$(dig +short myip.opendns.com @resolver1.opendns.com):5000 | grep \"HTTP/1.1 200 OK\" | tr -d \"\\r\\n\"", returnStdout: true).trim()
//                     sh 'echo "$STATUS_HTTP" >> result.json'
//                     /* groovylint-disable-next-line LineLength */
//                     STATUS_NAME = sh(script: "curl -v \$(dig +short myip.opendns.com @resolver1.opendns.com):5000 | grep \"hello Bachar\" | tr -d \"\\r\\n\"", returnStdout: true).trim()
//                     sh 'echo "$STATUS_NAME" >> result.json'
//                     sh 'echo "$DATE" >> result.json'
//                     /* groovylint-disable-next-line NestedBlockDepth */
//                     withAWS(credentials: 'aws-key', region: 'us-east-1') {
//                         /* groovylint-disable-next-line LineLength */
//                         sh "aws dynamodb put-item --table-name result --item '{\"User\": {\"S\": \"${BUILD_USER_ID}\"}, \"Date\": {\"S\": \"${DATE}\"}, \"TEST_RESULT\": {\"S\": \"${STATUS_HTTP}\"}, \"TEST_NAME\": {\"S\": \"${STATUS_NAME}\"}}'"
//                     }
//                 }
//             }
//         }
//         stage('Aws_S3_Upload') {
//             steps {
//                 /* groovylint-disable-next-line DuplicateMapLiteral, DuplicateStringLiteral */
//                 withAWS(credentials:'aws-key', region:'us-east-1') {
//                     s3Upload(bucket:'jenkins-sqlabs-amitb', path: 'project1/', includePathPattern:'result.json')
//                 }
//             }
//         }
//         stage('Stop&Clean') {
//             steps {
//                 sh 'sudo docker stop flaskapp1 && sudo docker rm flaskapp1'
//                 sh 'rm -r result.json'
//             }
//         }
//     }
// }
