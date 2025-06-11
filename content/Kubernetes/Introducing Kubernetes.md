
# Kubernetes in a nutshell

Kubernetes is a software system for automating the deployment and management of complex. large scale application systems composed of computer processes running in containers

## Abstracting away the Infrastructure

The deployment of applications goes through Kubernetes and not directly to individual computers.  What Kubernetes does is hide the underlying hardware from users and applications.  As an analogy sits on top of computer hardware, so that as operators and developers we only see Kubernetes and not the gory details going on under the hood. Kubernetes standardizes the way that applications are deployed. All the underlying differences in hardware are handled by Kubernetes

## Deploying Applications Declaratively

Kubernetes uses a declarative model to define an application.  You describe the components that make up the application that make up the application and Kubernetes turns the description into a running application.

When a change to the definition of the application Kubernetes will take the necessary steps to reconfigure the running application. As soon as the application is deployed to Kubernetes, Kubernetes takes over the daily management of the application.  If the application fails, Kubernetes takes care of it, if there is a hardware failure Kubernetes will take care of that. What Kubernetes does is handle the is take care of the details which allows system operators to focus on the big picture

