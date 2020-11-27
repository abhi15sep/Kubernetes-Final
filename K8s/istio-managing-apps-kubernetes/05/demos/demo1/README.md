# Demo 1 - Visualizing the Service Mesh

Using [Kiali](https://kiali.io) to graph active services and see the traffic flow between them.

## 1.0 Pre-reqs

Deploy Istio & bookinfo app:

```
kubectl apply -f ../setup/
```

> There are some new ports in the [Istio ingress gateway](../setup/02_istio-demo.yaml).

## 1.1 Publish the Kiali UI

Deploy a [Gateway and VirtualService](kiali.yaml) for Kiali:

```
kubectl apply -f kiali.yaml
```

> Browse to http://localhost:15029, sign in with `admin`/`admin`

- App graph in _Graph_
- Check `productpage` in Kiali _Workloads_

## 1.2 Canary deployment for v2

Deploy [v2 product page](./v2/productpage-v2-canary.yaml) and [v2 reviews API](./v2/reviews-v2-canary.yaml) updates:

```
kubectl apply -f ./v2/
```

> Browse to http://bookinfo.local/productpage and refresh 

- Back to Kiali
- Switch versioned app graph
- Add _Requests percentage_ label
- Check bookinfo virtual service in _Istio Config_ (editable!)

## 1.3 Generate some load

Use [Fortio](https://fortio.org) to send a few hundred requests to the app:

```
docker container run `
  --add-host "bookinfo.local:192.168.2.119" `
  fortio/fortio `
  load -c 32 -qps 25 -t 30s http://bookinfo.local/productpage
```

- Back to Kiali _Graph_