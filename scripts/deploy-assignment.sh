#!/bin/bash
# Deploy workshop assignment app

set -e

NAMESPACE="workshop"

echo "========================================="
echo "Deploying Workshop Assignment App"
echo "========================================="
echo ""

# Create ConfigMap with app code
echo "Creating ConfigMap with app code..."
oc create configmap assignment-app-code \
  --from-file=assignment_app.py \
  -n $NAMESPACE \
  --dry-run=client -o yaml | oc apply -f -

# Deploy the app
echo "Deploying assignment app..."
cat > /tmp/assignment-deployment.yaml <<'EOF'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: workshop-assignment
  namespace: workshop
  labels:
    app: workshop-assignment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: workshop-assignment
  template:
    metadata:
      labels:
        app: workshop-assignment
    spec:
      containers:
      - name: assignment-app
        image: python:3.11-slim
        command: ["/bin/sh", "-c"]
        args:
          - |
            pip install -q Flask
            python /app/assignment_app.py
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: TOTAL_USERS
          value: "50"
        - name: BASE_URL
          value: "https://jupyter-{user_id}.apps.ocp.ntdrq.sandbox503.opentlc.com"
        - name: SECRET_KEY
          value: "boston-tech-week-2026-secret"
        volumeMounts:
        - name: app-code
          mountPath: /app
        - name: assignments
          mountPath: /tmp
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      volumes:
      - name: app-code
        configMap:
          name: assignment-app-code
      - name: assignments
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: workshop-assignment
  namespace: workshop
spec:
  selector:
    app: workshop-assignment
  ports:
  - port: 8080
    targetPort: 8080
    name: http

---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: workshop-assignment
  namespace: workshop
spec:
  host: workshop.apps.ocp.ntdrq.sandbox503.opentlc.com
  to:
    kind: Service
    name: workshop-assignment
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
EOF

oc apply -f /tmp/assignment-deployment.yaml
rm /tmp/assignment-deployment.yaml

echo ""
echo "Waiting for deployment..."
oc wait --for=condition=available --timeout=300s deployment/workshop-assignment -n $NAMESPACE

echo ""
echo "========================================="
echo "Assignment App Deployed!"
echo "========================================="
echo ""
echo "URL: https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com"
echo ""
echo "Status API: https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com/status"
echo "Reset (admin): https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com/reset"
echo ""
echo "Share this URL with participants!"
echo ""
