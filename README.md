[![Stories in Ready](https://badge.waffle.io/PrettyTrue/noctis.png?label=ready&title=Ready)](https://waffle.io/PrettyTrue/noctis)
# Noctis
Open source production pipeline.

## About
When we think about pipeline management we generally turn to big companies doing big things with big data however that doesn't mean we should limit our concepts of infrastructure to just the largest of us. This project is built on the belief that pipeline design and asset management doesn't have to be reserved for the heavy hitters.

### Purpose
To connect the most intense elements of a production pipeline together and help manage them with minimal impact to the artist (always the most important part). The Noctis realm can be divided into a few major components.

- Tracking and the Ticket System
- Asset Handling (Physical data)
- Application Distribution
- Package Control

One thing to truly strive for in this project is universal access from any of the major operating distributions. Currently Noctis is developed on a co-Linux-Windows environment with light testing being done a OSX. If others would like to test the limitations of any of these systems that would be much obliged.
 
#### Tracking and the Ticket System
This is in part handled by the Noctis engine (Django) as well as a slight I/O component. We need to keep all of our data in oder. Unlike most environments however we want the ability to keep our assets moving to any place in particular without giving up even a hint of security.

#### Asset Handling
When we deal with an open source concept like Noctis we have to be prepared for many possible requirements of the parts and pieces that make up the heart of our data. Keeping assets managed both simple and reachable we can obtain quite a bit of information without bogging down the system.

#### Application Distribution
In an effort to exonerate the 'open source movement' Noctis will always try to handle projects using software available to everyone. Using proprietary software only where truly needed/supplied by another source. Internal networks using their own packages to work alongside this environment are welcome to use whatever they would like of course.

#### Package Control
Noctis will eventually have other support packages to run alongside the applications interacting with it. This includes resource management, tracking/status updating, etc.

### Development Setup
See the wiki for more detailed instructions (Coming soon...) however the prerequisites are:
```
Vagrant
Virtual Box
Git
```
Once you have the three of those, you just need to run `vagrant up` on the Vagrantfiles in the vagrants directory and follow the instructions they spit out.

This package was built using Python3.4.X. If all is compatible with Python2.7.X I would be delighted but that may not be possible.