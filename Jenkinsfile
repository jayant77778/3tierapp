pipeline {
  agent any

  environment {
    IMAGE_API = "three-tier-api"
    IMAGE_FE  = "three-tier-frontend"
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
            docker build -t ${IMAGE_API}:latest -t ${IMAGE_API}:${BUILD_TAG} ./api
            # FRONTEND
            docker build -t ${IMAGE_FE}:latest -t ${IMAGE_FE}:${BUILD_TAG} ./frontend
          """
        }
      }
    }

    stage('Deploy') {
      steps {
        dir('deploy') {
          sh """
            export BUILD_TAG=${BUILD_TAG}
            docker compose down || true
            docker compose up -d --build
          """
        }
      }
    }
  }
