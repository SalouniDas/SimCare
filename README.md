# SimCare: Voice‑Controlled Robotics for Assisted Living 🤖🎙️

<p align="center"> <img src="https://readme-typing-svg.demolab.com?font=Ubuntu&weight=600&size=22&pause=1200&color=3B82F6&secondaryColor=FFFFFF&vCenter=true&center=true&width=850&lines=SimCare%3A+Voice-Controlled+Robotics+for+Assisted+Living+%F0%9F%A4%96%F0%9F%8E%99%EF%B8%8F;Bridging+the+gap+between+multimodal+AI+and+autonomous+navigation.;An+intelligent%2C+voice-activated+assistive+robotic+system." alt="Typing SVG" /> </p>
```
![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu)
![Webots](https://img.shields.io/badge/Simulation-Webots-1F2937)

----

## Overview
SimCare is an intelligent, voice-activated assistive robotic system developed to explore
how voice interaction, autonomous navigation, and smart‑home automation
can work together in assisted living scenarios.

It helps elderly or mobility-limited users by responding to natural voice commands to: 
- Navigate rooms autonomously
- Control household devices (lights, AC, TV, radio)
- Actuate smart entries (doors)
- Send automated emergency or doctor alerts
- Provide critical medication reminders and monitor vitals

----

## Features

-   🎙️ Voice command interface\
-   🧭 Autonomous room navigation\
-   🏠 Smart environment interaction\
-   🚨 Simulated emergency alert workflow\
-   🔔 Medication reminder scenarios

----

## 🛠️System Architecture

The architecture functions through two primary custom modular subsystems:
```text
[ Spoken Audio ] ──> (Whisper Node) ──[ Intent Mapping ] ──> /cmd_vel (Twist)
│                                      └──> Nav2 Actions
└─────────[ Shell Pipelines ] ──> Device Automation / Logs
```
1. **whisper_cmd (Voice Engine)**: Operates a continuous thread using sounddevice to stream raw ambient microphone feeds. It runs local inference via the Whisper language model to map spoken words into semantic intents or coordinate actions.
2. **turtlebot3_webots_bringup (Physical Simulation)**: Instantiates a complete digital twin environment featuring autonomous SLAM via Cartographer mapping, hardware kinematic transforms, and pathfinding models.

----

## 📦 Workspace Features & Logic Breakdown 
### 🤖 Core Intelligence (whisper_node.py) 
- **Wake Word Logic**: Remains idle until triggered by saying "hello robot" or "hey robo".
- **Spatial Destination Tracking**: Directs the TurtleBot3 directly to exact pre-mapped coordinates (e.g., *fridge, sofa, table, cabinet, or door*) using nav2_msgs Action Servers.
- **Peripheral Hardware Overrides**: Translates voice queries into native subprocess shell paths to toggle physical rooms or appliances (TV, Radio, Light, AC) while generating tracking telemetry logs.
- **Adaptive Safety Monitoring**: Actively tracks the /vital_status telemetry topic. If abnormal data is captured, it triggers vocal overrides and spins up safety scripts to alert medical services.
- **Medication Alarms**: Runs daemon cron timers to audibly nudge patients at precise intervals (08:00, 13:14, 20:00).

----

## 🛠️ Tech Stack & Prerequisites

- **Frameworks**: ROS2 (Humble or newer), Nav2, Cartographer SLAM
- **AI/ML**: OpenAI Whisper (Base model), NLP Keyword Intent Parsing, PyTTSx3 (TTS Engine)
- **Simulation**: Webots / Gazebo   Languages: Python, C++, Bash
- **OS Requirement**: Ubuntu 22.04 LTS

----

## Project Structure

``` text
SimCare/
├── turtlebot3_webots_bringup/       # Simulation package 
│   └── launch/
│       └── full_sim_bringup.launch.py  # Launches full Webots simulation, SLAM & navigation 
└── whisper_cmd/                     # Voice interaction package 
    ├── whisper_cmd/
    │   └── whisper_node.py          # Main speech-to-intent tracking node 
    └── scripts/                     # External automation shell scripts 
        ├── switch_on_ac.sh, switch_on_light.sh, switch_on_tv.sh, switch_on_radio.sh
        ├── send_help_alert.sh, call_doctor.sh 
        └── open_door.sh
```

----

## 🚀 Installation & Setup

### 🏗️ Build the Workspace
1. Clone the repository into your ROS2 workspace source folder:
``` bash
cd ~/ros2_ws/src
git clone [https://github.com/SalouniDas/SimCare.git](https://github.com/SalouniDas/SimCare.git)
```

2. Install the required Python dependencies:
```bash
pip install openai-whisper sounddevice pyttsx3 numpy tf-transformations
```

3. Build the workspace packages using colcon:
``` bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 🖥️ How to Run
1. Start the Webots TurtleBot3 simulation environment:
``` bash
ros2 launch turtlebot3_webots_bringup full_sim_bringup.launch.py
```

2. In a secondary terminal, launch the voice assistant engine:
``` bash
ros2 run whisper_cmd whisper_node
```

3. Optionally test text commands directly via ROS2 topics:
```bash
ros2 topic pub /voice_commands std_msgs/String "data: 'move forward'"
```
----

## Example Commands

-   "Hello Robot"
-   "Go to the fridge"
-   "Switch on the light"
-   "Open the door"
-   "Call for help"
-   "What time is it?"

----

## 📊 Telemetry Logs   
The system automatically records persistent logs for tracking and diagnostics:
- Device Actions: Checked and updated via device_log.txt
- Emergency Alerts: Logged to emergency_log.txt
- Doctor Alerts: Logged to doctor_alert_log.txt

----

## Author

**Salouni Das**\
Master's in AI & Robotics
