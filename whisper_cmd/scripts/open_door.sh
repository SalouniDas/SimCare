#!/bin/bash
echo "Door opened at $(date)" >> ~/scripts/device_log.txt
paplay /usr/share/sounds/freedesktop/stereo/complete.oga
