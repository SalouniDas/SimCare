#!/bin/bash
echo "Doctor alert triggered at $(date)" >> ~/scripts/doctor_alert_log.txt
paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga
