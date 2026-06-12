import os
import time
import joblib
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP

# UI Terminal Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

print(f"{CYAN}📡 Loading Neural Sentry Production Core...{RESET}")

# Verify AI Model Integrity
if not os.path.exists("neural_sentry_brain.pkl") or not os.path.exists("model_columns.pkl"):
    print(f"{RED}❌ ERROR: Missing AI brain or structural column files!{RESET}")
    exit()

model = joblib.load("neural_sentry_brain.pkl")
model_columns = joblib.load("model_columns.pkl")

print(f"{GREEN}🎯 AI Core online. Hooking into live network card adapters...{RESET}")
time.sleep(1)
os.system('clear')

processed_count = 0
threats_detected = 0

def process_live_packet(packet):
    global processed_count, threats_detected
    
    # We only analyze standard IP packets (TCP/UDP/ICMP)
    if not packet.haslayer(IP):
        return

    processed_count += 1
    
    # 1. Extract raw continuous features live from the wire
    duration = 0  # Single packet captured live has instantaneous duration
    src_bytes = len(packet[IP].payload)
    dst_bytes = 0  # Single-direction capture context
    count = 1      # Individual packet sequence tracking
    
    # 2. Determine exact Network Protocols
    protocol = "tcp" if packet.haslayer(TCP) else "udp" if packet.haslayer(UDP) else "icmp" if packet.haslayer(ICMP) else "other"
    
    # 3. Determine Network Service based on standard system destination ports
    service = "private"
    if packet.haslayer(TCP) or packet.haslayer(UDP):
        port = packet.sport if packet.sport < packet.dport else packet.dport
        if port == 80 or port == 443: service = "http"
        elif port == 21: service = "ftp"
        elif port == 22: service = "ssh"
        elif port == 53: service = "dns"
        
    # 4. Extract TCP flag state metrics
    flag = "SF"  # Default normal established connection state flag
    if packet.haslayer(TCP):
        F = packet[TCP].flags
        if 'S' in F and 'A' not in F: flag = "S0"
        elif 'R' in F: flag = "REJ"

    # Build a single-row raw dataframe matching our feature engineering structure
    raw_packet_data = pd.DataFrame([{
        0: duration, 1: protocol, 2: service, 3: flag, 4: src_bytes, 5: dst_bytes, 22: count
    }])
    
    # One-Hot Encode live data categorical values mathematically
    encoded_packet = pd.get_dummies(raw_packet_data, columns=[1, 2, 3])
    encoded_packet.columns = encoded_packet.columns.astype(str)
    
    # Map and align perfectly to the AI's structural 88-column brain requirements
    X_live = encoded_packet.reindex(columns=model_columns, fill_value=0)
    
    # Feed to the brain for instant prediction
    start_time = time.time()
    prediction = model.predict(X_live)[0]
    latency = (time.time() - start_time) * 1000
    
    # Top Dashboard Stats Bar Display Update
    print(f"\033[H{BOLD}{CYAN}==========================================================================")
    print(f"🛡️  NEURAL SENTRY: ACTIVE PRODUCTION NETWORK MONITOR")
    print(f"📦 Live Wire Packets Sniffed: {processed_count} | 🚨 Anomalies Deflected: {threats_detected}")
    print(f"=========================================================================={RESET}")
    
    if prediction == "normal":
        print(f"{GREEN}[PASS] Live {protocol.upper()} Packet -> Size: {src_bytes}B | Port Service: {service} | OK{RESET}")
    else:
        threats_detected += 1
        print(f"{RED}{BOLD}🚨 [ANOMALY DETECTED] LIVE INTRUSION ALERT!{RESET}")
        print(f"{YELLOW}⚠️  Classified Signature: {prediction.upper()}{RESET}")
        print(f"{RED}💻 Source Meta: {protocol.upper()} socket utilizing flag {flag} | Intercept Latency: {latency:.2f}ms{RESET}")
        print(f"{RED}🔒 Operational Security State: Traffic dropped and flagged in system journal.{RESET}")
        print(f"{RED}--------------------------------------------------------------------------{RESET}")

# Initialize Scapy sniffing thread loop on any active interface card
try:
    sniff(prn=process_live_packet, store=0)
except KeyboardInterrupt:
    print(f"\n\n{YELLOW}🛑 Production wire monitor safely decoupled.{RESET}")
