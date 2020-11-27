# Demo 4 - Logging from Istio and Envoy

Use the EFK stack - [Elasticsearch](), [Fluentd]() and [Kibana]() to record and search logs.

## 4.0 Pre-reqs

Follow the steps from [Demo 1](../demo1/README.md).

```
kubectl apply -f ../setup/
```

## 4.1 Deploy the logging stack

Deployments, services etc. in [elasticsearch.yaml](./logging/01_elasticsearch.yaml), [kibana.yaml](./logging/02_kibana.yaml) and [fluentd.yaml](./logging/03_fluentd.yaml):

```
kubectl apply -f ./logging/

kubectl get pods -n logging
```

> Browse to Kibana at http://localhost:15033

- In _Discover_ create index pattern for `logstash*`

## 4.2 Generate some load

Running for 30 seconds:

```
docker container run `
  --add-host "bookinfo.local:192.168.2.119" `
  fortio/fortio `
  load -c 32 -qps 25 -t 30s http://bookinfo.local/productpage
```

- Back to Kibana
- Filter on `kubernetes.labels.app` _is_ `productpage`

## 4.3 Configure Istio to log to Fluentd

Deploy the [Fluentd setup](fluentd-istio.yaml):

```
kubectl apply -f fluentd-istio.yaml
```
   
## 4.4 Generate load

Run a 30s burst of requests:

```
docker container run `
  --add-host "bookinfo.local:192.168.2.119" `
  fortio/fortio `
  load -c 32 -qps 25 -t 30s http://bookinfo.local/productpage
```

> Refresh Kibana at http://localhost:15033 

- Filter on `kubernetes.container.name` _is_ `istio-proxy`
- These are Envoy logs 