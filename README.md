# Security Group Firewall Exercise

The goal of this exercise is to replicate AWS security group rules to a
host-based firewall running on Linux.

Develop a script in a language such as bash or Python to run on an Linux AWS
EC2 instance. The script should call the AWS API through `awscli` or through a
library such as `boto3` to obtain the security group rules associated with that
instance, then modify the firewall on the instance to permit ingress/egress
based on those rules. You may implement the rules using the host-based firewall
software of your choosing such as `iptables`, `nftables`, or `firewalld`, but
the firewall should take into account protocols (i.e. TCP, UDP, ICMP), ports,
and source or destination CIDRs. In the event the security group rule
references another security group, you may substitute VPC CIDR for the
instance. For simplicity, you may assume that all rules are IPv4.

## Example

Suppose that the EC2 instance is in a VPC with CIDR 10.123.321.0/24 and has the
following security group rules from one or more security groups:

Inbound security group rules

| Protocol | Port Range | Source    |
| -------- | ---------- | --------- |
| ICMP     | All        | sg-123456 |
| TCP      | 22         | 0.0.0.0/0 |
| TCP      | 443        | sg-987654 |

Outbound security group rules

| Protocol | Port Range | Destination     |
| -------- | ---------- | --------------- |
| ICMP     | All        | sg-123456       |
| TCP      | 80         | 0.0.0.0/0       |
| TCP      | 443        | 0.0.0.0/0       |
| TCP      | 53         | 9.9.9.9/32      |
| UDP      | 53         | 9.9.9.9/32      |
| TCP      | 8000-8100  | 10.112.223.0/24 |

These security group rules could generate the following `iptables` commands:

```bash
iptables -A INPUT -p icmp -s 10.123.321.0/24 -j ACCEPT
iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -s 10.123.321.0/24 --dport 443 -j ACCEPT

iptables -A OUTPUT -p icmp -d 10.123.321.0/24 -j ACCEPT
iptables -A OUTPUT -p tcp -d 0.0.0.0/0 --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp -d 0.0.0.0/0 --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -d 9.9.9.9/32 --dport 53 -j ACCEPT
iptables -A OUTPUT -p udp -d 9.9.9.9/32 --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp -d 10.112.223.0/24 --dport 8000:8100 -j ACCEPT
```

**Remember:** We're evaluating your design and development skills based on the
code you give us. Make sure it reflects the type of code you'd write on a
production software system for us. Take your time. If these instructions are
unclear, rather than ask for clarification, list your assumptions and work from
them.