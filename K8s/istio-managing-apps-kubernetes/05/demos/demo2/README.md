# Demo 2 - Monitoring with Prometheus & Grafana

See the metrics coming into [Prometheus](https://prometheus.io) and the Istio dashboards in [Grafana](https://grafana.com).

## 2.0 Pre-reqs

Follow the steps from [Demo 1](../demo1/README.md).

## 2.1 Publish the Prometheus UI

Deploy a [Gateway and VirtualService](prometheus.yaml) for Prometheus:

```
kubectl apply -f prometheus.yaml
```

> Browse to http://localhost:15030

- Select `istio_requests_total`
- Switch to _Graph_
- Check _Status_/_Targets_ - Kubernetes service discovery

## 2.2 Generate some load

Send requests for next 30 minutes:

```
docker container run `
  --add-host "bookinfo.local:192.168.2.119" `
  fortio/fortio `
  load -c 32 -qps 25 -t 30m http://bookinfo.local/productpage
```

- Back to _Graph_ view in Prometheus

## 2.3 Publish the Grafana UI

> New terminal

Deploy a [Gateway and VirtualService](grafana.yaml) for Grafana:

```
kubectl apply -f grafana.yaml
```

> Browse to http://localhost:15031

 - _Istio Mesh Dashboard_ - overview
 - _Istio Service Dashboard_ - drill down into service 

## 2.4 Deploy a failing service

Update the [v2 reviews service](reviews-v2-abort.yaml) to add `503` faults:

```
kubectl apply -f reviews-v2-abort.yaml
```

> Check [Grafana](http://localhost:15031/d/LJ_uJAvmk/istio-service-dashboard?orgId=1&refresh=5s&from=now-5m&to=now&var-service=reviews.default.svc.cluster.local&var-srcns=All&var-srcwl=All&var-dstns=All&var-dstwl=All)

> And [Kiali](http://localhost:15029/kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=versionedApp&namespaces=default&unusedNodes=false&injectServiceNodes=true&pi=10000&duration=300&layout=dagre)
