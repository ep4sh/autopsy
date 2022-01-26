# K8s chart for Autopsy

Autopsy k8s helm chart has been tested in minikube
It may be different for your cluster - feel free to change anything you want


## Installation

Create a namespace
```
kubectl create namespace autopsy
```

#### Secrets

```
cd common
cp secrets.yml.sample secrets.yml
k apply -f secrets.yml --namespace=autopsy
```


#### Autopsy app

Update dependencies
```
cd ../autopsy
helm dependency update
helm dependency list
```

Install with dependencies

```
helm install autopsy . -f values.yaml
```

Currently postgresql chart has a problem with secret injection:
https://github.com/bitnami/charts/issues/2061

but you can rollout PostgreSQL with standalone helm:
```
helm install postgresql --version 8.7.3 \
    --set postgresqlUsername=postgres \
    --set postgresqlPassword=postgres \
    --set postgresqlDatabase=postgres \
    bitnami/postgresql
```

For arm64 I recommend using:
```
helm install postgresql --set userDatabase.name=postgres --set userDatabase.user=postgres --set userDatabase.password=postgres groundhog2k/postgres
```

#### Set up a favourite ingress controller and apply ingress
