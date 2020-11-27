# Demo 3 - Distributed Tracing

Using [Jaegar](https://www.jaegertracing.io) to visualize trace spans and investigate outliers.

## 3.0 Pre-reqs

Follow the steps from [Demo 1](../demo1/README.md).

## 3.1 Publish the Jaegar UI

Deploy a [Gateway and VirtualService](jaegar.yaml) for Jaegar:

```
kubectl apply -f jaegar.yaml
```

> Browse to http://localhost:15032 

- Select service `productpage.default`
- Follow traces - OK & failing
- Zoom into timeline & check tags

## 3.2 Add service latency

Update the [product page](productpage-delay.yaml) to add 10s delays:

```
kubectl apply -f productpage-delay.yaml
```

> Check http://bookinfo.local/productpage & refresh

Generate some load:

```
docker container run `
  --add-host "bookinfo.local:192.168.2.119" `
  fortio/fortio `
  load -c 32 -qps 25 -t 30s http://bookinfo.local/productpage
```

- Back to Jaegar
- Follow trace for outlier