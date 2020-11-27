# Demo 2 - Migrate to Istio

Bring the existing random-number app into the mesh, without breaking it.

## 2.0 Setup

Follow [demo 1](../demo1/README.md).

## 2.1 Add services to the mesh

Check Istio auto-injection:

```
kubectl get ns -L istio-injection
```

Generate manifests with side-car config:

```
istioctl kube-inject -f ../setup/rng/02_numbers-api.yaml -o rng/numbers-api.yaml

istioctl kube-inject -f ../setup/rng/03_numbers-web.yaml -o rng/numbers-web.yaml
```

> Compare injected config with setup

Deploy:

```
kubectl apply -f ./rng
```

> Test the app at http://rng.sixeyed.com

Check with Kiali:

```
istioctl dashboard kiali
```

## 2.2 mTLS migration

Configure TLS - [required for client](./rng-pre/02_destinationrules.yaml) and [supported for service](./rng-pre/01_authn.yaml):

```
kubectl apply -f ./rng-pre
```

> Test at http://rng.sixeyed.com

Check with Kiali:

```
istioctl dashboard kiali
```

Now all clients are sending TLS, upgrade to [required mTLS](./rng-post/01_authn.yaml) & [authorization](./rng-post/02_authz.yaml):

```
kubectl apply -f ./rng-post
```

> http://rng.sixeyed.com FAILS - no mTLS from `LoadBalancer` service to pod

Revert back to permissive mTLS:

```
kubectl apply -f ./rng-pre/01_authn.yaml
```

> Fixes http://rng.sixeyed.com

## 2.2 Ingress migration

Add a [gateway virtual service for the RNG app](./ingress-pre/numbers-gateway.yaml):

```
kubectl apply -f ./ingress-pre/ 
```

Now the app is available through Istio's ingress. Get ingress IP address:

```
kubectl get svc ingressgateway -n istio-system

kubectl get svc istio-ingressgateway -n istio-system -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'

$ip=$(kubectl get svc istio-ingressgateway -n istio-system -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

But only with the correct host header. Check with cURL:

```
curl --header 'Host: rng.sixeyed.com' http://$ip

curl --header 'Host: rng.sixeyed.com' http://$ip/rng
```

> Change DNS record for `rng.sixeyed.com`

```
dig rng.sixeyed.com

dig bookinfo.sixeyed.com
```

> Test http://rng.sixeyed.com

Switch to [required mTLS](./ingress-post/authn.yaml) and [convert service to internal](./ingress-post/numbers-svc.yaml):

```
kubectl apply -f ./ingress-post/ --force
```

(`force` is needed to change the service type)

> Test http://rng.sixeyed.com and http://bookinfo.sixeyed.com

Check Kiali:

```
istioctl dashboard kiali
```

- _Graph_ view, select both namespaces


