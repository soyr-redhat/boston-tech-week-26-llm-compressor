# Workshop Security

## Network Isolation

The workshop uses Kubernetes NetworkPolicies to isolate user environments while still allowing access to shared resources.

### Applied Policies

**Jupyter User Isolation** (`openshift/jupyter-network-policy.yaml`)

This policy ensures users cannot interfere with each other's work:

- **Applies to**: All pods with label `app=jupyter`
- **Ingress**: Only allows connections from OpenShift ingress router (for external HTTPS access)
  - Users can access their JupyterLab via browser: `https://jupyter-userN.apps.ocp.ntdrq.sandbox503.opentlc.com`
  - Users CANNOT access other users' pods directly: `http://jupyter-user2:8888` is blocked
- **Egress**: Unrestricted (users can access internet, vLLM routes, pip, etc.)
  - vLLM models accessed via public HTTPS routes work normally
  - pip install and other internet access works normally

### What Users Can Access

- Their own JupyterLab instance (via browser/route)
- Shared vLLM models via public routes:
  - https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
  - https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
- Internet (for pip, guidellm, etc.)

### What Users Cannot Access

- Other users' JupyterLab pods (internal service-to-service blocked)
- Kubernetes API (no kubectl/oc installed, no RBAC permissions)
- Secrets or other cluster resources (default ServiceAccount has no permissions)

### Deployment

Apply the NetworkPolicy after deploying Jupyter instances:

```bash
oc apply -f openshift/jupyter-network-policy.yaml
```

This is automatically applied if you follow the instructor setup guide.

## RBAC Permissions

Jupyter pods use the `default` ServiceAccount which has minimal permissions:
- Can read own pod metadata
- Cannot create/delete/modify any resources
- Cannot access secrets
- Cannot list or access other pods

The workshop-assignment app uses a dedicated ServiceAccount with admin role binding scoped to the `workshop` namespace only.

## Risk Assessment

For a 60-minute workshop with a known audience:

- **Infrastructure risk**: Low (users can't modify cluster resources)
- **Data risk**: Low (no sensitive data, no secrets accessible)
- **Interference risk**: Low (NetworkPolicy prevents pod-to-pod access)
- **DoS risk**: Medium (users could spam vLLM endpoints, but notebook limits requests)

## Recommendations

For production or longer workshops:
1. Add rate limiting to vLLM routes
2. Consider separate namespaces per user for stronger isolation
3. Add resource quotas to prevent resource exhaustion
4. Enable audit logging to track user actions
