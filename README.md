# mesosphere-dcos-demo-application

A simple app to demonstrate the following DC/OS features.

* VIP based layer4 load balancing for presenting the FE app to access both BE apps.
* Marathon-LB to publish the FE app to the outside world and make it accessible via a vhost.
* TLS/SSL termination
* HTTP health check.
* Deployment constraints to unique hosts.
* Deploying Marathon apps as a group, with dependencies.

## Architecture ##

Please note the apps are baked into Docker images hosted off my personal Docker hub account, Dockerfiles are included if you wish to rebuild and host on your own Docker registry.

View this as a 2 layer application, with a front end (FE) website that calls on a back end (BE) API layer.

**BE**
* 2 instances of the the BE container deployed on unique private agents.
* A VIP address configured `demo-be-app.marathon.l4lb.thisdcos.directory:5000` which round robins to both BE apps on their container IP:port
* A Python Flask site presenting information from /.

**FE**
* 2 instances of the FE container deployed and configured
* A Marathon-LB backend called demo-fe-app which is exposed as vhost named test.example.com on both Marathon LB public agent address over TCP/80.
* A Python Flask site which connects to the BE VIP address and pulls in the content served by the BE apps.
* The FE app code performs a string replace to change the words Back with Front and present that information.


**Diagram & Walthrough**

<p align="center">
  <img src="https://github.com/aggress/mesosphere-dcos-demo-application/blob/master/demo_application_architecture.png?raw=true" alt="Demo Application Architecture"/>
</p>

1. Using cURL or a browser the user navigates to http://test.example.com.
2. Marathon-LB has test.example.com configured as a vhost and has a backend called demo-fe-app which contains both demo-fe-app container IP addresses and ports. It opens a connection to one.
3. The FE app opens a TCP connection to the VIP address for the BE apps.
4. The VIP address round robins to both BE apps and provides a connection to one.
5. THe BE app serves the content back to the FE app which then serves it back through Marathon-LB to the user.
6. With `HAPROXY_0_REDIRECT_TO_HTTPS":"true"` the site is automatically redirected to HTTPS.


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

This will deploy the following groups if they don't already exist:

* demo-team
  * back-end-service
     * demo-be-app
  * front-end-service
     * demo-fe-app


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

