#!groovy
pipeline {
	agent none
  stages {
  	stage('Python') {
    	agent {
      	docker {
        	image 'python:3.9-slim'
        }
      }
      steps {
      	sh 'python3 --version'
      }
    }
  }
}