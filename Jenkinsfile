node {

    git branch: "master", url: "http://git.ik.ntr/FIRE/Processador.git"

    stage ('Construindo a imagem podman do projeto Processador') {
        sh "echo construindo a imagem..."
        sh "podman --remote build --tag fire/processador:latest ."
        sh "echo construcao terminada"
    }

    stage ('Instalando o servidor Processador') {
        sh "echo Instalando o servidor Processador..."
        sh "podman --remote rm -f processador || true"
        sh "podman --remote run -p 8080:80 --restart unless-stopped --name processador fire/processador:latest"
        sh "echo container Processador instalado"
    }
}