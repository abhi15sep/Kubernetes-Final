#Let's ask the API Server for the API Groups it knows about.
kubectl api-resources | more

#A list of the objects available in that API Group
kubectl api-resources --api-group=apps

#We can use explain to dig further into a specific API Object 
#Check out KIND and VERSION, we'll see the API Group in the from group/version 
#Follow the version specified in THAT deprecation warning. Ah...the one we should use.
kubectl explain deployment --api-version apps/v1 | head

#Print the supported API versions on the API server again in the form group/version.
#Here we see several api objects have several version, addmissionregistration, apiextensions all have v1 and v1beta1 versions
kubectl api-versions | sort | more

#Deployment went GA under apps/v1 in version 1.9...so we can use apps/v1 as the api version
kubectl apply -f deployment.yaml

#let's look at a Deployment yaml from the api server, its apps/v1
kubectl get deployment hello-world -o yaml | head

#Let's clean up after this demo
kubectl delete deployment hello-world