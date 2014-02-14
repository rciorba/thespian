Thespian [![Build Status](https://travis-ci.org/rciorba/thespian.png?branch=master)](https://travis-ci.org/rciorba/thespian)
============
Thespian implements a simple __Actor Model__ for concurrency, using multiprocessing.
Actors have an inbox they'll consume messages from.
Actors communicate with other actors by sending messages to their inbox.
Sending messages will block if the recieving actor's inbox is full.
