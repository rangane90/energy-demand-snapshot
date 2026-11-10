pipeline {
    agent { label 'docker' }

    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Test API') {
            steps {
                sh 'python3 -B -m unittest -v'
            }
        }

        stage('Build image') {
            steps {
                script {
                    env.REVISION = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                }
                sh '''
                    docker build --label "org.opencontainers.image.revision=$REVISION" \
                        --tag "energy-demand-snapshot:$REVISION" .
                '''
            }
        }

        stage('Smoke test container') {
            steps {
                sh '''
                    container=$(docker run --detach "energy-demand-snapshot:$REVISION")
                    trap 'docker rm -f "$container" >/dev/null' EXIT
                    for attempt in 1 2 3 4 5; do
                        if docker exec "$container" python -c 'import json; from urllib.request import urlopen; data = json.load(urlopen("http://127.0.0.1:8080/summary", timeout=2)); assert data["samples"] == 8'; then
                            exit 0
                        fi
                        sleep 1
                    done
                    docker logs "$container"
                    exit 1
                '''
            }
        }
    }
}
