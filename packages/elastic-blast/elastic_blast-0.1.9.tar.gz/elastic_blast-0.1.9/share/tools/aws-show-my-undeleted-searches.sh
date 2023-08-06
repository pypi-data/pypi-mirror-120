#!/bin/bash
# aws-show-my-undeleted-searches.sh: This script shows my undeleted searches in
# AWS and their status
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Sat 07 Aug 2021 11:01:46 AM EDT

set -euo pipefail
shopt -s nullglob

aws sts get-caller-identity

for results in `aws batch describe-compute-environments --output json | \
                jq -Mr ".computeEnvironments[] | select(.tags.creator==\"$USER\") | .tags.results" | sort`; do
    echo $results
    b=`basename $results`
    elastic-blast status --results $results
done
