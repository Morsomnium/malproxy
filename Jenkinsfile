pipeline {
    agent { label 'norman' }
    stages {
        stage('Build') {
            steps {
                sh 'echo "building the repo"'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "I would have tested the app, if you were a better person..."'
                input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying the application"
                sh "nohup python3 app.py > log.txt 2>&1 &"
            }
        }
    }

    post {
        always {
            final String url = "http://localhost:8181/ping"
            final def (String body, int code) = sh(script: "curl -s -w '\\n%{response_code}' $url", returnStdout: true).trim().tokenize("\n")
            sh 'echo "HTTP response status code: $code"'

            if (code != 200 && body != "pong!") {
                error("cURL failed, assuming the Build has failed!")
            }

            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early...')
        }
	}
}
