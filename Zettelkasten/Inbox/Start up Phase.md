
Just get things working

## Phase Scenario

- We have the source code that is managed by a development team
- We need the quickest deployment with minimal effort
- We are looking for the biggest wins with minimal required to setup
- we are learning about what needs to be maintained


In the start up phase of an application or a company
the focus is to do whatever it takes to get it online

VPS = Virtual Private Server and EC2 instance in AWS

You can ship an OS with Docker,ship an image of the VPS, want to use containers because in the future want to move to orchestrators like Kubernetes


The infrastructure that the application will run on

The foundation of the infrastructure are containers

Where to run the container

managed easy solution to get you in the door

ECS is the foundation of AWS Cloud Infrastructure, a service on top of a service

out of the box horizontal scaling, automatic restarts, vendor lookin

the fun part of deploying applications, is that you get it running but it does not mean that it is working
i got code and it is not working on my machine

I know how the application works get comfortable with the application learn how to able to maintain it and what are the parameters of the application, check the functionality of the application

i checked the application locally, now I want to migrate the application to the cloud



## the growth phase

Database migration tool written in goland called `goose` everytime that a change is made to a database , i have to create a new migration

In a database migration any change to the database schema requuires new sql statements to be written

so i want to make changes to the database schema, and if it breaks i can roll back those changes and go back to the previous state of the database 


Create my first database migration

```bash

	goose -dir "migrations" create base_schema sql

```

remember to make sure that the migrations directory is already created
after the command is ran the new database migration file `.sql` will be created in the migration folder


In the database migration file i wrote sql statements for the database when the database is up, and if anything fails i have `DROP TABLE` statements to revert the database to its previous state

Now i need to update the `.env` have to add new environment variables


### Create a Makefile

a makefile is used to make files literally, i will be using the makefile, not to make things but to run commands for us

the command to get the size of docker images stored locally

```bash

docker images --format "{{.Repository}}::{{.Tags}} {{Size}}"


```

## Optimizing the Docker Images

we want to run  the goose installer in the image

```Dockerfile
	 Run go install github.com/pressly/goose/v3/cmd/goose@latest
 
```


# Check out company pacific fusion



On another note think of a Dockerfile as a template to create an environment to run applications in

Build times and performance


In a Dockerfile the build stage can be one stage where is does everything

If you want multiple images or do multiple things then it is best to write the Dockerfile in stages


In a Dockerfile there when in a different stage you are in a different image, so anything that you want replicated has to be done again in the new stage of the build, because you are in a different image


the command in the Dockerfile downloads from a previous stage into a new stage, instead of building from scratch again in the new stage, this is an example of using cache

```Dockerfle
# build is from a previous stage
COPY --from=build /app/main
```

Deployments and infrastructure is also improving your environment and what you are working in, it also making it so that developer are working fast and and also doing complex operations and that is really the problem that I am really trying to solve. developers do not necessarily need to know what's Docker running under the hood , they just need to know the commands that are available, and that is it



## Solving the problem of secrets

- what i want to do is to create a user in Amazon Iam to authenticate with amazon and pull and push and do everything that it needs to do with amazon


### Growth Phase Transcripts

scripts
Collapse
>> Erik Reinert: Let's talk about the phase changes really quickly from thissecond phase.So we went through startup, we experienced what startup was like, andyou got to experience the pains of managing infrastructure on your own.That was super fun, right?And then in phase two, you kind of got to understand the pains of CI andlike how to set all that up and like build this developer experience, right?And basically through that, we added database migrations sodatabase databases can be securely and safely updated.Now we added a make file for developer automation,which also means that we added automation for CI too.We added a multi stage docker file for different uses.Again, that was the real takeaway I wanted you to have.There is you can make a build image that you can reuse in CI, butthen if you want to just have a very smaller production image,you can separate those two and reuse them as much as you want.We added a build step for code changes.We added a test step for schema changes, and then we added a deploy step forautomated deployments, right?Then the biggest part too is we added a lot of future support because wehave GitHub Actions in there now.Because we have a Makefile in there now.We can add more commands in the future, we can add more pipeline jobs in the future.This is that growth that I'm telling you about.It's not just growing, but we want to make sure it can continue growing.But what are the pros to this phase, this growth phase?Well, there was no real impactful changes made if you think about it, right?Like we never touched the service once, service never went down, right?And we still got tons of value out of what we did, right?It was behind the scenes, but it was still a lot of added value, right?We improved our schema management, right?We improved developer productivity,we improved code reliability as well as the life cycle with delivery jobs.Now we have a complete life cycle.Merge, merge, deploy.Merge, deploy, right?Test, merge, deploy, test, merge, deploy.That's the whole.If I was in some way to sum up, really a big part of this course,that's what you just want to get comfortable with,is what are the steps you need to do to get to your goal?I want to build, I want to test, I want to deploy, okay?In the future now I want to build, then I want to run migrations,then I want to test.We built an actual life cycle there that we can rely on.What are the cons to this?Well, we still have no infrastructure management whatsoever.If we have to go back and manage the service, it's still clunky.We still have to deal with App Runner a bit.We don't have a staging environment, sowe're deploying directly to production right now.There's no I want to check in dev and then go to prod.There's also no network isolation.So again, your database is publicly exposed as well as if you had a devenvironment, that would be publicly exposed too.There's no service support really here either.What happens in the future if we want to build another application?How would those two communicate?And how would we be able to build more of a microservice infrastructure?We can't really do that in this current setup, because it's just like App Runner.Those are the cons, basically.


## Phase Scenario

- support multiple teams
- minimal deployment friction
- longterm architected solutions
- more money to spend

### Phase Goals
- infrastructure automation
- cloud enviroments
- create promotion process
- create application observability

build the application and get it out asap build it ship it deploy it

there is always a cost and that cost is the tradeoff


main branch go to staging then go to production as off now pushing straight to production


## Terraform

State - it keeps data that is refeential to your resources, take care of state, it is how terraform keeps track of state it is important data, it can be stored in multilple places


build on the problems that i am trying to solve, figure out how to describe the environment