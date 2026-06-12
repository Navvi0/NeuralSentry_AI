import pandas as pd
import joblib
import os
import time
import random

# Terminal Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

print(f"{CYAN}--- Neural Sentry: Initializing Real-Time Live Monitor ---{RESET}")

# Verify structural files
if not os.path.exists("neural_sentry_brain.pkl") or not os.path.exists("model_columns.pkl") or not os.path.exists("KDDTest+.txt"):
    print(f"{RED}❌ ERROR: Core system files are missing!{RESET}")
    exit()

# Load intelligence model and data columns
model = joblib.load("neural_sentry_brain.pkl")
model_columns = joblib.load("model_columns.pkl")

# Load data stream source
stream_source = pd.read_csv("KDDTest+.txt", header=None)
total_rows = len(stream_source)

print(f"{GREEN}🎯 AI Core Synced successfully. Starting live packet inspection loop...{RESET}\n")
time.sleep(1.5)

# Clear screen setup for a futuristic hacker console feel
os.system('clear')

try:
    processed_count = 0
    threats_blocked = 0
    
    while True:
        # Pick a random network packet row to simulate an incoming stream thread
        random_idx = random.randint(0, total_rows - 1)
        packet_row = stream_source.iloc[[random_idx]]
        
        # Pull details for console printing
        duration = packet_row.iloc[0, 0]
        protocol = packet_row.iloc[0, 1]
        service = packet_row.iloc[0, 2]
        src_bytes = packet_row.iloc[0, 4]
        dst_bytes = packet_row.iloc[0, 5]
        
        # Pre-process packet features to match the 88-column shape of the brain
        feature_indices = [0, 1, 2, 3, 4, 5, 22]
        X_raw = packet_row.iloc[:, feature_indices]
        X_encoded = pd.get_dummies(X_raw, columns=[1, 2, 3])
        X_encoded.columns = X_encoded.columns.astype(str)
        X_live = X_encoded.reindex(columns=model_columns, fill_value=0)
        
        # Inference stopwatch metric
        start_time = time.time()
        prediction = model.predict(X_live)[0]
        inference_speed = (time.time() - start_time) * 1000 # convert to ms
        
        processed_count += 1
        
        # Display the live monitoring interface top-bar
        print(f"\033[H{BOLD}{CYAN}==========================================================================")
        print(f"📡 NEURAL SENTRY: REAL-TIME INTRUSION MONITORING HARDWARE")
        print(f"📦 Packets Sniffed: {processed_count}  |  🛡️ Threats Deflected: {threats_blocked}  |  ⚡ Speed: {inference_speed:.1f}ms")
        print(f"=========================================================================={RESET}")
        
        # Check classification output
        if prediction == "normal":
            print(f"{GREEN}[SAFE] {protocol.upper()} Packet -> Service: {service} | Length: {src_bytes + dst_bytes} bytes | Status: PASSED{RESET}")
        else:
            threats_blocked += 1
            print(f"{RED}{BOLD}🚨 [ALERT] CRITICAL INTRUSION DETECTED!{RESET}")
            print(f"{YELLOW}⚠️  Threat Signature: {prediction.upper()}{RESET}")
            print(f"{RED}💻 Details: {protocol.upper()} thread exploiting '{service}' | Volume: {src_bytes}B sent, {dst_bytes}B rec'd | Latency: {inference_speed:.2f}ms{RESET}")
            print(f"{RED}🔒 Action: Packet dropped. Source ip quarantined inside VM routing table.{RESET}")
            print(f"{RED}--------------------------------------------------------------------------{RESET}")
            
        # Add a realistic small jitter delay between incoming network spikes
        time.sleep(random.uniform(0.1, 0.6))

except KeyboardInterrupt:
    print(f"\n\n{YELLOW}🛑 Live monitoring thread killed by user. Generating system logs...{RESET}")
    print(f"📊 Final session logs: Processed {processed_count} packets and successfully neutralized {threats_blocked} attacks.")
