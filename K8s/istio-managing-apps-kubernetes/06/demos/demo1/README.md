# Demo 1 - Deploy Istio & BookInfo

Deploy a production-grade Istio setup on a cluster with an existing app; run Istio and non-Istio apps together.

## 1.0 Setup

See [Istio's platform setup guides](https://istio.io/docs/setup/platform-setup/).

I'm using a [4-node AKS cluster](create-aks-cluster.md).

> In Docker Desktop, select your cluster

Verify:

```
kubectl get nodes
```

Deploy random number generator app:

```
kubectl apply -f ../setup/rng/

kubectl get pods -n rng

kubectl get svc -n rng

dig rng.sixeyed.com
```

> Check the app at http://rng.sixeyed.com

## 1.1 Install istio

> Download [istioctl](https://github.com/istio/istio/releases)

```
istioctl profile list

istioctl profile dump > ./temp/istio-default-profile.yaml
```

> These are the [configurable settings](https://istio.io/docs/reference/config/istio.operator.v1alpha12.pb/)

Deploy direct from `istioctl`:

```
istioctl manifest apply

istioctl manifest apply --set values.kiali.enabled=true
```

## 1.2 Customize the installation

Generate a Kube manifest:

```
istioctl manifest generate > ./temp/istio-default-manifest.yaml
```

- Open [default manifest](./temp/istio-default-manifest.yaml)
- Search for _MeshPolicy_
- Search for _Kiali component_

Generate a custom manifest:

```
istioctl manifest generate --set values.kiali.enabled=true > ./temp/istio-custom-manifest.yaml
```

Or use an [override file](./istio-custom/kiali-enable.yaml) for more control:

```
istioctl manifest generate -f istio-custom/kiali-enable.yaml > ./istio/istio-custom-manifest.yaml
```

- Open [custom manifest](./istio/istio-custom-manifest.yaml)
- Search for _MeshPolicy_
- Search for _Kiali component_

## 1.2 Deploy Istio

```
kubectl apply -f ./istio/
```

Check Kiali:

```
istioctl dashboard kiali
```

> Check [random number generator app](http://rng.sixeyed.com) is still working

## 1.3 Deploy BookInfo

BookInfo v1 deployment with Istio:

- [namespace with Istio injection](./bookinfo/01_bookinfo-ns.yaml)
- every component has a [ServiceAccount and a Service with named ports](./bookinfo/05_bookinfo-v1.yaml)
- [VirtualServices](./bookinfo/06_virtualservices.yaml) and [DestinationRules](./bookinfo/04_destinationrules.yaml) for all components
- [mTLS with Istio certs](./bookinfo/02_authn.yaml) and [service authorization](./bookinfo/03_authz.yaml)
- [gateway configured for production domain](./bookinfo/07_bookinfo-gateway.yaml)

```
kubectl apply -f ./bookinfo/
```

Get ingress IP address:

```
kubectl get svc istio-ingressgateway -n istio-system
```

> Add external IP to DNS A record - `bookinfo.sixeyed.com`

```
dig bookinfo.sixeyed.com
```

Check Kiali:

```
istioctl dashboard kiali
```

> Check [bookinfo.sixeyed.com](http://bookinfo.sixeyed.com) is up

> Check [rng.sixeyed.com](http://rng.sixeyed.com) is still working
