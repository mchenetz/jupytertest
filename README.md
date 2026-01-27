The standard way to install JupyterHub is via the zero-to-jupyterhub Helm chart. You’ll customize it to use Portworx for user home directories and NFS for a shared dataset folder.1

Prerequisites
A Kubernetes cluster with Portworx installed.
An NFS server (external or in-cluster) with a shared path (e.g., /export/datasets).
Step A: Create Portworx StorageClasses
Create a high-performance class for the Hub database and user home directories.

YAML

Template:

kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: portworx-proxy-volume-volume
provisioner: pxd.portworx.com
parameters:
  proxy_endpoint: "nfs://<nfs-share-endpoint>"
  proxy_nfs_exportpath: "/<mount-path>"
  mount_options: "vers=4.0"
allowVolumeExpansion: true
Example:

kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: portworx-proxy-volume-volume
provisioner: pxd.portworx.com
parameters:
  proxy_endpoint: "nfs://192.168.10.5"
  proxy_nfs_exportpath: "/volume1/kube"
  mount_options: "vers=4.0"
allowVolumeExpansion: true
Step B: Define the NFS Shared Volume
Create a PersistentVolume (PV) and Claim (PVC) for the NFS share.

YAML

kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: nfs-data
  namespace: jupyterhub
  labels:
    app: jupyterhub
spec:
  storageClassName: portworx-proxy-volume-volume
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Ti
Step C: Configure and Install JupyterHub
Create a values.yaml file to tell JupyterHub to use these storage resources.

YAML


hub:
  db:
    pvc:
      storageClassName: px-csi-replicated
  
singleuser:
  image:
    name: jupyter/datascience-notebook
    tag: latest
  extraLabels:
    app: "jupyterhub"
  storage:
    dynamic:
      storageClass: px-csi-replicated
    extraVolumes:
      shared-data:
        name: shared-data
        persistentVolumeClaim:
          claimName: nfs-data
    extraVolumeMounts:
      shared-data:
        name: shared-data
        mountPath: /home/jovyan/shared
Install via Helm:

Bash

helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm repo update
helm upgrade --install jhub jupyterhub/jupyterhub --values values.yaml -n jupyterhub --create-namespace
