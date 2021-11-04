# Swarming Your Server for Fun and Profit: A Locust Primer
_Adapted from Dr. Dionisio's materials from previous semesters_

This document aims to provide startup instructions for getting a [Locust](https://locust.io) setup running. The first part of the instructions are actually generic for installing and using one or more third-party Python libraries (similar to what `npm` or `yarn` do for Node). After that, we will get into Locust proper.

## Installation and Setup
First and foremost, you’ll need Python 3. Presumably most students already have this installed due to other courses that they have taken, but if this has not applied to you yet, then now is the time. Python is prevalent enough that there should be plenty of resources on the web for how to install it on any given operating system.

Python has a module called `venv` (short for “virtual environment”) which allows developers to create a local Python environment where third-party libraries can exist without having to modify the system-level Python installation. This is similar to how having a _node_modules_ folder in a JavaScript code base allows libraries and packages to be installed there without modifying the overall system.

To initialize a local Python environment, run this at the top of your repository:

    python3 -m venv env

This will initialize the environment and create a folder called _env_. This folder is specific to the development machine and should _not_ be committed to the repository (thus it is listed in _.gitignore_).

To begin working within this environment, run this before starting to work (also while at the top of your repository):

    source env/bin/activate

This “activates” the environment so that you can now install libraries in the local setup without having the change the global one. You can tell when `virtualenv` is active by checking if `(env)` precedes your command line prompt. When `(env)` is on, you can now install Locust:

    pip install locust

It is important that you run `pip install` strictly _after_ you have set up and activated the virtual environment, because otherwise, Python will attempt to install the package _globally_ and this is generally no longer viewed as a recommended practice.

More detailed installation instructions are available on https://docs.locust.io/en/stable/installation.html (including specific instructions for different operating systems). These might be helpful if you run into any issues following the simplified instructions here.

Once installed, there is no need to install again for that repository. Only `source env/bin/activate` needs to be invoked per work session. To “disconnect” from the environment, type:

    deactivate
    
You will notice how, when the environment is inactive, you can’t run or use Locust because you’re “outside” the environment at that point.

## Preparing the Locust File
This repository has a _locustfile.py_ with comments to help in understanding how to set things up.

The concept is this: for the service that you want to load test, you define a _task set_ that implements the range of network requests and transactions that you would like to perform on the service being tested. The requests and transactions are things you expect might cause your service stress or throw exceptions when overloaded with requests. Each _task_ in the set performs a network operation and reports its results. Locust’s function is to invoke those tasks multiple times by simulating serveral users, thus creating a “swarm” of requests on your network service and recording how it holds up.

Locust works fine on a single machine but can really ramp things up with distributed execution. We don’t cover that here but if you’re interested in how that would work, you can consult https://docs.locust.io/en/stable/running-locust-distributed.html for details (and extra credit will be given to those who successfully perform a distributed Locust test)

## Running Locust
Once everything is set up, you can download the files in this repository to try out (and debug) your _locustfile.py_. Simply activate the virtual environment (`source env/bin/activate`) then starting Locust:

    locust

The Locust server will start and you can now initiate tests with however many concurrent users you want to observe and the spawn rate–how many new users instanciated per second. The Locust server starts a web server at port 8089 (meta alert—note how Locust is itself a type of custom network service) so at this point you should open a browser at http://localhost:8089 or http://127.0.0.1:8089. You should be greeted by this page:

![Locust opening page](./primer-images/locust-opening.png)

Make sure your network service is running, then at this point, you can enter how many users to simulate, how quickly to spawn them, and the host running your service. Click _Start swarming_ and away it goes.

During the swarm, you can see on-going results in the web app. Console output will also likely appear for both Locust and your service being tested. You might also find it useful to have your network service produce some console output in case you uncover bugs at this point or just want a full picture of what’s going on.

The following screenshots illustrate the tabular, graphical, and error output of an on-going Locust swarm on an instance of Dr. Toal’s capitalization server:

![Locust stats page](./primer-images/locust-stats.png)
![Locust charts page](./primer-images/locust-charts.png)
![Locust failures page](./primer-images/locust-failures.png)

The _Download Data_ tab has links from which you can download the CSV versions of the data or a nice report you are asked to submit for this activity.

There are two other example Locust files named _babylocustfile.py_, based on the Hello World from the documentation, and _locustfile-sample.py_ from a helpful Stack Overflow post. These are for reference only. These are not quite ready for prime time. BabyLocust issues http requests to our non-http capitalization service, but it works and you can see why it's failing and what error messages you get. The locustfile-sample has a placeholder print statement where you would need to implement connecting to your own service and simulating a realistic request. If you would like to adapt and try them out for this activity, you would rename your current _locustfile.py_ something else (to save it!!) and then rename the file you want Locust to run instead to _locustfile.py_

## Show No Mercy!
Have fun with Locust, and don’t hesitate to max things out (briefly) to see what happens. Using Locust (especially in distributed mode) offers you some perspective on what happens in a production network environment. It gives you a real sense for the finiteness of the resources we’re using. Even if those limits are indeed somewhat large in practice, the limits are still there.
