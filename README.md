# Profiling Python Applications with Grafana Phlare

Samples for continuous profiling of Python applications using Grafana Phlare

-----

If you find this useful, you can support me on Ko-Fi (Donations are always appreciated, but never required):

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K6F4XN6)

## Blog Post - More Information About This Repo

You can find more information about this project/repository and how to use it in following blog post:

[...](TODO)

## Quick Start

```bash
git clone git@github.com:MartinHeinz/python-phlare.git
cd python-phlare
kind create cluster --config ./cluster.yaml --name kind --image=kindest/node:v1.26.0
kubectl apply -f grafana-deploy.yaml
kubectl apply -f phlare-deploy.yaml

# Optionally, tweak environment variables in "python-deploy.yaml"
kubectl apply -f python-deploy.yaml

kubectl port-forward svc/grafana 8080:3000
# Open: http://localhost:8080/explore
```
