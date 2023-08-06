% BOT(1) BOTD version 64
% Bart Thate 
% Sep 2021

# NAME

**bot** - pure python3 IRC bot

# SYNOPSIS

 bot \<cmd\> \[key=value\] \[key==value\] 
    
# DESCRIPTION


**bot** is an attempt to achieve OS level integration of bot technology 
directly into the operating system. A solid, non hackable bot, that can 
offer "display in your irc channel" functionality to the unix programmer.
It runs under systemd and rc.d as a 24/7 background service that starts the
bot after reboot, stores it's data as JSON files on disk, every object is
timestamped, readonly of which the latest is served to the user layer. This
bot is intended to be programmable in a static, only code, no popen, no
importing from directories, way that makes it suitable for embedding.

**bot** is placed in the Public Domain, no Copyright, no LICENSE.

# IRC

IRC configuration is done with the use of the botctl program, the cfg
command configures the IRC bot.

> $ bot cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

default channel/server is #botd on localhost.

# SASL

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this.

> $ bot pwd \<nickservnick\> \<nickservpass\>

after creating you sasl password add it to you configuration.

> $ bot cfg password=\<outputfrompwd\>

# USERS

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

> $ bot cfg users=True

> $ bot met \<userhost\>

# RSS

if you want rss feeds in your channel install feedparser.

> $ sudo apt install python3-feedparser

add a url to the bot and the feed fetcher will poll it every 5 minutes.

> $ bot rss <url>

# FILES

| bin/bot
| man/man1/bot.1.gz

# AUTHOR

Bart "botfather" Thate <bthate67@gmail.com>

# SEE ALSO

| https://botd.io
| https://botd.rtfd.io
| https://pypi.org/project/botd
