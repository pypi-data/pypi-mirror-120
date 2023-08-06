% BOTD(1) BOTD version 57
% Bart Thate 
% Aug 2021

# NAME
**BOTD** - 24/7 channel daemon

# SYNOPSIS

| botctl \<cmd>\ \[options\] \[mod=mod1,mod2\] \[key=value\] \[key==value\]

# DESCRIPTION

**BOTD** is a pure python3 IRC chat bot that can run as a background daemon for
24/7 a day presence in a IRC channel, it can be used to display RSS
feeds, act as a UDP to IRC relay and you can program your own commands for it.

**BOTD** an attempt to achieve OS level integration of bot technology directly
into the operating system. A solid, non hackable bot version, that can offer
"display in your irc channel" functionality to the unix programmer. **BOTD**
runs on both BSD and Linux, is placed in the Public Domain, and, one day,
will be the thing you cannot do without ;]

# INSTALL

 | sudo pip3 install botd && sudo systemctl enable botd \-\-now

 | * default channel/server is #botd on localhost

# CONFIGURATION

| botctl cfg server=localhost channel=\#bot nick=bot

| botctl cfg users=true 
| botctl met \<userhost\>

| botctl pwd \<nick\> \<password\>
| botctl cfg password=\<outputofpwd\>

| botctl rss \<url\>

FILES
=====

| bin/botctl
| bin/botd
| man/man8/botd.8.gz
| man/man8/botctl.8.gz
| lib/systemd/system/botd.service
| etc/rc.d/botd

COPYRIGHT
=========

**BOTD** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate 

SEE ALSO
========

https://pypi.org/project/botd
