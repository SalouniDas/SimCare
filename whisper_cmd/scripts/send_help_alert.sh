#!/bin/bash
echo "Emergency alert triggered at $(date)" >> ~/scripts/emergency_log.txt
# Optional: play a loud sound
paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga
