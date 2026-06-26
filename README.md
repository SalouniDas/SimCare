<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Ubuntu&weight=600&size=22&pause=1500&color=3B82F6&secondaryColor=FFFFFF&vCenter=true&center=true&width=800&lines=SimCare%3A+A+Simulated+Voice-Controlled+Robotic+Assistant+for+Assisted+Living+%F0%9F%A4%96%F0%9F%8E%99%EF%B8%8F;SimCare+is+an+intelligent%2C+voice-activated+assistive+robotic+system+developed+to+bridge+the+gap+between+multimodal+conversational+AI+and+autonomous+robotic+navigation." alt="Typing SVG" />
</p>
# SimCare : A Simulated Voice Controlled Robotic Assistant for Assisted Living
SimCare is a **voice-controlled assistive robot** built on **ROS 2**, **Webots**, and **OpenAI Whisper**.  
It helps elderly or mobility-limited users by responding to natural voice commands to:
- Navigate rooms
- Control devices (lights, AC, TV, etc.)
- Open doors
- Send emergency or doctor alerts
- Provide reminders and monitor vitals
  
---

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

## Requirements
- Ubuntu 22.04 + ROS 2 Humble
- Webots + TurtleBot3 simulation
- Python dependencies:
  ```bash
  pip install -r requirements.txt

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
