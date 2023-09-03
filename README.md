# Darklab peasant

![Peasant Icon](documentation/assets/icon.png)

project to get me into gov queue

# Description

You may find this project useful because it gives example of configuring running Python as
- AWS Lambda
  - in event bridge (cron analong)
  - via docker image deployment method

- as Celery in AWS ECS
  - in private network
  - with bastion access to debug it

# Debugging ECS cluster stuff

- terragrunt output bastion_private_key > ~/.ssh/darklab.peasant.production.bastion.pem
- chmod 400 ~/.ssh/darklab.peasant.production.bastion.pem
- add to ~/.ssh/config:
Host peasant-prod-bastion
   HostName 34.246.194.191
   User ec2-user
   IdentityFile ~/.ssh/darklab.peasant.production.bastion.pem

Host peasant-prod-cluster
   HostName 10.0.2.24
   User ec2-user
   IdentityFile ~/.ssh/darklab.peasant.production.bastion.pem
   ProxyCommand ssh peasant-prod-bastion -W $(echo %h|cut -d- -f2):%p

- change `34.246.194.191` to your own bastion public ip
- change `10.0.2.24` to private ip of cluster EC2 host
- access with `ssh peasant-prod-bastion` or `ssh peasant-prod-cluster``
