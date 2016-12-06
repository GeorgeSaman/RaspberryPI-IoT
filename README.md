# RaspberryPI-IoT
An IoT project utilizing RS232(UART),FLASK,MYSQL and rendering a website on a RPI.

##Index

* What you need?
* Introduction



## What you need?
* RaspberryPI with access to a network.
* USB to RS232 cable.

##Introduction
This project uses RaspberryPI 3 to host a website from which it receives and records data/commands and send them serially using UART.
Meaning you can **control** a machine that receives serial commands **remotely**. 
> In this repository the RPI is controlling an **Automated Carousel**.

The diagram below illustrates the system in which the RPI is embedded in,
![System_Overview](/System_Overview.png?raw=true "System Overview")

The RPI will:
* In normal mode..
  * Pass serial data from Chromeleon to the Carousel.
* In debug mode..
  * Pass serial data from the website to the Carousel.
  
