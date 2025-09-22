pipeline {
    agent any

    environment {
        AWS_ACCOUNT   = '558772714202'                // your AWS account
        AWS_REGION    = 'ap-southeast-2'              // your AWS region
        IMAGE_NAME    = 'weatherapp'                  // your Docker image name
        ECS_CLUSTER   = 'first-cluster-ecs'           // ECS cluster name
        ECS_SERVICE   = 'first-cluster-service'       // ECS service name
    }

    stages {
        stage('Checkout Source') {
            steps {
                git url: 'git@github.com:Abhi-Ritika-Org/WeatherApp.git',
                    credentialsId: 'GITHUB-WEATHER-APP'
                // Jenkins will checkout the branch you specify in job config (Branch Specifier, e.g. */dev)
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // sanitize branch name for Docker tag (replace / with -)
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
                    # Login to AWS ECR
                    aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    # Tag images with full ECR path
                    docker tag ${IMAGE_NAME}:latest ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest
                    docker tag ${IMAGE_NAME}:${BRANCH_TAG} ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BRANCH_TAG}

                    # Push both tags
                    docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest
                    docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BRANCH_TAG}

                    # Optional: clean up
                    docker image rm ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:latest \
                                   ${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BRANCH_TAG} \
                                   ${IMAGE_NAME}:latest ${IMAGE_NAME}:${BRANCH_TAG}
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
