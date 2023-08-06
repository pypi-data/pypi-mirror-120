# This file is placed in the Public Domain.


import bot.fnd as fnd
import bot.irc as irc
import bot.log as log
import bot.obj as obj
import bot.rss as rss
import bot.run as run
import bot.sys as sys
import bot.udp as udp

from bot.run import Table

Table.addmod(fnd)
Table.addmod(irc)
Table.addmod(log)
Table.addmod(obj)
Table.addmod(rss)
Table.addmod(sys)
Table.addmod(udp)
