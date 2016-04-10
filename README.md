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

#### Tracking and the Ticket System
This is in part handled by the Noctis engine (Django) as well as a slight I/O component. We need to keep all of our data in oder. Unlike most environments however we want the ability to keep our assets moving to any place in particular without giving up even a hint of security.

#### to be continued...


### Development Setup
See the wiki for more detailed instructions however the prerequisites are:
```
Vagrant
Virtual Box
Git
```
Once you have the three of those, you just need to run `vagrant up` on the Vagrantfiles in the vagrants directory and follow the instructions they spit out.

This package was built using Python3.4.X. If all is compatible with Python2.7.X I would be delighted but that may not be possible.