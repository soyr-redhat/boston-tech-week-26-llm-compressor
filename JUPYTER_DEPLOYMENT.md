# JupyterLab Deployment Guide

## Deploy Per-User JupyterLab Instances

### Prerequisites

- Logged into OpenShift cluster as admin
- Workshop namespace exists

### Quick Deploy (50 users)

```bash
# Provision JupyterLab for all 50 users
./scripts/provision-users.sh 50

# This creates:
# - jupyter-user1 through jupyter-user50
# - Routes: https://jupyter-user1.apps.ocp.ntdrq.sandbox503.opentlc.com, etc.
```

### Deploy Single User (for testing)

```bash
# Deploy for a specific user
oc process -f openshift/jupyter-user-template.yaml \
  -p USER_ID=user1 \
  -n workshop \
  | oc apply -f -

# Wait for deployment
oc wait --for=condition=available --timeout=300s deployment/jupyter-user1 -n workshop

# Check pod status
oc get pods -n workshop -l user=user1

# Get the route URL
oc get route jupyter-user1 -n workshop -o jsonpath='{.spec.host}'
```

### Access JupyterLab

1. Navigate to the route URL (e.g., `https://jupyter.apps.ocp.ntdrq.sandbox503.opentlc.com`)
2. The workshop notebook will be pre-loaded at `/home/jovyan/workshop_notebook.ipynb`
3. Participants can run cells to benchmark models

### Verify Setup

```bash
# Check if notebook ConfigMap exists
oc get configmap workshop-notebook -n workshop

# View notebook content
oc get configmap workshop-notebook -n workshop -o jsonpath='{.data.workshop_notebook\.ipynb}' | head -20

# Check service endpoints
oc get svc -n workshop | grep -E "(jupyter|vllm)"
```

### Update Notebook

If you need to update the notebook after deployment:

```bash
# Edit the ConfigMap
oc edit configmap workshop-notebook -n workshop

# Or recreate from file
oc delete configmap workshop-notebook -n workshop
oc create configmap workshop-notebook \
  --from-file=workshop_notebook.ipynb \
  -n workshop

# Restart the Jupyter pod to pick up changes
oc rollout restart deployment/jupyter -n workshop
```

### Troubleshooting

**Pod not starting:**
```bash
# Check pod logs
oc logs -f deployment/jupyter -n workshop

# Describe pod for events
oc describe pod -l app=jupyter -n workshop
```

**Can't access notebook:**
```bash
# Check route
oc get route jupyter -n workshop

# Verify service is up
oc get svc jupyter -n workshop

# Test internal connectivity
oc run test-curl --rm -it --image=curlimages/curl -- sh
# curl http://jupyter:8888
```

**Notebook not loaded:**
```bash
# Check ConfigMap mount
oc get pod -l app=jupyter -n workshop -o jsonpath='{.items[0].spec.volumes[?(@.name=="workshop-notebook")]}'

# Exec into pod and check
oc exec -it deployment/jupyter -n workshop -- ls -la /home/jovyan/
```

### Scaling for Multiple Users

For a multi-user setup (50+ participants), consider using JupyterHub instead:

```bash
# Deploy JupyterHub (example using Helm)
helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm repo update

helm install jupyterhub jupyterhub/jupyterhub \
  --namespace workshop \
  --values jupyterhub-config.yaml
```

See [Zero to JupyterHub](https://zero-to-jupyterhub.readthedocs.io/) for full multi-user setup.

### Resource Limits

Current configuration:
- **Requests:** 1 CPU, 2Gi RAM
- **Limits:** 2 CPU, 4Gi RAM

Adjust based on user load:

```bash
oc set resources deployment/jupyter \
  --requests=cpu=2,memory=4Gi \
  --limits=cpu=4,memory=8Gi \
  -n workshop
```

### Clean Up

```bash
# Remove JupyterLab deployment
oc delete -f openshift/jupyter-deployment.yaml

# Or delete individual resources
oc delete deployment jupyter -n workshop
oc delete service jupyter -n workshop
oc delete route jupyter -n workshop
oc delete configmap workshop-notebook -n workshop
```

## Architecture

```
┌─────────────────────────────────────────┐
│     Participant Browser                 │
│  https://jupyter.apps...opentlc.com     │
└────────────┬────────────────────────────┘
             │ HTTPS
             ▼
    ┌────────────────┐
    │  OpenShift     │
    │  Route         │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │  JupyterLab    │
    │  Service       │
    │  Port: 8888    │
    └────────┬───────┘
             │
             ▼
    ┌────────────────────────────────────┐
    │  Jupyter Pod                        │
    │  - scipy-notebook image             │
    │  - workshop_notebook.ipynb mounted  │
    │  - guidellm auto-installed in cell  │
    └────────┬───────────────────────────┘
             │
             │ Internal cluster networking
             │
    ┌────────▼─────────┬──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ vLLM     │    │ vLLM     │    │Comparison│
│ Original │    │Quantized │    │   UI     │
│ :8000    │    │ :8000    │    │  :7860   │
└──────────┘    └──────────┘    └──────────┘
```

## Notes

- Notebook uses internal cluster service URLs (`http://vllm-original:8000/v1`)
- No external API keys or authentication needed
- Each participant gets isolated notebook cells
- Results are stored in ephemeral storage (lost on pod restart)
- For persistent storage, add a PVC mount
