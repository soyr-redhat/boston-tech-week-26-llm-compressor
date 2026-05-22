# Instructor Setup Guide - Boston Tech Week 2026

## Pre-Workshop Deployment (Day Before)

### 1. Deploy Shared Infrastructure

```bash
# Log into OpenShift
oc login https://api.ocp.ntdrq.sandbox503.opentlc.com:6443

# Create workshop namespace
oc create namespace workshop

# Deploy vLLM models and comparison UI
oc apply -f openshift/workshop-deployment.yaml

# Wait for models to load (5-10 minutes)
oc get pods -n workshop -w

# Verify models are responding
curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
curl https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
```

### 2. Provision User JupyterLab Instances

```bash
# Deploy JupyterLab for 50 users
./scripts/provision-users.sh 50

# This creates jupyter-user1 through jupyter-user50
# Each user gets: https://jupyter-user{N}.apps.ocp.ntdrq.sandbox503.opentlc.com
```

### 3. Verify All Services

```bash
# Check all pods are running
oc get pods -n workshop

# Should see:
# - vllm-original-* (2 GPUs)
# - vllm-quantized-* (2 GPUs)
# - comparison-ui-*
# - jupyter-user1 through jupyter-user50

# Check all routes
oc get routes -n workshop

# Test a few user notebooks
open https://jupyter-user1.apps.ocp.ntdrq.sandbox503.opentlc.com
open https://jupyter-user25.apps.ocp.ntdrq.sandbox503.opentlc.com
open https://jupyter-user50.apps.ocp.ntdrq.sandbox503.opentlc.com
```

### 4. Prepare User List

Create a simple user assignment list:

```bash
# Generate user URLs
for i in {1..50}; do
  echo "User $i: https://jupyter-user${i}.apps.ocp.ntdrq.sandbox503.opentlc.com"
done > workshop-user-urls.txt
```

Print or share this file with participants at the workshop.

---

## During Workshop

### Part 1: Demo (30 min)

1. **Show comparison UI** - https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
   - Run a few prompts side-by-side
   - Point out the performance differences in real-time

2. **Explain the architecture:**
   ```
   50 Participants → 50 JupyterLab instances → 2 Shared vLLM models
   ```

3. **Show what quantization does:**
   - Memory: FP16 ~14GB vs INT4 ~5GB
   - Speed: 1.5-2x faster throughput
   - Quality: <2% degradation

### Part 2: Hands-On (30 min)

1. **Distribute user IDs:**
   - Hand out slips with user numbers (1-50)
   - Or display the workshop-user-urls.txt file

2. **Guide participants:**
   - Open your assigned URL
   - Click on `workshop_notebook.ipynb`
   - Run cells in order (Shift+Enter)
   - First cell installs guidellm (~2 min)

3. **Help troubleshoot:**
   - If notebook doesn't load: check pod status `oc get pods -n workshop -l user=user{N}`
   - If benchmark fails: likely too many concurrent requests, ask them to retry
   - If guidellm install fails: restart kernel and try again

### Common Issues

**"Cannot connect to vLLM"**
- Check if vLLM pods are running: `oc get pods -n workshop -l app=vllm`
- Verify services: `oc get svc vllm-original vllm-quantized -n workshop`

**"JupyterLab won't load"**
- Check specific user's pod: `oc get pod -l user=user5 -n workshop`
- View logs: `oc logs deployment/jupyter-user5 -n workshop`

**"Benchmarks are slow"**
- Expected! 50 users hammering 2 shared models
- Suggest running with fewer requests: `--max-requests 5` instead of 10

---

## Post-Workshop

### Keep Environment Running (Optional)

Leave the infrastructure up for a week so participants can experiment:

```bash
# Just leave everything running
# Participants can access their notebooks anytime
```

### Clean Up After Event

```bash
# Remove all user JupyterLab instances
./scripts/cleanup-users.sh 50

# Remove shared infrastructure
oc delete -f openshift/workshop-deployment.yaml

# Or delete entire namespace
oc delete namespace workshop
```

---

## Resource Usage

### Current Deployment

- **GPUs:** 4× NVIDIA L4 (2 per vLLM model)
- **Memory:** ~60GB total
  - 32GB for vLLM models (16GB each)
  - 200GB for 50 JupyterLab instances (4GB limit each)
- **CPU:** ~60 cores
  - 16 cores for vLLM models (8 each)
  - 50 cores for JupyterLab (1 limit each)

### Cost Optimization

If resources are tight, reduce JupyterLab limits:

```bash
# Lower memory/CPU per user
# Edit openshift/jupyter-user-template.yaml:
resources:
  requests:
    memory: "1Gi"   # from 2Gi
    cpu: "250m"     # from 500m
  limits:
    memory: "2Gi"   # from 4Gi
    cpu: "500m"     # from 1
```

---

## Workshop Materials

### Share with Participants

- **GitHub Repo:** https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor
- **Quick Start:** Point them to QUICK_START.md
- **Documentation:** https://soyr-redhat.github.io/boston-tech-week-26-llm-compressor

### After Workshop

Participants can:
- Download their notebooks with results
- Clone the repo and run locally
- Explore RedHat AI models: https://huggingface.co/RedHatAI
- Try LLM Compressor: https://github.com/vllm-project/llm-compressor

---

## Contact

Questions or issues? Check the repo issues:
https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor/issues
