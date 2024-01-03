# rhoai

Localhost cmds:

- podman build -t priv_net_app .
- podman login -u <USER> -p <PWD> quay.io
- podman tag <IMAGE_ID> quay.io/ldornele/priv_net_app
- podman push quay.io/ldornele/priv_net_app

Bastion Server cmds:

- oc apply -f deploy/deployment.yaml
- oc apply -f deploy/service.yaml
- oc apply -f deploy/route.yaml