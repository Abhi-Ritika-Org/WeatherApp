pipeline {
    agent any

    environment {
        // BRANCH_NAME   = 'dev'                      // branch to build
        AWS_ACCOUNT   = '558772714202'             // your AWS account
        AWS_REGION    = 'ap-southeast-2'              // your AWS region
        IMAGE_NAME    = 'weatherapp'              // your Docker image name
        ECS_CLUSTER   = 'first-cluster-ecs'      // ECS cluster name
        ECS_SERVICE   = 'first-cluster-service'      // ECS service name
    }

    stages {
        stage('Checkout Source') {
            steps {
                git url: 'https://github.com/Abhi-Ritika-Org/WeatherApp.git"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    # Login to AWS ECR
                    aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    # Tag and push image
                    docker tag ${IMAGE_NAME}:latest ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest
                    docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest

                    # Optional: remove local image to save space
                    docker image rm ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to ECS') {
            steps {
                sh """
                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --force-new-deployment \
                        --region ${AWS_REGION}
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs."
        }
    }
}
