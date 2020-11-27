# Demo 2 - Service Authorization

Enforce access control for services based on the caller's mTLS identity.

## 2.0 Pre-reqs

Follow the steps from [Demo 1](../demo1/README.md).

## 2.1 Restrict access to reviews

Apply a [deny-all authorization policy](reviews-deny-all.yaml) for the service:

```
kubectl apply -f reviews-deny-all.yaml
```

> Check http://localhost/productpage

## 2.2 Allow access from product page

Apply the [updated authorization policy](reviews-allow-productpage.yaml) to allow service access:

```
kubectl apply -f reviews-allow-productpage.yaml
```

> And check http://localhost/productpage

## 2.3 Try from unauthorized service

Run a shell in the details API container:

```
docker container ls --filter name=k8s_details

docker container exec -it $(docker container ls --filter name=k8s_details --format '{{ .ID}}') sh
```

Try accessing the reviews & ratings APIs:

```
curl http://reviews:9080/1

curl http://ratings:9080/ratings/1
```

## 2.4 Check the TLS client certs

Run a shell in the product page container:

```
docker container exec -it $(docker container ls --filter name=istio-proxy_productpage --format '{{ .ID}}') sh
```

Check the identity in the cert:

```
cat /etc/certs/cert-chain.pem | openssl x509 -text -noout  | grep 'Subject Alternative Name' -A 1

exit
```

> URI is the principal in AuthorizationPolicy (using [SPIFFE](https://spiffe.io))

And in the details API container:

```
docker container exec -it $(docker container ls --filter name=istio-proxy_details --format '{{ .ID}}') sh

cat /etc/certs/cert-chain.pem | openssl x509 -text -noout  | grep 'Subject Alternative Name' -A 1

exit
```

> Principal not listed in AuthorizationPolicy

