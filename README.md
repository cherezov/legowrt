# Curiosity Mars LegoEV3 Rover
This project was made for my son, who asked me to make possible wireless control his Lego Mindstorm EV3 robot from PC.
Below is the log of what was done, what is needed to be done and several notes and instructions.

## General idea
![legowrt idea](images/legowrt.jpg)

## Requirements
* Rover shall has a camera eye and image shall be visible on laptop
* Rover shall be controlled via joystick connected to a laptop
* Rover shall be controlled via laptop keyboard
* Notebook and rover shall communicate wirelessly (e.g via wifi)

## Hardware
* WiFi router and PC or laptop (my with CentOS 7)
* [Lego Mindstorms](https://www.lego.com/mindstorms/)
* Micro SDHC card with [ev3dev image](http://www.ev3dev.org/docs/getting-started/)
* [TP-Link TL-MR3020 router with OpenWRT onboard](https://wiki.openwrt.org/toh/tp-link/tl-mr3020)
* UVC webcam ([check list here](http://www.ideasonboard.org/uvc/))
* Arduino UNO board
* Servos
* Joystick 
* USB hub
* USB-miniUSB cord

## Plan and progress and thoughts
- [ ] ~Connect Lego EV3 Brick to wifi network~ **Note:** this requires WiFi dongle and will occupy single USB port
- [x] Connect MR3020 board to EV3 Brick with [USB reverse tethering](#USB-reverse-tethering)
- [x] Setup [port forwarding from MR3020 to EV3](#Port-forwarding-from-MR3020-to-EV3) Brick
- [x] Run python listening server on EV3 Brick and teset connection from laptop 
- [x] Make same test with WebCamera and EV3 Brick connected to MR3020 board via USB hab
- [x] Connect joystick to laptop
- [x] Find out a way to code joystick: pygame is quite good!
- [x] Develop python3 listenening server for EV3 Brick
- [x] Code [client side application](src/client)
- [x] Add auto configuration usb0 interface on MR3020 board [configure DHCP?](http://en.qi-hardware.com/wiki/Ethernet_over_USB#Editing-the-Host's-Network-Configuration)
- [x] Run server app as daemon at runtime
- [ ] Inernet access for MR3020 brick and/or auto update listening server

## Installation
* Setup OpenWRT to [TP-Link TL-MR3020](https://wiki.openwrt.org/toh/tp-link/tl-mr3020)
* Setup [ev3dev](http://www.ev3dev.org/docs/getting-started/) for Lego EV3 Brick
* todo..

## Configuration notes
### USB reverse tethering
This simply requires additional package to install on MR3020 board
```shell
> opkg update
> opkg install kmod-usb-net-cdc-ether
> reboot
```
More info about [OpenWRT usb reverse tethering](https://wiki.openwrt.org/doc/howto/usb.reverse.tethering)

EV3 brick part is described [here](http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/)

### Wires
USB Hub -> 3020 USB port  
Ev3 brick mini USB -> USB hub  
UVC camera -> USB hub  
3020 mini USB -> external power bank  

### Add ssh publick keys access
to /etc/dropbear/authorized_keys

### Port forwarding from MR3020 to EV3
Port forwarding is described in ```/etc/config/rinetd``` 

```
> ifconfig usb0 169.254.233.100
```

Restart **rinetd**
```
> /etc/init.d/rinetd restart
```

Test connection:
```
> ssh robot@169.254.233.76
```
pass:maker  
link: http://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/

### Ev3 root password
```
> sudo passwd
```
pass: maker

### Forward to UART
3020 is listening on TCP port 2000 and forwards data to UART  
Following line will redirect command to UART using CLI over the network
```
sudo echo 'any command' | nc <3020 ip address> 2000
```

### Forward to ev3dev
ev3dev is listening on port 8080  
3020 is listening on port 88 and redirects to ev3dev:8080
```
sudo echo 'any command' | nc <3020 ip address> 88
```

### Auto start ev3dev serv
Add to /etc/rc.local
```
python3.4 /usr/local/bin/ev3server.daemon.py start
```

