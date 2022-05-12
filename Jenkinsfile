pipeline {
    agent { label 'norman' }
    stages {
        stage('Build') {
            steps {
                echo "building the repo"
                sh "pip install -r requirements.txt"
            }
        }

        stage('Test') {
            steps {
                echo "I would have tested the app, if you were a better person..."
                input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying the application"
                sh "screen -dm -S mal_proxy_screen 'python3 app.py &'"
                echo "Waiting 5 secs to let app finish booting..."
                sh "sleep 5s"
                sh "curl --silent --show-error --fail http://127.0.0.1:8181/ping"
            }
        }
    }

    post {
        always {
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
