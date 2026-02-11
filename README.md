# AuraNet Home Network Protection

Network-wide ad blocker and parental controls for Raspberry Pi.

## Features

- Blocks ads and trackers on ALL devices
- Blocks malware and phishing sites
- Optional parental controls (adult, social media, gambling, gaming)
- Easy web dashboard
- No software to install on phones/tablets

## Protection Modes

| Mode | Blocks |
|:-----|:-------|
| Kids | Adult, social, gambling, gaming, malware, ads |
| Family | Adult, gambling, malware, ads |
| Standard | Malware, ads, trackers |

## Requirements

- Raspberry Pi 4 (2GB+)
- 32GB+ SD card
- Pi-hole v6
- Python 3 + Flask

## Quick Install

1. Install Pi-hole:curl -sSL https://install.pi-hole.net | bash

2. Clone this repo:
git clone https://github.com/AuraNet-AU/auranet-dashboard.git ~/auranet_dashboard

3. Install Flask:
sudo apt install python3-flask sqlite3 -y

4. Start the service:
sudo systemctl enable auranet
sudo systemctl start auranet

5. Access dashboard:
http://auranet-hub.local:8080

## Commands

| Task | Command |
|:-----|:--------|
| Restart | `sudo systemctl restart auranet` |
| View logs | `sudo journalctl -u auranet -f` |
| Update blocklists | `sudo pihole -g` |

## Version

1.0.0

## License

Proprietary - AuraNet Australia
