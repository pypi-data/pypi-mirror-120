#!/bin/bash
# gcp-show-my-undeleted-searches.sh: This script shows my undeleted searches in
# AWS and their status
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Tue 17 Aug 2021 09:57:27 PM EDT

set -euo pipefail
shopt -s nullglob

#gcloud config get-value core/account
#gcloud config get-value core/project
#gcloud config get-value compute/region
#gcloud config get-value compute/zone

#gcloud container clusters list --filter=resourceLabels.owner=$USER
for r in `gcloud container clusters list --filter=resourceLabels.owner=$USER --format='value(resourceLabels.results)' | sort `; do
    results=$(echo $r | sed 's,---,://,')
    if [[ "$r" =~ "elasticblast-$USER" ]]; then
        results=$(echo $r | sed "s,---,://,;s,$USER.,$USER/,")
    fi
    echo $results
    elastic-blast status --results $results
done
