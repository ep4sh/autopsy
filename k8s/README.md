# K8s chart for Autopsy

Autopsy k8s helm chart has been tested in minikube
It may be different for your cluster - feel free to change anything you want


## Installation

#### Secrets

```
cd common
cp secrets.yml.sample secrets.yml
k apply -f secrets.yml
```


#### Autopsy app
```
cd autopsy/k8s
helm install autopsy autopsy/ -f autopsy/values.yaml
```


#### Setup your favourite balancer for autopsy service

#### Cheerz =*
