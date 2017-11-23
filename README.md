# mesosphere-dcos-demo-application

A simple back-end (BE) and front-end (FE) appl to demonstrate the following DC/OS features

* VIP based layer4 load balancing for presenting the BE to the FE
* Marathon-LB usage to publish the FE app to the outside world
* HTTP health check
* Deployment to unique hosts

## Architecture ##

**BE**
* 2 instances of the the BE container are deployed on unique private agents.
* A VIP address is configured to round robin between them `demo-be-app.marathon.l4lb.thisdcos.directory:5000`.
* A Python Flask site presents host level information from /.

**FE**
* 2 instances of the FE container are deployed and configured to expose themselves via Marathon LB.
* A Marathon-LB backend is configured with both FE containers, exposed via the public agents on TCP/10004.
* A Python Flask site connects to the BE VIP address and pulls in the information presented.
* The code then performs a string replace to change the words Back with Front and present that information.



## Usage ##

**Requirements**

A running DC/OS cluster with a minimum of 2 public agents and 2 private agents

1. Check out this repository and navigate to it.
1. Install Marathon-lb if not already installed `$ dcos package install marathon-lb`.
1. Launch the BE app with `$ dcos marathon app add demo-be-app-marathon.json`.
1. Launch the FE app with `$ dcos marathon app add demo-fe-app-marathon.json`.
1. Navigate to the DC/OS UI > Service to view the applications and confirm they're running and healthy.
1. Find the public IP address of one of your public agents and open in a browser http://<publicIP>:10004/ to see the following. Refresh the browser to see the hostname information change as both BE apps are called.

````
Front end application demo
Start Time	2017-Nov-23 13:43:26
Hostname	1fe8a1417897
Local Address	172.17.0.2
Remote Address	10.0.3.20
Server Hit	56
````

Let's check one of the back end applications

1. Find the IP of one private agent running a BE app from the UI > services > demo-be-app.
1. Get shell on the private agent `$ dcos node ssh --master-proxy --private-ip=<IP>`.
1. Find one of the BE app container's port, it'll look like 0.0.0.0:23352 `$ docker ps | grep demo-be`.
1. Curl the container directly to see the back end output `curl http://0.0.0.0:23352/` Note it'll say *Back end application demo* rather than *Front*.

## HAProxy statistics ##

These are accessible from each Marathon-LB instance on their public IP http://<publicIP>:9090/haproxy?stats
