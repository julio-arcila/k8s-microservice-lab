# 01 — Cluster Setup & Monitoring

## Goal
Set up a local k3d Kubernetes cluster optimized for learning on limited hardware.

## Prerequisites
- Docker installed
- k3d installed (`yay -S k3d` or `curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash`)
- kubectl installed

## Step 1: Create the cluster

```bash
k3d cluster create ai \
  --servers 1 \
  --agents 1 \
  --k3s-arg "--disable=traefik,metrics-server,local-storage,servicelb@server:*" \
  --k3s-arg "--bind-address=0.0.0.0@server:*" \
  --k3s-node-label "type=worker@agent:*" \
  --k3s-node-label "type=master@server:*"
```

**What this does:**
- Creates 1 server + 1 worker node
- Disables unnecessary services (Traefik, ServiceLB, etc.) to save RAM
- Binds API to all interfaces so workers can join
- Labels nodes for scheduling control

## Step 2: Verify

```bash
kubectl get nodes -o wide
```

Expected output:
```
NAME              STATUS   ROLES                  AGE   VERSION
k3d-ai-agent-0    Ready    <none>                 20s   v1.31.5+k3s1
k3d-ai-server-0   Ready    control-plane,master   26s   v1.31.5+k3s1
```

## Step 3: Install Monitoring

```bash
# Metrics Server (for kubectl top)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# k9s terminal UI
curl -sL "https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz" | tar xz -C ~/.local/bin k9s

# Test
kubectl top nodes
k9s
```

## Lessons Learned

1. **Bind address matters** — without `--bind-address=0.0.0.0`, worker nodes can't join
2. **Resource awareness** — on 11GB RAM, disable unused k3s components
3. **DNS is fragile** — manual coredns changes break RBAC; let k3s manage it
4. **Storage provisioners** — k3d has no default; use `emptyDir` for learning labs
