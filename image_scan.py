#! /usr/local/bin/python3

import boto3
import time
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
      description='imagescan - scan a container image in ECR')

    parser.add_argument('-r', '--retries', action='store', default=15, type=int,
                        required=False, help='number of retries when waiting for image scan to complete')
    parser.add_argument('-n', '--repositoryname', action='store',
                        required=True, help='name of repository')
    parser.add_argument('-e', '--endpoint', action='store',
                        required=True, help='endpoint of registry')
    parser.add_argument('-i', '--imagetag', action='store',
                        required=True, help='id of container image')
    parser.add_argument('-c', '--cvecount', action='store', default=15, type=int,
                        required=True, help='threshold of high cve findings')

    args = parser.parse_args()

    exit_code = 0

    try:
        exit_code = scan(args.endpoint, args.repositoryname,
                         args.imagetag, args.retries, args.cvecount)
    except Exception as e:
        print(e)
        exit_code = 1
    finally:
        sys.exit(exit_code)


def scan(endpoint, repositoryName, imagetag, retries, cvecount):

    parsed_endpoint = endpoint.split('.')
    registry = parsed_endpoint[0]
    region = parsed_endpoint[3]

    client = boto3.client('ecr', region_name=region)

    status_code = 0
    tries = 0

    print(f'Doing CVE scan of {repositoryName}:{imagetag} in registry {endpoint}')

    while tries < retries:

        response = client.describe_image_scan_findings \
            (registryId=registry, repositoryName=repositoryName,
             imageId={'imageTag': imagetag}, maxResults=1000)

        status = response['imageScanStatus']['status']

        if status == 'IN_PROGRESS':
            time.sleep(60)
            tries += 1
            continue
        elif status == 'COMPLETE':
            if response['imageScanFindings']['findingSeverityCounts']['HIGH'] >= cvecount:
                status_code = 1
                print('CVE findings failed by policy')
                print(response['imageScanFindings']['findingSeverityCounts'])
            else:
                print('CVE findings permitted by policy')
            break
        else:
            # scan failed, so can't flag container image as bad
            break

    return status_code


if __name__ == '__main__':

    main()
