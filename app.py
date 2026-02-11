from flask import Flask, render_template, flash, redirect, url_for, request
import subprocess
import json
import os
import urllib.request
import urllib.error
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-and-random-key-for-auranet'

# File to store settings
SETTINGS_FILE = os.path.expanduser('~/auranet_dashboard/settings.json')

# Pi-hole database locations
PIHOLE_GRAVITY_DB = '/etc/pihole/gravity.db'
PIHOLE_FTL_DB = '/etc/pihole/pihole-FTL.db'

# ============== REDUNDANT BLOCKLISTS ==============
CATEGORY_LISTS = {
    'adult': {
        'name': 'Adult Content',
        'description': 'Blocks pornography and adult websites',
        'icon': 'bi-eye-slash',
        'color': '#dc2626',
        'urls': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts',
            'https://blocklistproject.github.io/Lists/alt-version/porn-nl.txt',
            'https://raw.githubusercontent.com/4skinSkywalker/Anti-Porn-HOSTS-File/master/HOSTS.txt',
            'https://nsfw.oisd.nl/domainswild',
        ]
    },
    'social': {
        'name': 'Social Media',
        'description': 'Blocks Facebook, Instagram, TikTok, Twitter, Snapchat',
        'icon': 'bi-chat-dots',
        'color': '#2563eb',
        'urls': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social-only/hosts',
            'https://blocklistproject.github.io/Lists/alt-version/social-nl.txt',
        ]
    },
    'gambling': {
        'name': 'Gambling',
        'description': 'Blocks betting, casino, and gambling sites',
        'icon': 'bi-dice-5',
        'color': '#ca8a04',
        'urls': [
            'https://blocklistproject.github.io/Lists/alt-version/gambling-nl.txt',
            'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/gambling-onlydomains.txt',
        ]
    },
    'gaming': {
        'name': 'Online Gaming',
        'description': 'Blocks gaming platforms like Steam, Xbox, PlayStation',
        'icon': 'bi-controller',
        'color': '#7c3aed',
        'urls': [
            'https://blocklistproject.github.io/Lists/alt-version/gaming-nl.txt',
        ]
    },
    'malware': {
        'name': 'Malware & Phishing',
        'description': 'Blocks dangerous websites, scams, and viruses',
        'icon': 'bi-bug',
        'color': '#dc2626',
        'urls': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
            'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt',
            'https://blocklistproject.github.io/Lists/alt-version/phishing-nl.txt',
            'https://phishing.army/download/phishing_army_blocklist.txt',
            'https://blocklistproject.github.io/Lists/alt-version/malware-nl.txt',
            'https://urlhaus.abuse.ch/downloads/hostfile/',
            'https://blocklistproject.github.io/Lists/alt-version/ransomware-nl.txt',
            'https://blocklistproject.github.io/Lists/alt-version/scam-nl.txt',
        ]
    },
    'tracking': {
        'name': 'Ads & Trackers',
        'description': 'Blocks advertisements and online tracking',
        'icon': 'bi-incognito',
        'color': '#0891b2',
        'urls': [
            'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt',
            'https://blocklistproject.github.io/Lists/alt-version/tracking-nl.txt',
            'https://blocklistproject.github.io/Lists/alt-version/ads-nl.txt',
            'https://small.oisd.nl/domainswild',
        ]
    }
}

PROTECTION_MODES = {
    'kids': {
        'name': 'Kids Mode',
        'description': 'Maximum protection - blocks adult content, social media, gambling, and gaming',
        'icon': 'bi-emoji-smile',
        'color': '#22c55e',
        'categories': ['adult', 'social', 'gambling', 'malware', 'tracking', 'gaming']
    },
    'family': {
        'name': 'Family Mode',
        'description': 'Balanced protection - blocks adult content, gambling, and dangerous sites',
        'icon': 'bi-house-heart',
        'color': '#6366f1',
        'categories': ['adult', 'gambling', 'malware', 'tracking']
    },
    'standard': {
        'name': 'Standard Mode',
        'description': 'Basic protection - blocks ads, trackers, and dangerous sites only',
        'icon': 'bi-shield-check',
        'color': '#0ea5e9',
        'categories': ['malware', 'tracking']
    }
}

DEFAULT_GROUPS = {
    'kids': {
        'name': 'Kids Devices',
        'description': 'Maximum protection for children',
        'icon': 'bi-emoji-smile',
        'color': '#22c55e'
    },
    'teens': {
        'name': 'Teen Devices',
        'description': 'Moderate protection for teenagers',
        'icon': 'bi-person',
        'color': '#f59e0b'
    },
    'adults': {
        'name': 'Adult Devices',
        'description': 'Standard protection for adults',
        'icon': 'bi-person-check',
        'color': '#6366f1'
    },
    'unrestricted': {
        'name': 'Unrestricted',
        'description': 'No content filtering (still blocks malware)',
        'icon': 'bi-unlock',
        'color': '#64748b'
    }
}

# ============== HELPER FUNCTIONS ==============

def load_settings():
    """Load settings from file"""
    default_settings = {
        'enabled_categories': ['malware', 'tracking'],
        'protection_mode': 'standard',
        'devices': {},
        'last_health_check': None
    }
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                for key in default_settings:
                    if key not in settings:
                        settings[key] = default_settings[key]
                return settings
    except Exception:
        pass
    return default_settings

def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception:
        return False

def run_pihole_command(command_list, ignore_errors=False):
    """Execute a Pi-hole command"""
    try:
        full_command = ['sudo'] + command_list
        result = subprocess.run(full_command, check=True, timeout=300, capture_output=True, text=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            return True, "Skipped"
        return False, e.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "The command timed out."
    except Exception as e:
        return False, str(e)

def run_sqlite_query(db_path, query):
    """Execute a query on a Pi-hole database using sudo sqlite3"""
    try:
        result = subprocess.run(
            ['sudo', 'sqlite3', '-separator', '|', db_path, query],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def check_url_accessible(url, timeout=10):
    """Check if a URL is accessible"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AuraNet/1.0'})
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except Exception:
        return False

def add_adlist(url, comment="Added by AuraNet"):
    """Add an adlist to Pi-hole"""
    # Check if exists
    success, result = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        f"SELECT id FROM adlist WHERE address = '{url}';"
    )
    
    if success and result.strip():
        # Already exists, enable it
        run_sqlite_query(
            PIHOLE_GRAVITY_DB,
            f"UPDATE adlist SET enabled = 1 WHERE address = '{url}';"
        )
        return True, "Already exists, enabled"
    
    # Insert new
    success, result = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        f"INSERT INTO adlist (address, enabled, comment) VALUES ('{url}', 1, '{comment}');"
    )
    return success, result

def remove_adlist(url):
    """Remove an adlist from Pi-hole"""
    success, result = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        f"DELETE FROM adlist WHERE address = '{url}';"
    )
    return success, result

def update_gravity():
    """Update Pi-hole's gravity (blocklists)"""
    return run_pihole_command(['/usr/local/bin/pihole', '-g'])

def apply_category(category_id, enable=True):
    """Enable or disable a category's blocklists"""
    if category_id not in CATEGORY_LISTS:
        return False, "Invalid category"
    
    category = CATEGORY_LISTS[category_id]
    successful_adds = 0
    
    for url in category['urls']:
        if enable:
            success, msg = add_adlist(url, f"AuraNet: {category['name']}")
            if success:
                successful_adds += 1
        else:
            remove_adlist(url)
    
    if enable and successful_adds == 0:
        return False, "Failed to add any blocklists for this category"
    
    return True, "Success"

def get_pihole_status():
    """Check if Pi-hole protection is currently enabled"""
    try:
        result = subprocess.run(
            ['sudo', '/usr/local/bin/pihole', 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.lower()
        if 'blocking' in output and 'enabled' in output:
            return True
        elif 'blocking' in output and 'disabled' in output:
            return False
        elif 'not' in output or 'disabled' in output:
            return False
        else:
            return True
    except Exception:
        return True

def get_stats():
    """Get Pi-hole statistics from FTL database"""
    stats = {
        'queries_today': '0',
        'blocked_today': '0',
        'percent_blocked': '0',
        'domains_blocked': '0'
    }
    
    try:
        # Get domains blocked count from gravity (unique domains)
        success, result = run_sqlite_query(
            PIHOLE_GRAVITY_DB,
            "SELECT COUNT(DISTINCT domain) FROM gravity;"
        )
        if success and result.strip():
            stats['domains_blocked'] = f"{int(result.strip()):,}"
    except Exception:
        pass
    
    try:
        # Get today's date boundaries (Unix timestamp)
        import time
        now = time.time()
        today_start = now - (now % 86400)  # Start of today UTC
        
        # Get total queries today
        success, result = run_sqlite_query(
            PIHOLE_FTL_DB,
            f"SELECT COUNT(*) FROM query_storage WHERE timestamp >= {int(today_start)};"
        )
        total_queries = int(result.strip()) if success and result.strip() else 0
        stats['queries_today'] = f"{total_queries:,}"
        
        # Get blocked queries today (status 2 = blocked by gravity)
        # Status codes: 2=blocked (gravity), 3=blocked (regex), 4=blocked (exact blacklist), 
        # 5=blocked (external), 10=blocked (special domain), 11=blocked (special domain)
        success, result = run_sqlite_query(
            PIHOLE_FTL_DB,
            f"SELECT COUNT(*) FROM query_storage WHERE timestamp >= {int(today_start)} AND status IN (2,3,4,5,10,11);"
        )
        blocked_queries = int(result.strip()) if success and result.strip() else 0
        stats['blocked_today'] = f"{blocked_queries:,}"
        
        # Calculate percentage
        if total_queries > 0:
            percent = round((blocked_queries / total_queries) * 100, 1)
            stats['percent_blocked'] = percent
        else:
            stats['percent_blocked'] = 0
            
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    return stats

def get_network_devices():
    """Get list of devices on the network from Pi-hole FTL database"""
    devices = []
    
    try:
        # Get devices from network table
        success, result = run_sqlite_query(
            PIHOLE_FTL_DB,
            "SELECT id, hwaddr, interface, firstSeen, lastQuery, numQueries, macVendor FROM network WHERE hwaddr != '' AND hwaddr NOT LIKE 'ip-%' ORDER BY lastQuery DESC;"
        )
        
        if not success or not result.strip():
            return devices
        
        for line in result.strip().split('\n'):
            if not line.strip():
                continue
                
            parts = line.split('|')
            if len(parts) < 7:
                continue
            
            device_id = parts[0]
            hwaddr = parts[1]
            interface = parts[2]
            firstSeen = parts[3]
            lastQuery = parts[4]
            numQueries = parts[5]
            macVendor = parts[6] if len(parts) > 6 else ""
            
            # Get IP address for this device
            ip_success, ip_result = run_sqlite_query(
                PIHOLE_FTL_DB,
                f"SELECT ip FROM network_addresses WHERE network_id = {device_id} ORDER BY lastSeen DESC LIMIT 1;"
            )
            
            ip_address = ip_result.strip() if ip_success and ip_result.strip() else "Unknown"
            
            # Create friendly name
            if macVendor:
                name = macVendor
            else:
                name = f"Device ({hwaddr[-8:]})"
            
            devices.append({
                'mac': hwaddr,
                'ip': ip_address,
                'name': name,
                'vendor': macVendor,
                'queries': int(numQueries) if numQueries else 0,
                'last_seen': lastQuery
            })
    
    except Exception as e:
        print(f"Error getting devices: {e}")
    
    return devices

def set_device_group(mac_address, group_name, device_name=None):
    """Assign a device to a group"""
    settings = load_settings()
    
    if 'devices' not in settings:
        settings['devices'] = {}
    
    settings['devices'][mac_address] = {
        'group': group_name,
        'name': device_name
    }
    
    save_settings(settings)
    return True

# ============== HEALTH CHECK FUNCTIONS ==============

def run_health_check():
    """Run comprehensive health check"""
    health = {
        'timestamp': datetime.now().isoformat(),
        'overall_status': 'healthy',
        'checks': {}
    }
    
    issues = []
    
    # Check 1: Pi-hole service running
    try:
        result = subprocess.run(['sudo', 'systemctl', 'is-active', 'pihole-FTL'], 
                                capture_output=True, text=True, timeout=10)
        pihole_running = result.stdout.strip() == 'active'
    except Exception:
        pihole_running = False
    
    health['checks']['pihole_service'] = {
        'name': 'Pi-hole Service',
        'status': 'ok' if pihole_running else 'error',
        'message': 'Running normally' if pihole_running else 'Pi-hole service is not running'
    }
    if not pihole_running:
        issues.append('pihole_service')
    
    # Check 2: DNS resolution working
    try:
        result = subprocess.run(['nslookup', 'google.com', '127.0.0.1'],
                                capture_output=True, text=True, timeout=10)
        dns_working = result.returncode == 0
    except Exception:
        dns_working = False
    
    health['checks']['dns_resolution'] = {
        'name': 'DNS Resolution',
        'status': 'ok' if dns_working else 'error',
        'message': 'Working correctly' if dns_working else 'DNS queries are failing'
    }
    if not dns_working:
        issues.append('dns_resolution')
    
    # Check 3: Gravity database exists and has entries
    try:
        success, result = run_sqlite_query(PIHOLE_GRAVITY_DB, "SELECT COUNT(*) FROM gravity;")
        gravity_count = int(result.strip()) if success and result.strip() else 0
        gravity_ok = gravity_count > 1000
    except Exception:
        gravity_ok = False
        gravity_count = 0
    
    health['checks']['blocklist_database'] = {
        'name': 'Blocklist Database',
        'status': 'ok' if gravity_ok else 'warning',
        'message': f'{gravity_count:,} domains in blocklist' if gravity_ok else 'Blocklist may be empty or corrupted'
    }
    if not gravity_ok:
        issues.append('blocklist_database')
    
    # Check 4: Internet connectivity
    try:
        urllib.request.urlopen('https://google.com', timeout=10)
        internet_ok = True
    except Exception:
        internet_ok = False
    
    health['checks']['internet_connection'] = {
        'name': 'Internet Connection',
        'status': 'ok' if internet_ok else 'error',
        'message': 'Connected' if internet_ok else 'No internet connection detected'
    }
    if not internet_ok:
        issues.append('internet_connection')
    
    # Check 5: At least one blocklist source is accessible
    blocklist_accessible = False
    for cat_id, cat in CATEGORY_LISTS.items():
        if check_url_accessible(cat['urls'][0], timeout=5):
            blocklist_accessible = True
            break
    
    health['checks']['blocklist_sources'] = {
        'name': 'Blocklist Sources',
        'status': 'ok' if blocklist_accessible else 'warning',
        'message': 'Sources accessible' if blocklist_accessible else 'Some blocklist sources may be unavailable'
    }
    if not blocklist_accessible:
        issues.append('blocklist_sources')
    
    # Check 6: Disk space
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            usage_percent = int(parts[4].replace('%', ''))
            disk_ok = usage_percent < 90
        else:
            disk_ok = True
            usage_percent = 0
    except Exception:
        disk_ok = True
        usage_percent = 0
    
    health['checks']['disk_space'] = {
        'name': 'Disk Space',
        'status': 'ok' if disk_ok else 'warning',
        'message': f'{usage_percent}% used' if disk_ok else f'Disk almost full ({usage_percent}% used)'
    }
    if not disk_ok:
        issues.append('disk_space')
    
    # Check 7: Memory usage
    try:
        result = subprocess.run(['free', '-m'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            total = int(parts[1])
            available = int(parts[6]) if len(parts) > 6 else int(parts[3])
            memory_percent = round((1 - available / total) * 100)
            memory_ok = memory_percent < 90
        else:
            memory_ok = True
            memory_percent = 0
    except Exception:
        memory_ok = True
        memory_percent = 0
    
    health['checks']['memory'] = {
        'name': 'Memory Usage',
        'status': 'ok' if memory_ok else 'warning',
        'message': f'{memory_percent}% used' if memory_ok else f'Memory running low ({memory_percent}% used)'
    }
    if not memory_ok:
        issues.append('memory')
    
    # Set overall status
    error_checks = [c for c in health['checks'].values() if c['status'] == 'error']
    warning_checks = [c for c in health['checks'].values() if c['status'] == 'warning']
    
    if error_checks:
        health['overall_status'] = 'error'
    elif warning_checks:
        health['overall_status'] = 'warning'
    else:
        health['overall_status'] = 'healthy'
    
    health['issues'] = issues
    
    # Save last health check
    settings = load_settings()
    settings['last_health_check'] = health
    save_settings(settings)
    
    return health

def get_troubleshooting_steps(issue):
    """Get troubleshooting steps for common issues"""
    steps = {
        'pihole_service': [
            'Try restarting your AuraNet device by unplugging it and plugging it back in',
            'Wait 2-3 minutes for the device to fully start up',
            'If the problem persists, contact support'
        ],
        'dns_resolution': [
            'Check that your router is connected to the internet',
            'Try restarting your AuraNet device',
            'Make sure no other device is using the same IP address'
        ],
        'blocklist_database': [
            'Go to Home and click on any Protection Mode to rebuild blocklists',
            'Wait 2-3 minutes for the update to complete',
            'If the problem persists, restart your AuraNet device'
        ],
        'internet_connection': [
            'Check that your router has internet access',
            'Make sure the ethernet cable is securely connected',
            'Try restarting your router',
            'Contact your internet provider if the issue persists'
        ],
        'blocklist_sources': [
            'This is usually temporary - blocklist servers may be updating',
            'Your current protection is still working',
            'Check again in a few hours'
        ],
        'disk_space': [
            'Your device storage is getting full',
            'This may affect performance over time',
            'Contact support for assistance'
        ],
        'memory': [
            'Try restarting your AuraNet device',
            'If this happens frequently, contact support'
        ]
    }
    return steps.get(issue, ['Contact support for assistance'])

# ============== ROUTES ==============

@app.route('/')
def index():
    settings = load_settings()
    is_protected = get_pihole_status()
    stats = get_stats()
    
    return render_template('index.html',
        title='AuraNet - Home Network Protection',
        is_protected=is_protected,
        settings=settings,
        categories=CATEGORY_LISTS,
        modes=PROTECTION_MODES,
        stats=stats
    )

@app.route('/devices')
def devices():
    settings = load_settings()
    is_protected = get_pihole_status()
    network_devices = get_network_devices()
    
    for device in network_devices:
        device_settings = settings.get('devices', {}).get(device['mac'], {})
        device['custom_name'] = device_settings.get('name', '')
        device['icon'] = device_settings.get('icon', 'laptop')
    
    return render_template('devices.html',
        title='AuraNet - Device Management',
        is_protected=is_protected,
        devices=network_devices,
        settings=settings
    )

@app.route('/health')
def health():
    settings = load_settings()
    is_protected = get_pihole_status()
    health_data = run_health_check()
    
    troubleshooting = {}
    for issue in health_data.get('issues', []):
        troubleshooting[issue] = get_troubleshooting_steps(issue)
    
    return render_template('health.html',
        title='AuraNet - System Health',
        is_protected=is_protected,
        health=health_data,
        troubleshooting=troubleshooting,
        settings=settings
    )

@app.route('/help')
def help_page():
    settings = load_settings()
    is_protected = get_pihole_status()
    
    return render_template('help.html',
        title='AuraNet - Help & FAQ',
        is_protected=is_protected,
        settings=settings
    )

@app.route('/device/<mac_address>/rename', methods=['POST'])
def rename_device(mac_address):
    custom_name = request.form.get('custom_name', '').strip()
    icon = request.form.get('icon', 'laptop')
    
    if not custom_name:
        flash('Please enter a name for the device.', 'warning')
        return redirect(url_for('devices'))
    
    settings = load_settings()
    
    if 'devices' not in settings:
        settings['devices'] = {}
    
    settings['devices'][mac_address] = {
        'name': custom_name,
        'icon': icon
    }
    
    save_settings(settings)
    
    flash(f'Device renamed to "{custom_name}".', 'success')
    return redirect(url_for('devices'))

@app.route('/domain', methods=['POST'])
def manage_domain():
    domain_raw = request.form.get('domain')
    action = request.form.get('action')

    if not domain_raw:
        flash('Please enter a website address.', 'warning')
        return redirect(url_for('index'))

    domain = domain_raw.replace("http://", "").replace("https://", "")
    domain = domain.split('/')[0]
    if domain.lower().startswith('www.'):
        domain = domain[4:]

    if action == 'allow':
        run_pihole_command(['/usr/local/bin/pihole', 'deny', 'remove', domain], ignore_errors=True)
        cmd = ['/usr/local/bin/pihole', 'allow', domain]
        action_text = "allowed"
    elif action == 'deny':
        run_pihole_command(['/usr/local/bin/pihole', 'allow', 'remove', domain], ignore_errors=True)
        cmd = ['/usr/local/bin/pihole', 'deny', domain]
        action_text = "blocked"
    else:
        return redirect(url_for('index'))

    success, message = run_pihole_command(cmd)

    if success:
        flash(f'"{domain}" has been {action_text}. It may take a few minutes to take effect.', 'success')
    else:
        flash(f'There was a problem: {message}', 'danger')

    return redirect(url_for('index'))

@app.route('/protection/pause', methods=['POST'])
def pause_protection():
    duration = request.form.get('duration', '5m')
    
    valid_durations = {
        '5m': '5 minutes',
        '15m': '15 minutes',
        '30m': '30 minutes',
        '1h': '1 hour',
        '2h': '2 hours'
    }
    
    if duration not in valid_durations:
        flash('Invalid duration selected.', 'danger')
        return redirect(url_for('index'))
    
    success, message = run_pihole_command(['/usr/local/bin/pihole', 'disable', duration])
    
    if success:
        flash(f'Protection paused for {valid_durations[duration]}. Your network is temporarily unprotected.', 'warning')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(url_for('index'))

@app.route('/protection/enable')
def enable_protection():
    success, message = run_pihole_command(['/usr/local/bin/pihole', 'enable'])
    if success:
        flash('Protection is back on! Your network is now secure.', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    return redirect(url_for('index'))

@app.route('/mode/<mode_name>')
def set_mode(mode_name):
    if mode_name not in PROTECTION_MODES:
        flash('Invalid protection mode.', 'danger')
        return redirect(url_for('index'))
    
    mode = PROTECTION_MODES[mode_name]
    settings = load_settings()
    
    # First, remove all category lists
    for cat_id in CATEGORY_LISTS:
        apply_category(cat_id, enable=False)
    
    # Then add the ones for this mode
    failed_categories = []
    for cat_id in mode['categories']:
        success, result = apply_category(cat_id, enable=True)
        if not success:
            failed_categories.append(cat_id)
    
    # Update gravity
    success, message = update_gravity()
    
    if success:
        settings['protection_mode'] = mode_name
        settings['enabled_categories'] = mode['categories'].copy()
        save_settings(settings)
        
        if failed_categories:
            flash(f'{mode["name"]} is now active, but some blocklists could not be added. Protection is still working.', 'warning')
        else:
            flash(f'{mode["name"]} is now active! Your blocklists have been updated.', 'success')
    else:
        flash(f'There was an issue updating blocklists. Please try again or check System Health.', 'danger')
    
    return redirect(url_for('index'))

@app.route('/category/<category_name>/toggle')
def toggle_category(category_name):
    if category_name not in CATEGORY_LISTS:
        flash('Invalid category.', 'danger')
        return redirect(url_for('index'))
    
    settings = load_settings()
    category = CATEGORY_LISTS[category_name]
    
    if category_name in settings.get('enabled_categories', []):
        apply_category(category_name, enable=False)
        settings['enabled_categories'].remove(category_name)
        action = "disabled"
    else:
        success, result = apply_category(category_name, enable=True)
        if 'enabled_categories' not in settings:
            settings['enabled_categories'] = []
        settings['enabled_categories'].append(category_name)
        action = "enabled"
    
    settings['protection_mode'] = 'custom'
    save_settings(settings)
    
    success, message = update_gravity()
    
    if success:
        flash(f'{category["name"]} blocking has been {action}.', 'success')
    else:
        flash(f'{category["name"]} {action}, but there was an issue updating. Check System Health for details.', 'warning')
    
    return redirect(url_for('index'))

@app.route('/repair/<issue>')
def repair_issue(issue):
    """Attempt to automatically repair common issues"""
    
    if issue == 'pihole_service':
        success, msg = run_pihole_command(['systemctl', 'restart', 'pihole-FTL'], ignore_errors=True)
        if success:
            flash('Pi-hole service has been restarted.', 'success')
        else:
            flash('Could not restart the service. Try restarting the device.', 'warning')
    
    elif issue == 'blocklist_database':
        success, msg = update_gravity()
        if success:
            flash('Blocklist database has been rebuilt.', 'success')
        else:
            flash('Could not rebuild database. Please try again later.', 'warning')
    
    elif issue == 'dns_resolution':
        run_pihole_command(['pihole', 'restartdns'], ignore_errors=True)
        flash('DNS service has been restarted.', 'success')
    
    else:
        flash('Automatic repair is not available for this issue. Please follow the manual steps.', 'info')
    
    return redirect(url_for('health'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
