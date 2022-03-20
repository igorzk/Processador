node {

    stage ('Deploy the podman image') {
        sh "echo deploying container..."
        sh "podman --remote run -p 80:8080 --name test-nginx nginx"
        sh "echo container deployed"
    }
}