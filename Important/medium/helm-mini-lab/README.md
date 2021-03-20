# Table of Contents
1. [Play with Kubernetes](#play-with-kubernetes)
1. [Play with Helm](#play-with-helm)

# Play with Kubernetes

## Create new Deployment

```sh
kubectl run my-nginx --image=nginx
```

## List objects created by this Deployment

```sh
kubectl get deployment,rs,pod,svc
```

## Forward Pod port to localhost

```sh
kubectl port-forward my-nginx-b67c7f44-lv4fb 8000:80 # pod name: my-nginx-b67c7f44-lv4fb
```

## Remove Deployment

```sh
kubectl delete deployment my-nginx
```

# Play With Helm

## Create a new Chart

```sh
helm create mychart
# base files will be created under mychart/ directory
```

## Create a ConfigMap

Sample file `mychart/templates/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-configmap
data:
  superSecretValue: "idgafos"

```

## Install our new Chart

```sh
helm install ./mychart --name mychart
```

## Check our Chart configuration

```sh
helm get manifest mychart
```

## Update Chart configuration

```sh
helm upgrade mychart ./mychart
```

## Set custom values using the Command Line

```sh
helm upgrade mychart ./mychart --set asdfcomplex.qwert=kkk
```
