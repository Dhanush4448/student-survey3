pipeline {
  agent any
  environment {
    NAMESPACE = "studentsurvey"
    FRONTEND_IMG = "docker.io/dhanush853/studentsurvey-frontend"
    BACKEND_IMG  = "docker.io/dhanush853/studentsurvey-backend"
    IMAGE_TAG = ""
    DOCKER_BUILDKIT = "1"
  }
  options { timestamps() }
  stages {
    stage('Checkout'){ steps { checkout scm } }

    stage('Build'){
      steps {
        bat """
          docker build -t "%FRONTEND_IMG%:%IMAGE_TAG%" .\\frontend
          docker build -t "%BACKEND_IMG%:%IMAGE_TAG%"  .\\backend
        """
      }
    }

    stage('Push'){
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
          bat """
            echo %PASS% | docker login -u %USER% --password-stdin
            docker push "%FRONTEND_IMG%:%IMAGE_TAG%"
            docker push "%BACKEND_IMG%:%IMAGE_TAG%"
          """
        }
      }
    }

    stage('K8s base'){
      steps {
        bat """
          kubectl apply -f k8s\\namespace.yaml
          kubectl -n "%NAMESPACE%" apply -f k8s\\configmap-frontend.yaml
          kubectl -n "%NAMESPACE%" apply -f k8s\\backend-service.yaml
          kubectl -n "%NAMESPACE%" apply -f k8s\\frontend-service.yaml
          kubectl -n "%NAMESPACE%" apply -f k8s\\hpa-backend.yaml || exit /b 0
          kubectl -n "%NAMESPACE%" apply -f k8s\\hpa-frontend.yaml || exit /b 0
        """
      }
    }

    stage('Deploy backend & frontend'){
      steps {
        bat """
          powershell -NoProfile -Command ^
            (Get-Content k8s\\backend-deployment.yaml) ^
              -replace '__TAG__','%IMAGE_TAG%' ^
              -replace 'docker.io/YOUR_DOCKERHUB_USERNAME/studentsurvey-backend','%BACKEND_IMG%' ^
            | kubectl -n "%NAMESPACE%" apply -f -
          kubectl -n "%NAMESPACE%" rollout status deployment/studentsurvey-backend

          powershell -NoProfile -Command ^
            (Get-Content k8s\\frontend-deployment.yaml) ^
              -replace '__TAG__','%IMAGE_TAG%' ^
              -replace 'docker.io/YOUR_DOCKERHUB_USERNAME/studentsurvey-frontend','%FRONTEND_IMG%' ^
            | kubectl -n "%NAMESPACE%" apply -f -
          kubectl -n "%NAMESPACE%" rollout status deployment/studentsurvey-frontend
        """
      }
    }

    stage('Show endpoints'){
      steps {
        bat """
          kubectl -n "%NAMESPACE%" get svc
          kubectl -n "%NAMESPACE%" get deploy,pods
        """
      }
    }
  }
}
