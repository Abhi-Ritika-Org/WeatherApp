pipeline {
    agent any

    environment {
        REMOTE_USER = 'ubuntu'   // use 'ubuntu' if you're using Ubuntu AMI
        REMOTE_HOST = '13.236.185.88'
        SSH_KEY = credentials('../../Downloads/weather-app-key.pem') // set this in Jenkins credentials
        APP_DIR = '/home/ubuntu/flask_app'
    }

    stages {
        stage('Clone Source') {
            steps {
                git url: 'https://github.com/Abhi-Ritika-Org/WeatherApp.git', branch: 'dev'
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['ec2-ssh-key-id']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST 'mkdir -p $APP_DIR'
                    scp -o StrictHostKeyChecking=no -i $SSH_KEY app.py $REMOTE_USER@$REMOTE_HOST:$APP_DIR/
                    scp -o StrictHostKeyChecking=no -i $SSH_KEY requirements.txt $REMOTE_USER@$REMOTE_HOST:$APP_DIR/
                    ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST 'pip install -r $APP_DIR/requirements.txt'
                    ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST 'nohup python3 $APP_DIR/app.py &'
                    """
                }
            }
        }
    }
}
