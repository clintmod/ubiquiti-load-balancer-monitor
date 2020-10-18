#!/usr/bin/env expect

set hostname [lindex $argv 0]
spawn telnet 192.168.100.1
expect "/ #"
log_file -noappend workdir/uptime.txt
send "cat /proc/uptime \r"
expect "/ #"
log_file
send "exit\r"
expect eof
