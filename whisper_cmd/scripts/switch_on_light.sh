#!/bin/bash
echo "Light switched on at $(date)" >> ~/scripts/device_log.txt
paplay /usr/share/sounds/freedesktop/stereo/complete.oga
