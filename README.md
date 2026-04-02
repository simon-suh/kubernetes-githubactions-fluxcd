# kubernetes-githubactions-fluxcd

Local Kubernetes stack with Minikube, GitHub Actions and Flux CD for GitOps CI/CD pipeline.

## Stack
- Minikube: local Kubernetes cluster
- GitHub Actions: CI pipeline (build and push Docker image)
- Flux CD: CD GitOps controller (deploys to Minikube)
- Python Flask: sample microservice with health check endpoint
- Docker: containerization
