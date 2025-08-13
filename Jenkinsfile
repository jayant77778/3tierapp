pipeline {
  agent any

  environment {
    IMAGE_API      = "three-tier-api"
    IMAGE_FE       = "three-tier-frontend"
    DOCKERHUB_USER = credentials('dockerhub-username') // just username string
    // dockerhub-creds should be a "Username with password" credential
  }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/jayant77778/Devops-project.git'
      }
    }

    stage('Prepare') {
      steps {
        sh '''
        echo "Docker version:" && docker --version
        echo "Node version:" || true
        '''
      }
    }

    stage('Build Images') {
      steps {
        script {
          env.BUILD_TAG = "build-${env.BUILD_NUMBER}"
          sh """
            # API
            docker build -t ${DOCKERHUB_USER}/${IMAGE_API}:latest -t ${DOCKERHUB_USER}/${IMAGE_API}:${BUILD_TAG} ./api
            # FRONTEND
            docker build -t ${DOCKERHUB_USER}/${IMAGE_FE}:latest -t ${DOCKERHUB_USER}/${IMAGE_FE}:${BUILD_TAG} ./frontend
          """
        }
      }
    }

    stage('Push Images') {
      when { expression { return env.DOCKER_PUSH?.toBoolean() || true } }
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${DOCKERHUB_USER}/${IMAGE_API}:latest
            docker push ${DOCKERHUB_USER}/${IMAGE_API}:${BUILD_TAG}
            docker push ${DOCKERHUB_USER}/${IMAGE_FE}:latest
            docker push ${DOCKERHUB_USER}/${IMAGE_FE}:${BUILD_TAG}
            docker logout
          """
        }
      }
    }

    stage('Deploy') {
      steps {
        dir('deploy') {
          sh """
            export DOCKERHUB_USER=${DOCKERHUB_USER}
            export BUILD_TAG=${BUILD_TAG}
            # ensure compose plugin or docker-compose is present
            docker compose version || true
            docker compose pull || true
            docker compose up -d
          """
        }
      }
    }
  }

  post {
    success {
      echo "✅ Deployed. Frontend: http://<EC2-IP>/  | API: http://<EC2-IP>:5000/health"
    }
    failure {
      echo "❌ Pipeline failed. Check stages log."
    }
  }
}
