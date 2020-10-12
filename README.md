# ubiquiti-load-balancer-monitor

A program to monitor a multi wan setup for my Ubiquiti er-x router.


## Motivation

I'm load balancing 4 LTE modems and they are kind of flaky. 

I run the modems on a two Kasa smart power strips.

So I: 
- pull the report from the Ubiquiti er-x router
- check to see if the interface in the report is down
- check to see if the plug has been rebooted in the last 2 minutes
- reboot the modem using the Kasa smart plug api

## Requirements

- docker

## Building the image

```
make build
```

## Running the program

```
make run
```

## Running the unit tests

```
make test
```
