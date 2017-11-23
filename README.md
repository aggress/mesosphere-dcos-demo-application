# mesosphere-dcos-demo-application

A simple back-end (BE) and front-end (FE) app to demonstrate the following DC/OS features.

* VIP based layer4 load balancing for presenting the FE app to access both BE apps
* Marathon-LB to publish the FE app to the outside world and make it accessible via a vhost
* HTTP health check
* Deployment constraints to unique hosts

## Architecture ##

Please note the apps are baked into Docker images hosted off my personal Docker hub account, Dockerfiles are included if you wish to rebuild and host on your own Docker registry.

**BE**
* 2 instances of the the BE container deployed on unique private agents.
* A VIP address configured `demo-be-app.marathon.l4lb.thisdcos.directory:5000` which round robins to both BE apps on their container IP:port
* A Python Flask site presenting information from /.

**FE**
* 2 instances of the FE container deployed and configured
* A Marathon-LB backend called demo-fe-app which is exposed as vhost named test.example.com on both Marathon LB public agent address over TCP/80.
* A Python Flask site which connects to the BE VIP address and pulls in the content served by the BE apps.
* The FE app code performs a string replace to change the words Back with Front and present that information.


## Usage ##

**Requirements**

* A minimum of 2 public and 2 private agents
* Marathon-LB installed on both public agents
* This repository checked out locally

**Deploy as individual Marathon applications**

1. Add the BE app with `$ dcos marathon app add demo-be-app-marathon.json`.
1. Add the FE app with `$ dcos marathon app add demo-fe-app-marathon.json`.

**Deploy as a group**

1. Add both the BE & FE apps as a group, with the BE being a dependency for the FE `$ dcos marathon group add demo-app-group.json`.

This will a group structure if it doesn't exist:

demo-team
  back-end-service
    demo-be-app

  front-end-service
    demo-fe-app


**Testing**

1. Navigate to the `DC/OS UI > Service` to view the applications and confirm they're running and healthy.
1. Find the public IP addresses of both of your public agents and add to your /etc/hosts for `test.example.com`
1. In a browser navigate to `http://test.example.com`.
1. Refresh the browser to see the content change as the FE app you land on calls different BE apps serving different content.

````
Front end application demo
Start Time	2017-Nov-23 13:43:26
Hostname	1fe8a1417897
Local Address	172.17.0.2
Remote Address	10.0.3.20
Server Hit	56
````

Let's check one of the back end applications

1. Find the IP of one private agent running a BE app from `UI > services > demo-be-app`.
1. Get a shell on the private agent `$ dcos node ssh --master-proxy --private-ip=<IP>`.
1. Find one of the BE app container's port with `$ docker ps | grep demo-be` it'll look like `0.0.0.0:23352`.
1. Curl the container directly from the shell to see the BE app output `curl http://0.0.0.0:23352/` it'll say *Back end application demo* rather than *Front*.

## HAProxy statistics ##

These are accessible from each Marathon-LB instance on their public IP like `http://test.example.com:9090/haproxy?stats`

