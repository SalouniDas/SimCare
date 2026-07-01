# SimCare: Voice‑Controlled Robotics for Assisted Living 🤖🎙️

```{=html}
<p align="center">
```
`<img src="https://readme-typing-svg.demolab.com?font=Ubuntu&weight=600&size=22&pause=1200&color=3B82F6&center=true&width=900&lines=SimCare+-+Voice-Controlled+Robotics+for+Assisted+Living;ROS2+%7C+Whisper+%7C+Webots+%7C+Navigation2;Intelligent+Assistive+Robotics+for+Smart+Living" />`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu)
![Webots](https://img.shields.io/badge/Simulation-Webots-1F2937)

```{=html}
</p>
```
## Overview

SimCare is a simulated assistive robotics platform developed to explore
how voice interaction, autonomous navigation, and smart‑home automation
can work together in assisted living scenarios.

The system combines: - Speech recognition using Whisper - Intent
understanding - ROS2 communication - Autonomous navigation using Nav2 -
Simulation using Webots

## Features

-   🎙️ Voice command interface\
-   🧭 Autonomous room navigation\
-   🏠 Smart environment interaction\
-   🚨 Simulated emergency alert workflow\
-   🔔 Medication reminder scenarios

------------------------------------------------------------------------

## System Architecture

``` text
User Voice
   ↓
Whisper Node
   ↓
Intent Mapping
   ├── Navigation (Nav2)
   ├── Device Control
   └── Alert Actions
```

------------------------------------------------------------------------

## Tech Stack

  Category     Technology
  ------------ --------------
  Robotics     ROS2 Humble
  Navigation   Nav2
  Mapping      Cartographer
  Speech       Whisper
  Simulation   Webots
  Languages    Python, Bash

------------------------------------------------------------------------

## Project Structure

``` text
SimCare/
├── turtlebot3_webots_bringup/
├── whisper_cmd/
├── launch/
├── scripts/
└── docs/
```

------------------------------------------------------------------------

## Installation

``` bash
cd ~/ros2_ws/src
git clone https://github.com/SalouniDas/SimCare.git
```

Install dependencies:

``` bash
pip install openai-whisper sounddevice pyttsx3 numpy
```

Build:

``` bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

------------------------------------------------------------------------

## Run

Start simulation:

``` bash
ros2 launch turtlebot3_webots_bringup full_sim_bringup.launch.py
```

Start assistant:

``` bash
ros2 run whisper_cmd whisper_node
```

------------------------------------------------------------------------

## Example Commands

-   "Hello Robot"
-   "Go to the fridge"
-   "Switch on the light"
-   "Open the door"
-   "Call for help"

------------------------------------------------------------------------

## Results

Current project scope focuses on simulation and research validation of
voice‑driven assistive robotics.

## Roadmap

-   [ ] Multimodal interaction
-   [ ] Better intent recognition
-   [ ] Real robot deployment
-   [ ] Cloud telemetry

## License

MIT License

## Author

**Salouni Das**\
Master's in AI & Robotics
