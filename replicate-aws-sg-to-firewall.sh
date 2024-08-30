#! /bin/bash

## Assumptions:
##  1 awscli is installed and up to date
##  2 jq is installed and up to date
##  3 

usage () {
    echo "hello usage"
}

query_ec2_sg () {
    echo "Get the security group info!"
    aws ec2 describe-security-group-rules
}

modify_firewall () {
    echo "modify the firewall!"
}

main () {
    query_ec2_sg
    modify_firewall
    echo "profit"
}

main