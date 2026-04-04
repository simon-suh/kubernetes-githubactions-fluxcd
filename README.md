# Kubernetes + GitHub Actions + Flux CD

A local Kubernetes CI/CD pipeline using GitHub Actions for continuous integration and Flux CD for GitOps-based continuous deployment. A Python Flask microservice is built and pushed to DockerHub on every push to main. Flux CD watches the GitHub repo and automatically deploys changes to a local Minikube cluster.

## Architecture

```
GitHub (push to main)
│
├── GitHub Actions (CI)         triggered by push
│   ├── builds Docker image
│   ├── tags image with commit SHA
│   └── pushes to DockerHub
│
└── Flux CD (CD - GitOps)       polls GitHub independently
    ├── watches k8s/ folder in GitHub repo
    └── auto-deploys to Minikube
            └── Flask App (2 replicas)
                ├── /        - app status
                └── /health  - liveness probe
```

## Tech Stack

| Category | Technology |
|---|---|
| Orchestration | Kubernetes (Minikube) |
| CI | GitHub Actions |
| CD | Flux CD |
| Registry | DockerHub |
| Application | Python Flask |
| Containerization | Docker |

## Getting Started

### Prerequisites

- Docker Desktop
- Minikube
- kubectl
- Flux CLI
- GitHub account with access to this repo
- DockerHub account

### Start Minikube

```bash
minikube start --driver=docker
```

### Bootstrap Flux CD

```bash
# Replace your-github-username with your own GitHub username
GITHUB_USER=your-github-username

flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=kubernetes-githubactions-fluxcd \
  --branch=main \
  --path=./flux \
  --personal
```

After bootstrap completes, run `git pull` to get the Flux system files it created in the repo:

```bash
git pull
```

### Deploy manifests

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Trigger the CI pipeline

Push any change to main to trigger GitHub Actions. The pipeline builds the Docker image, tags it with the commit SHA, and pushes it to DockerHub. Update the image tag in `k8s/deployment.yaml` and push — Flux CD will detect the manifest change and redeploy to Minikube within 1 minute.

## Service Endpoints

| Endpoint | Description |
|---|---|
| `/` | Returns app name, status, and version |
| `/health` | Returns health status - used by liveness probe |

To access the app locally:

```bash
minikube service flask-app --url
```

Keep this terminal open — Minikube creates a tunnel that must stay running.

## Verify

Check pods are running:

```bash
kubectl get pods
```

Check Flux CD sync status:

```bash
flux get kustomizations
```

Hit the health endpoint:

```bash
curl http://<url from minikube service>/health
```

The URL is dynamically assigned by Minikube each time. Get it by running `minikube service flask-app --url` in a separate terminal and substituting the output above.

Expected response:

```json
{
    "status": "healthy",
    "app": "kubernetes-githubactions-fluxcd",
    "message": "Pipeline deployed successfully",
    "version": "2.0.0"
}
```

## Teardown

Delete Kubernetes resources:

```bash
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml
```

Stop and delete the Minikube cluster:

```bash
minikube stop
minikube delete
```

Remove unused Docker images to free disk space:

```bash
docker image prune -a
```

Docker will confirm with a "Total reclaimed space" message.
