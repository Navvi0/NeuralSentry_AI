# NeuralSentry_AI

**Argus** is an autonomous intrusion detection and monitoring system built to analyze network traffic patterns in real-time. Designed specifically for privacy-focused environments such as Parrot OS, this project focuses on distinguishing routine local network activity from potential malicious anomalies using custom-trained machine learning models.

## Why This Project?
I developed NeuralSentry to address the growing concern of digital privacy and the intimidation factor of enterprise-grade security tools. Many users hesitate to browse freely due to the fear of installing unintentional malware or having their personal data harvested by cloud-based monitors.

My goal was to create a tool that runs entirely local to your system, ensuring that no network traffic logs or sensitive data are ever sent to an external cloud server. It is designed to be lightweight, transparent, and easy to deploy for users who need robust security without the complexity of traditional corporate software.

## Technical Overview
The system is built on a modular Python architecture designed to handle packet capture and analysis with minimal overhead:

* **Packet Capture:** Utilizes `scapy` to sniff traffic on the specified network interface in real-time.
* **Data Processing:** Uses `pandas` and `numpy` to normalize raw packet data into a structured format suitable for machine learning.
* **Detection Engine:** Employs classification models (Random Forest/SVM) to identify behavioral anomalies.
* **Environment:** Developed and optimized for Linux-based distributions, specifically tested on Parrot OS.

## Requirements
* **Python 3.x**
* **Dependencies:** `scapy`, `pandas`, `numpy`, `scikit-learn`
* **Privileges:** Root/Sudo access is required to capture raw network packets.

## Setup
To get the project running, follow these commands in your terminal:

```bash
# 1. Clone the project
git clone https://github.com/Navvi0/NeuralSentry_AI.git
cd NeuralSentry_AI

# 2. Set up the virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the monitor
# Identify your network interface first by running 'ip link show'
sudo python3 main.py -i <your_interface_name>
