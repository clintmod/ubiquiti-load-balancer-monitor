#!/usr/bin/env expect

set hostname [lindex $argv 0]
spawn telnet 192.168.100.1
expect "/ #"
send "reboot\r"
expect eof
