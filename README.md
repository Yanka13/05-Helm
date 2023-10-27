# Airflow Kubernetes Deployment Guide

This document provides a step-by-step guide for deploying Apache Airflow on a Kubernetes cluster. The instructions are meant to be executed in order, each command fulfilling a specific part of the setup and configuration process.

```bash
# Create a new namespace for the Airflow deployment
kubectl create namespace $AIRFLOW_NAMESPACE

# Set the current context to the newly created namespace
kubectl config set-context --current --namespace=airflow

# Create secrets for encrypting sensitive data
kubectl create secret generic airflow-fernet-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__CORE__FERNET_KEY
kubectl create secret generic airflow-webserver-secret-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__WEBSERVER__SECRET_KEY
kubectl create secret generic airflow-pg-password --namespace="$AIRFLOW_NAMESPACE" --from-literal=password=$POSTGRES_PASSWORD
kubectl create secret generic airflow-pg-user --namespace="$AIRFLOW_NAMESPACE" --from-literal=username=$POSTGRES_USER

# Apply the PostgreSQL configuration to the cluster
kubectl apply -f postgres.yaml --namespace=airflow

# Copy a database file to the PostgreSQL pod and execute it to set up the database
kubectl cp f1db.sql postgres-statefulset-0:f1db.sql
kubectl exec postgres-statefulset-0 -- psql -f f1db.sql --user=airflow f1

# Install Airflow using the official Helm chart
helm install \
  "$AIRFLOW_NAME" \
  airflow-stable/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --version "8.6.1" \
  --values ./helm-values.yaml

# Retrieve the manifest of the installed Airflow release
helm get manifest $AIRFLOW_NAME > outputs.yaml   
```

## Understanding the Airflow Pods

Once the above steps are executed successfully, you'll notice several pods running in your Kubernetes cluster, each serving a unique purpose in the Airflow deployment:

1. airflow-cluster-db-migrations
Handles database migrations ensuring the database schema is up-to-date with the Airflow version being deployed.

2. airflow-cluster-pgbouncer
Manages and optimizes PostgreSQL database connections using PgBouncer, a connection pooler.

3. airflow-cluster-scheduler
Runs the Airflow scheduler monitoring all tasks and DAGs, and triggering task instances based on their schedules.

4. airflow-cluster-sync-users
Likely responsible for syncing user accounts and permissions within Airflow.


5. airflow-cluster-triggerer
Manages the triggering of jobs as a new component introduced in Airflow 2.0 and above.

6. airflow-cluster-web
Runs the Airflow webserver providing the web UI for monitoring and managing the Airflow environment.
