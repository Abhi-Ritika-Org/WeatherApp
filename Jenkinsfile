pipeline {
    agent any

    environment {
        AWS_ACCOUNT   = '558772714202'
        AWS_REGION    = 'ap-southeast-2'
        IMAGE_NAME    = 'weatherapp'
        ECS_CLUSTER   = 'first-cluster-ecs'
        ECS_SERVICE   = 'first-cluster-service'
    }

    stages {
        // stage('Checkout Source') {
        //     steps {
        //         echo "Source already checked out by Jenkins. Using branch: ${env.BRANCH_NAME}"
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                script {
                    BRANCH_TAG = env.BRANCH_NAME.replaceAll('/', '-')
                }
                sh """
                    docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${BRANCH_TAG} .
                """
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    BRANCH_TAG = env.BRANCH_NAME.replaceAll('/', '-')
                }
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    docker tag ${IMAGE_NAME}:latest ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest
                    docker tag ${IMAGE_NAME}:${BRANCH_TAG} ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BRANCH_TAG}

                    docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest
                    docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BRANCH_TAG}
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
