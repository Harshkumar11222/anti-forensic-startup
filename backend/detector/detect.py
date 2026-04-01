import os
import time

def calculate_risk(suspicious_count, recent_count):
    score = 0

    # Rule based AI logic
    score += suspicious_count * 2
    score += recent_count * 1

    if suspicious_count > 20:
        score += 20

    if recent_count > 50:
        score += 10

    # limit max 100
    return min(score, 100)

def scan_system(path="C:\\Users"):
    suspicious = []
    recent_files = []
    current_time = time.time()
    deleted_traces = find_deleted_traces()
    log_issues = check_log_tampering()
    anomaly = detect_anomaly(len(suspicious), len(recent_files), log_issues)

    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)

            try:
                stat = os.stat(full_path)

                if file.endswith((".tmp", ".log", ".bak")):
                    suspicious.append(full_path)

                if file.startswith("."):
                    suspicious.append(full_path)

                if current_time - stat.st_mtime < 3600:
                    recent_files.append(full_path)

                if stat.st_mtime > current_time:
                    suspicious.append(full_path)

            except:
                continue

    risk_score = calculate_risk(len(suspicious), len(recent_files))
    
    status = "SAFE"
    if risk_score > 50:
        status = "WARNING"
    if risk_score > 80:
        status = "DANGEROUS"

    return {
        "total_suspicious": len(suspicious),
        "recent_activity": len(recent_files),
        "risk_score": risk_score,
        "status": status,
        "deleted_traces": len(deleted_traces),
        "log_issues": log_issues,
        "anomaly": anomaly,
        "sample_suspicious": suspicious[:5]
        
    }

def find_deleted_traces():
    paths = [
        "C:\\$Recycle.Bin",
        "C:\\Windows\\Temp",
        "C:\\Users"
    ]

    found = []

    for path in paths:
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith((".tmp", ".dat", ".chk")):
                        found.append(os.path.join(root, file))
        except:
            continue

    return found[:10]

def check_log_tampering():
    log_paths = [
        "C:\\Windows\\System32\\winevt\\Logs",
        "C:\\Windows\\Logs"
    ]

    issues = 0

    for path in log_paths:
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)

                    try:
                        size = os.path.getsize(full_path)

                        # suspicious: empty log file
                        if size == 0:
                            issues += 1

                    except:
                        continue
        except:
            continue

    return issues

def detect_anomaly(suspicious_count, recent_count, log_issues):
    
    anomaly_score = 0

    # pattern logic
    if suspicious_count > 50:
        anomaly_score += 30

    if recent_count > 100:
        anomaly_score += 30

    if log_issues > 10:
        anomaly_score += 40

    if anomaly_score > 70:
        return "HIGH ANOMALY ⚠"
    elif anomaly_score > 40:
        return "MEDIUM ANOMALY ⚠"
    else:
        return "NORMAL ✅"