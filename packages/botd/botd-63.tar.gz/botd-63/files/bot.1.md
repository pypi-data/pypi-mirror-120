% BOT(1) BOTLIB version 130
% Bart Thate 
% Aug 2021

# NAME
BOT - pure python3 irc bot

# DESCRIPTION

BOT is a pure python3 IRC chat bot that can run as a background daemon for
24/7 a day presence in a IRC channel, it can be used to display RSS
feeds, act as a UDP to IRC relay and you can program your own commands for it.

BOT an attempt to achieve OS level integration of bot technology directly
into the operating system. A solid, non hackable bot version, that can offer
"display in your irc channel" functionality to the unix programmer. BOT
runs on both BSD and Linux, is placed in the Public Domain, and, one day,
will be the thing you cannot do without ;]

# SYNOPSIS

| bot \<cmd>\ [options] [key=value] [key==value]
 
# CONFIGURATION
| bot cfg server=localhost channel=\#bot nick=bot
| bot m=irc,rss
| bot pwd \<nick\> \<password\>
| bot cfg password=\<outputofpwd\>
| bot cfg users=true 
| bot met \<userhost\>
| bot rss \<url\>

# OPTIONS
| -b	\# bork mode
| -c	\# start client
| -d	\# daemon mode
| -v	\# use verbose
