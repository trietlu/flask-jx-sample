#! /bin/bash

high_findings=$(aws ecr describe-image-scan-findings --repository-name trietlu/flask-jx-sample --image-id imageTag=0.0.0-SNAPSHOT-PR-1-3 --region us-east-2 --max-items 50 --page-size 50 | jq '.imageScanFindings.findingSeverityCounts.HIGH')
if [ $high_findings -gt 50 ]
then
  echo Bad 
  exit 0
else 
  echo Good 
  exit 1
fi
