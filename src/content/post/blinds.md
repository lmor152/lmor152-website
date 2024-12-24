---
layout: ../../layouts/post.astro
title: "Smart Home: Blind Automation"
description: Using an Arduino and Homebridge to automate my blinds
dateFormatted: Nov 30th, 2020
---

I'm a big fan of waking up to light in the morning, but I also suck at falling asleep when it's not dark. I could have bought a sunrise alarm clock and called it a day, but I decided to take the opportunity to learn a little bit more about IoT and design my own smart blinds system.

My setup uses 
- An Arduino board with a WiFi card
- 5V stepper motor 
- 12V power supply
- 3D printed gear system
- 3D printed casing
- Homebridge for coordinating it all

# Steps

1. Using [this guide](https://docs.arduino.cc/learn/electronics/stepper-motors/) I set up the Arduino to control the stepper motor.

![pic](/assets/images/projects/blinds/arduino.png)
(image from [here](https://cavecafe.medium.com/inexpensive-home-automation-for-a-lazy-guy-d30ff59369d0))

2. Since my blinds are pulled by a piece of string rather than beads, it's difficult to grab it using a plain gear. My solution to this was to use two two-tiered gears like this one: 
![pic](/assets/images/projects/blinds/gear.png)

The bottom set of teeth are longer and drive another copy of the gear, the top set of teeth are shorter and leave space for the string to feed through. This means the gears pull the string through applying pressure from both sides. I also printed a simple enclosure for the whole system.

3. The next step was to use my router to assign a fixed IP address to the Arduino board, this allows Homebridge to reliably communicate with the system.

4. I set up Homebridge using [this plugin](https://github.com/hjdhjd/homebridge-blinds-cmd) which uses a config file like the below to control the blinds system. Mine is set up to send HTTP requests to the Arduino for each type of control for the blind.

```json
   "platforms": [
     {
       "platform": "Blinds Command",

       "blinds": [
         {
           "name": "Downstairs Window Blinds",
           "manufacturer": "Somfy",
           "model": "Sonesse",
           "serial": "1234",
           "up": "/path/to/your/raise_blinds_script",
           "down": "/path/to/your/lower_blinds_script",
           "status": "/path/to/your/blinds_state_script",
           "stop": "/path/to/your/stop_blinds_script",
           "transitionInterval": 10,
           "refreshRate": 5
         }
      ]
    }
  ]
```

It was a bit finnicky to set up, especially configuring the points the motor should stop at when raising or lowering the blinds, but the whole set up only cost about $40 and has allowed me to schedule when my blinds open or close every day, and to control the remotely from my phone.

