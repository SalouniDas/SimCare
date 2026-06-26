<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Ubuntu&weight=600&size=22&pause=1200&color=3B82F6&secondaryColor=FFFFFF&vCenter=true&center=true&width=850&lines=SimCare%3A+Voice-Controlled+Robotic+Assistance+%F0%9F%A4%96%F0%9F%8E%99%EF%B8%8F;Bridging+the+gap+between+multimodal+AI+and+autonomous+navigation.;An+intelligent%2C+voice-activated+assistive+robotic+system." alt="Typing SVG" />
</p>
---

## 🚀 Overview
**SimCare** is an intelligent, voice-activated assistive robotic workspace designed for ambient assisted living environments. By integrating localized automatic speech recognition (ASR) via **OpenAI's Whisper model** with **ROS 2 Navigation (Nav2)** and **Webots simulations**, the platform allows users to manage spatial home configurations and emergency calls via natural verbal cues[cite: 11, 16, 17]. 
It helps elderly or mobility-limited users by responding to natural voice commands to:
- Navigate rooms
- Control devices (lights, AC, TV, etc.)
- Open doors
- Send emergency or doctor alerts
- Provide reminders and monitor vitals
  
---
## 🛠️ System Architecture

The architecture functions through two primary custom modular subsystems:

[ Spoken Audio ] ──> (Whisper Node) ──[ Intent Mapping ] ──> /cmd_vel (Twist)
│                                 └──> Nav2 Actions
└─────────[ Shell Pipelines ] ──> Device Automation / Logs


1. **`whisper_cmd` (Voice Engine)**[cite: 17]: Operates a continuous thread using `sounddevice` to stream raw ambient microphone streams. It runs local inference via the Whisper language engine to map spoken words into semantic intents or coordinate actions.
2. **`turtlebot3_webots_bringup` (Physical Simulation)**[cite: 12, 17]: Instantiates a complete digital twin environment featuring autonomous SLAM via Cartographer mapping, hardware kinematic transforms, and pathfinding models.

---

## 📦 Workspace Features & Logic Breakdown

### 🤖 Core Intelligence (`whisper_node.py`)
- **Wake Word Logic**: Remains idle until triggered by saying `"hello robot"` or `"hey robo"`[cite: 16].
- **Spatial Destination Tracking**: Directs the TurtleBot3 directly to exact mapped locations (e.g., *fridge, sofa, table, cabinet, or door*) using `nav2_msgs` Action Servers[cite: 16].
- **Peripheral Hardware Overrides**: Translates voice queries into native subprocess shell paths to toggle physical rooms or appliances (TV, Radio, Light, AC) while generating tracking telemetry logs[cite: 1, 16].
- **Adaptive Safety Monitoring**: Actively tracks the `/vital_status` telemetry topic[cite: 16]. If abnormal data is captured, it triggers vocal overrides and spins up safety scripts to alert medical services.
- **Medication Alarms**: Runs daemon cron timers to audibly nudge patients at precise intervals (`08:00`, `13:14`, `20:00`)[cite: 16].

---

## 🚀 Tech Stack

- **Frameworks:** ROS2 (Robot Operating System), Nav2
- **AI/ML:** OpenAI Whisper, NLP Keyword Intent Parsing
- **Simulation:** Webots / Gazebo
- **Languages:** Python, C++

---
## 📦 Installation & Setup

### Prerequisites
- Ubuntu 22.04 LTS equipped with **ROS 2 (Humble Hawksbill)**[cite: 17]
- System dependencies:
  ```bash
  sudo apt install ros-humble-desktop ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3-apps
- ROS2 (Humble or newer)
- Nav2 & Simulation packages

## Project Structure
### ROS 2 Packages:
- `whisper_cmd/`: main ROS2 package which handles real-time voice recognition and command execution.
- `launch/` – simulation launch files, launches full Webots simulation for TurtleBot3 including SLAM and navigation.
### Core Nodes:
- `whisper_node.py`: Main node for handling all voice commands using Whisper and controlling robot actions.

### Bash Scripts:
- Device controls: `switch_on_ac.sh`, `switch_on_light.sh`, `switch_on_tv.sh`, `switch_on_radio.sh`
- Emergency: `send_help_alert.sh`
- Doctor call: `call_doctor.sh`
- Door interaction: `open_door.sh`

---


## How to Run
1. Start the Webots TurtleBot3 simulation:
```bash
ros2 launch turtlebot3_webots_bringup full_sim_bringup.launch.py
```
2. Run the voice assistant:
```bash
ros2 run whisper_cmd whisper_node
```
3. Example command:
"Go to the kitchen"
"Switch on the light"
"Call the doctor"
