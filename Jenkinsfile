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
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying the application"
                sh "sudo /bin/systemctl restart gunicorn_malproxy.service"
                echo "Waiting 5 secs to let app finish booting..."
                sh "sleep 3s"
                sh "curl --silent --show-error --fail http://127.0.0.1:8181/ping"
            }
        }

        stage('Post-Deploy Test') {
            steps {
                sh 'python -m py.test --junit-xml test-reports/deploy_results.xml tests/test_deploy.py'
            }
        }
    }

    post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test-reports/*.xml'
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
