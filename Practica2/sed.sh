#!/bin/bash

regexp=$1
replacement=$2

sed "s/#*$regexp/$replacement/" < /etc/ssh/sshd_config > /etc/ssh/sshd_config1

cp /etc/ssh/sshd_config1 /etc/ssh/sshd_config

rm /etc/ssh/sshd_config1

systemctl restart sshd
