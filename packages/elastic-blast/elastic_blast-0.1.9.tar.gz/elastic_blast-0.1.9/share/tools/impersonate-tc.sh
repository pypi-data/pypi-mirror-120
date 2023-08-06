#!/bin/bash -xe
# Script to "impresonate" TC and delete GKE clusters that are lingering
export ELB_GCP_PROJECT=ncbi-sandbox-blast
[ $# -lt 2 ] && { echo "Usage: $0 $ELB_RESULTS $ELB_CLUSTER_NAME"; exit 1 ; }

export ELB_RESULTS=${1}
export ELB_CLUSTER_NAME=${2}

if [[ $ELB_RESULTS =~ ^gs:// ]]; then
    export ELB_GCP_ZONE=${3:-"us-east4-b"}
    export ELB_GCP_REGION=$(echo $ELB_GCP_ZONE | cut -b-8)
    export ELB_DONT_DELETE_SETUP_JOBS=1
    export KUBECONFIG=${PWD}/kubeconfig.yaml
fi

elastic-blast status --verbose --loglevel DEBUG --logfile stderr --results ${ELB_RESULTS}
elastic-blast delete --loglevel DEBUG --logfile stderr --results ${ELB_RESULTS}
