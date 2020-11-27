Download `az` or use [Cloud Shell](shell.azure.com)

Login if runing locally:

```
az login
```

Create resource group & AKS cluster with 4 nodes:

```
$rg='psod-istio'
$region='westeurope'
$cluster='psod-istio-aks'

az group create --name $rg --location $region

az aks create --resource-group $rg --name $cluster --node-count 4 --kubernetes-version 1.15.5 --generate-ssh-keys

az aks get-credentials --resource-group $rg --name $cluster
```
