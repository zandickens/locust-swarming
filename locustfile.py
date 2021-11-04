"""
This file provides an example Locust setup for load-testing Dr. Toal’s sample capitalization server.
Copy this file as _locustfile.py_ for each of your services and revise the `UserBehavior` methods as
needed in order to tailor them to your service’s functionality.
"""
import socket
import time
from random import randint

from locust import Locust, TaskSet, events, task, between, User, HttpLocust, HttpUser


# The `UserBehavior` class is a subclass of `TaskSet`, defining a collection of activities that you
# would like to simulate. Each `task` takes an integer `weight` parameter which specifies the relative
# frequency of that task during the load-testing session.
#
# There appears to be a lot of code here but it’s actually pretty repetitive.
class UserBehavior(TaskSet):
    @task(7)
    def short_capitalization(self):
        start_time = time.time()
        response = ''
        try:
            # Notice that this part of the code _strongly resembles_ the network client code.
            # (well, a Python version of that code at least)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.user.host, 59898))
                sock.sendall('this is a short one\n'.encode('utf-8'))

                # We don’t need the same buffer loop here because we know how much data to expect in advance.
                response = sock.recv(1024).decode('utf-8')
                # To minimize noise, we don’t print the response, but you can certainly opt to do so while debugging.
        except Exception as e:
            # Because Locust doesn’t really know how your service is supposed to behave, reporting back to Locust
            # is also the responsibility of this code. Here, we report a failure.
            #
            # `request_type` and `name` are free-form and can be used as needed to identify the various activities
            # that the simulated user will perform.
            total_time = int(time.time() - start_time) * 1000
            events.request_failure.fire(request_type='capitalize',
                                        name='short',
                                        response_time=total_time,
                                        response_length=0,
                                        exception=e)
        else:
            # Here, we report a successful connection.
            total_time = int(time.time() - start_time) * 1000
            events.request_success.fire(request_type='capitalize',
                                        name='short',
                                        response_time=total_time,
                                        response_length=len(response))

    @task(3)
    def long_capitalization(self):
        # Fewer comments on this one because it follows the same pattern, mostly.
        start_time = time.time()
        response_length = 0  # Note the change in how we track response length.
        try:
            # Notice that this part of the code _strongly resembles_ the network client code.
            # (well, a Python version of that code at least)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.user.host, 59898))
                for i in range(randint(20, 100)):
                    sock.sendall(f'this is line {i} from a bunch\n'.encode('utf-8'))
                    response = sock.recv(1024).decode('utf-8')
                    response_length = response_length + len(response)
        except Exception as e:
            total_time = int(time.time() - start_time) * 1000
            events.request_failure.fire(request_type='capitalize',
                                        name='long',
                                        response_time=total_time,
                                        response_length=0,
                                        exception=e)
        else:
            total_time = int(time.time() - start_time) * 1000
            events.request_success.fire(request_type='capitalize',
                                        name='long',
                                        response_time=total_time,
                                        response_length=response_length)


# This is the top-level entry-point for the load-testing session.
class SocketUser(User):
    # This host is the default value; it can be overridden in the web interface.
    host = 'localhost'

    # This refers to the TaskSet subclass that is defined above.
    tasks = {UserBehavior}

    # This is the amount of time to wait between tasks.
    wait_time = between(1, 3)