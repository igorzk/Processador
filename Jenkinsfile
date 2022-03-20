node {

    stage ('Deploy the podman image') {
        sh "echo deploying container..."
        sh "podman --remote run -p 8080:80 --name test-nginx nginx"
        sh "echo container deployed"
    }
}