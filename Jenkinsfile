node {

    git branch: "master", url: "http://git.ik.ntr/FIRE/Processador.git"

    stage ('Build podman image') {
        sh "echo building the image..."
        sh "podman --remote build --tag python:3.9 ."
        sh "echo buid complete"
    }

    stage ('Deploy the podman image') {
        sh "echo deploying container..."
        sh "podman --remote run -p 8000:8000 --name processador python:3.9"
        sh "echo container deployed"
    }
}