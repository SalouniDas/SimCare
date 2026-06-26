import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import String
from geometry_msgs.msg import Twist, PoseStamped
from nav2_msgs.action import NavigateToPose

import whisper
import sounddevice as sd
import numpy as np
import pyttsx3
import re
from datetime import datetime, time
from threading import Timer, Thread
from tf_transformations import quaternion_from_euler
import time as systime
import subprocess
from queue import Queue

class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.emergency_pub = self.create_publisher(String, 'emergency_alert', 10)
        self.create_subscription(String, 'vital_status', self.vitals_callback, 10)

        self.model = whisper.load_model("base")
        self.tts = pyttsx3.init()
        self.speech_queue = Queue()
        Thread(target=self.speech_loop, daemon=True).start()

        self.get_logger().info("Whisper model loaded. Waiting for wake word...")

        self.named_goals = {
            "light": {"x": 2.39, "y": 0.04, "yaw": -1.54},
            "door": {"x": -0.96, "y": -1.96, "yaw": 3.12},
            "ac": {"x": 1.82, "y": -6.07, "yaw": -3.01},
            "fridge": {"x": -0.17, "y": 3.57, "yaw": 3.03},
            "table": {"x": 0.91, "y": -1.81, "yaw": 0.03},
            "cabinet": {"x": 2.64, "y": -3.56, "yaw": -0.18},
            "sofa": {"x": 2.01, "y": -1.71, "yaw": 0.11},
            "tv": {"x": 1.5, "y": -2.5, "yaw": 0.0},
            "radio": {"x": 0.5, "y": -3.0, "yaw": 1.57}
        }

        self.awaiting_command = False
        self.last_interaction_time = systime.time()
        self.pending_action = None

        self.start_idle_checker()
        self.start_medication_reminders()
        self.say_greeting()

        Thread(target=self.listen_loop, daemon=True).start()

    def speech_loop(self):
        while True:
            text = self.speech_queue.get()
            self.get_logger().info(f"🔊 {text}")
            self.tts.say(text)
            self.tts.runAndWait()

    def say(self, text):
        self.speech_queue.put(text)

    def say_greeting(self):
        now = datetime.now().hour
        if 5 <= now < 12:
            self.say("Good morning! Ready to help you today.")
        elif 12 <= now < 18:
            self.say("Good afternoon! Let me know if you need anything.")
        else:
            self.say("Good evening! I'm here if you need me.")

    def start_idle_checker(self):
        def check_idle():
            while rclpy.ok():
                systime.sleep(60)
                if systime.time() - self.last_interaction_time > 300:
                    self.say("Let me know if you need me.")
                    self.last_interaction_time = systime.time()
        Thread(target=check_idle, daemon=True).start()

    def start_medication_reminders(self):
        def check_time():
            while rclpy.ok():
                now = datetime.now().strftime("%H:%M")
                if now in ["08:00", "13:14", "20:00"]:
                    self.say("Time for your medication.")
                    systime.sleep(60)
                systime.sleep(30)
        Thread(target=check_time, daemon=True).start()

    def listen_loop(self):
        duration = 6
        fs = 16000

        while rclpy.ok():
            self.get_logger().info("🎧 Listening...")
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()

            audio_np = np.squeeze(audio)
            result = self.model.transcribe(audio_np, fp16=False)
            command = result["text"].strip().lower()

            if not re.search(r"[a-zA-Z]", command):
                self.get_logger().info("⚠️ No speech detected.")
                continue

            self.get_logger().info(f"📝 Transcribed: {command}")
            self.last_interaction_time = systime.time()

            if "hello robot" in command or "hey robo" in command:
                self.say("Yes, I'm listening.")
                cleaned_command = re.sub(r"(hello robot|hey robo)[,\.]?", "", command).strip()
                if cleaned_command:
                    self.handle_command(cleaned_command)
                else:
                    self.awaiting_command = True
                continue

            if self.awaiting_command:
                self.handle_command(command)
                self.awaiting_command = False
            else:
                self.get_logger().info("🛌 Waiting for 'hello robot' wake command.")

    def handle_command(self, command):
        twist = Twist()

        if "forward" in command:
            twist.linear.x = 0.2
            self.cmd_pub.publish(twist)
            self.say("Moving forward.")
        elif "backward" in command:
            twist.linear.x = -0.2
            self.cmd_pub.publish(twist)
            self.say("Moving backward.")
        elif "left" in command:
            twist.angular.z = 0.5
            self.cmd_pub.publish(twist)
            self.say("Turning left.")
        elif "right" in command:
            twist.angular.z = -0.5
            self.cmd_pub.publish(twist)
            self.say("Turning right.")
        elif "stop" in command:
            self.cmd_pub.publish(Twist())
            self.say("Stopping.")
        elif "go to the" in command or "come to the" in command:
            for name in self.named_goals:
                if name in command:
                    if "come to the" in command:
                        self.say(f"Coming to the {name}")
                    else:
                        self.say(f"Going to the {name}")
                    self.navigate_to(name)
                    return
            self.say("I don't know that location.")
        elif "open the door" in command:
            self.pending_action = "open_door"
            self.navigate_to("door")
        elif "switch on" in command:
            for device in ["ac", "light", "tv", "radio"]:
                if device in command:
                    self.pending_action = f"switch_on_{device}"
                    self.navigate_to(device)
                    return
            self.say("I don't recognize that device.")
        elif "remind me" in command:
            if re.search(r"remind me to .+ in \d+", command):
                self.handle_reminder(command)
            else:
                self.say("Please tell me what to remind you and when.")
                self.awaiting_command = True
        elif "what time" in command or "what is the time" in command:
            now = datetime.now().strftime("%I:%M %p")
            self.say(f"The time is {now}")
        elif "help" in command or "call for help" in command:
            self.say("Alert! Calling for help now.")
            self.trigger_help()
        elif "how are you" in command:
            self.say("I'm doing great, thank you for asking!")
        elif "what can you do" in command:
            self.say("I can move, navigate to locations, tell you the time, remind you of tasks, and more!")
        else:
            self.say("I did not understand that command.")

    def handle_reminder(self, command):
        match = re.search(r"remind me to (.+?) in (\d+)\s*(second|seconds|minute|minutes)?", command)
        if match:
            task = match.group(1).strip()
            amount = int(match.group(2))
            unit = match.group(3) or "seconds"
            delay = amount * 60 if 'minute' in unit else amount

            self.say(f"Okay, I will remind you to {task} in {amount} {unit}.")
            Timer(delay, lambda: self.say(f"⏰ Reminder: It is time to {task}.")).start()
        else:
            self.say("I couldn't understand the reminder. Please say something like: remind me to drink water in 10 seconds.")

    def trigger_help(self):
        emergency_msg = String()
        emergency_msg.data = "Emergency! Help requested by voice command."
        self.emergency_pub.publish(emergency_msg)
        self.get_logger().warn("🚨 Emergency alert published on /emergency_alert")

        try:
            subprocess.Popen(["/home/rucha/scripts/send_help_alert.sh"])
            self.get_logger().info("📲 External emergency script triggered.")
        except Exception as e:
            self.get_logger().error(f"Failed to run help script: {e}")

    def call_doctor(self):
        try:
            subprocess.Popen(["/home/rucha/scripts/call_doctor.sh"])
            self.get_logger().info("📞 Doctor alert script triggered.")
        except Exception as e:
            self.get_logger().error(f"Failed to run doctor call script: {e}")

    def vitals_callback(self, msg):
        data = msg.data.lower()
        self.get_logger().info(f"📡 Vitals received: {data}")
        if "abnormal" in data or "alert" in data:
            self.say("Warning, abnormal vitals detected. Calling your doctor now.")
            self.call_doctor()

    def run_device_script(self, device):
        script_path = f"/home/rucha/scripts/switch_on_{device}.sh"
        try:
            subprocess.Popen([script_path])
            self.get_logger().info(f"💡 Device control script triggered: {script_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to run {device} script: {e}")

    def navigate_to(self, location):
        goal = self.named_goals[location]
        goal_msg = NavigateToPose.Goal()

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = goal["x"]
        pose.pose.position.y = goal["y"]
        q = quaternion_from_euler(0, 0, goal["yaw"])
        pose.pose.orientation.x, pose.pose.orientation.y = q[0], q[1]
        pose.pose.orientation.z, pose.pose.orientation.w = q[2], q[3]

        goal_msg.pose = pose

        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            self.say("Navigation server not available.")
            self.get_logger().error("Navigation server not available.")
            return

        self.get_logger().info(f"Sending goal to {location} at {goal['x']}, {goal['y']}")
        send_goal_future = self.nav_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(lambda future: self._goal_response_callback(future, location))

    def _goal_response_callback(self, future, location):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.say("I couldn't go there.")
            self.get_logger().error("Goal was rejected by server.")
            return

        self.get_logger().info("Goal accepted. Waiting for result...")
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(lambda r: self._goal_result_callback(r, location))

    def _goal_result_callback(self, future, location):
        status = future.result().status
        if status == 4:
            if self.pending_action:
                if self.pending_action.startswith("switch_on_"):
                    device = self.pending_action.split("_")[2]
                    self.say(f"{device.upper()} switched on now.")
                    self.run_device_script(device)
                elif self.pending_action == "open_door":
                    self.say("Opening the door now.")
                self.pending_action = None
            else:
                self.say(f"I have reached the {location}")
        else:
            self.say(f"Failed to reach the {location}")

def main(args=None):
    rclpy.init(args=args)
    node = WhisperNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("🛑 Shutting down whisper node.")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

