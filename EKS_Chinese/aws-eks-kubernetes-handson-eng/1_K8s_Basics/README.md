# 1. K8s Basics

# 1.1 Master Worker Architecture
![alt text](../imgs/k8s_architecture.png "K8s Architecture")

Master node (i.e. AWS EKS calls this wrapper resource as Control Plane): 
- Brain of K8s cluster
- does heavy lifting of HA, security, storage, scaling, etc

Worker node: 
- Listens to master node and create/delete container workloads
- reports metrics to master node
- has container runtime


# 1.2 Master Node (Control Plane)

![alt text](../imgs/k8s_master_worker.png "K8s Architecture")

- API server: interacts with kubectl CLI
- Etcd: key-value store, implements locks
- Controller: health check, makes sure pods are running
- Scheduler: creates new pods and assign them to nodes


# 1.3 Worker Nodes (Data Plane)

- Kubelet: agent running on cluster nodes
- Container runtime: such as Docker runtime
- Kubectl: CLI to manage/deploy apps on cluster


# 1.4 K8s Objects - pod, deployment, service, configmap, serviceaccount, ingress, etc

Pod
![alt text](../imgs/pod.png "K8s pod")

Deployment
![alt text](../imgs/deployment.png "K8s Deployment")

Service
![alt text](../imgs/service.png "K8s Service")
![alt text](../imgs/service_type.png "K8s Service Type")

Ingress
![alt text](../imgs/ingress.png "K8s Ingress")

ConfigMap
![alt text](../imgs/configmap.png "K8s ConfigMap")