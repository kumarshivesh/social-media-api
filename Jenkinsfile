pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from the repository
                checkout scm
            }
        }

        // Uncomment the following stages once the Jenkins workspace is created and ready

        /*
        stage('Cleanup Previous Containers') {
            steps {
                // Stop and remove any previous containers
                sh 'docker-compose down'
            }
        }

        stage('Build and Test') {
            steps {
                // Build the Docker images and run tests
                sh 'docker-compose build'
                sh 'docker-compose run web pytest'
            }
        }

        stage('Deploy') {
            steps {
                // Start the application using Docker Compose
                sh 'docker-compose up -d'
            }
        }
        */
    }

    post {
        always {
            // Log a message to confirm post-execution
            echo 'This will always run'
            
            // Uncomment the following to clean up unused Docker resources
            // sh 'echo "y" | docker system prune -a --volumes'
        }
    }
}
