from lib.inventory import Inventory
from lib.varmap import Varmap
from string import Template
import argparse

parser = argparse.ArgumentParser(
    description='This script generates the swift ring-making scripts')

parser.add_argument('-i', dest='inventory_file',
    required=True,
    help='specify the inventory file path')

args = parser.parse_args()

inv = Inventory(args.inventory_file)
var = Varmap('group_vars/storage')

# comments
scripts = [
    '#!/bin/bash',
    '',
    'cd roles/swift-ring-holder/files/',
    '',
    'rm -f *.builder *.ring.gz backups/*.builder backups/*.ring.gz',
    '',
]

cmd = Template('swift-ring-builder ${type}.builder add r1z${zone}-${ip}:${port}/${device} ${weight}')
servers = inv.groups['storage']
# object builder

scripts.append('swift-ring-builder object.builder create 15 1 1')
object_port = var.data['object_port']
for host in servers:
    scripts.append(
        cmd.substitute(type='object', zone=1,
            ip=servers[host], port=object_port, device='sdb', weight=100)
    )
scripts.append('swift-ring-builder object.builder rebalance')
scripts.append(' ')

# container builder
scripts.append('swift-ring-builder container.builder create 15 3 1')
container_port = var.data['container_port']
for host in servers:
    scripts.append(
        cmd.substitute(type='container', zone=1,
            ip=servers[host], port=container_port, device='sdb', weight=100)
    )
scripts.append('swift-ring-builder container.builder rebalance')
scripts.append(' ')

# account builder
scripts.append('swift-ring-builder account.builder create 15 3 1')
account_port = var.data['account_port']
for host in servers:
    scripts.append(
        cmd.substitute(type='account', zone=1,
            ip=servers[host], port=account_port, device='sdb', weight=100)
    )
scripts.append('swift-ring-builder account.builder rebalance')
scripts.append(' ')

scripts = [line + '\n' for line in scripts]

with open('remakerings.sh', 'w') as f:
    f.writelines(scripts)


