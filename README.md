<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Ubuntu&weight=600&size=22&pause=1200&color=3B82F6&secondaryColor=FFFFFF&vCenter=true&center=true&width=850&lines=SimCare%3A+Voice-Controlled+Robotic+Assistance+%F0%9F%A4%96%F0%9F%8E%99%EF%B8%8F;Bridging+the+gap+between+multimodal+AI+and+autonomous+navigation.;An+intelligent%2C+voice-activated+assistive+robotic+system." alt="Typing SVG" />
</p>
SimCare isan intelligent, voice-activated assistive robotic system developed to bridge the gap between multimodal conversational AI and autonomous robotic navigation. The system allows users to issue natural spoken commands, which are processed in real-time to execute complex spatial tasks in a simulated environment.  
It helps elderly or mobility-limited users by responding to natural voice commands to:
- Navigate rooms
- Control devices (lights, AC, TV, etc.)
- Open doors
- Send emergency or doctor alerts
- Provide reminders and monitor vitals
  
---

## 🚀 Tech Stack

- **Frameworks:** ROS2 (Robot Operating System), Nav2
- **AI/ML:** OpenAI Whisper, NLP Keyword Intent Parsing
- **Simulation:** Webots / Gazebo
- **Languages:** Python, C++

---
## 📦 Installation & Setup

### Prerequisites
- Ubuntu 22.04 LTS (or compatible Linux environment)
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
