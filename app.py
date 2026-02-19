from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
import subprocess
import json
import os
import sqlite3
import secrets
import urllib.request
import urllib.error
import threading
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, available_timezones

# ============== APP SETUP ==============

SETTINGS_FILE = os.path.expanduser('~/auranet_dashboard/settings.json')
GRAVITY_STATUS_FILE = os.path.expanduser('~/auranet_dashboard/gravity_status.json')
UPDATE_STATUS_FILE = os.path.expanduser('~/auranet_dashboard/update_status.json')
VERSION_FILE = os.path.expanduser('~/auranet_dashboard/version.txt')
DASHBOARD_DIR = os.path.expanduser('~/auranet_dashboard')
GITHUB_VERSION_URL = 'https://raw.githubusercontent.com/AuraNet-AU/auranet-dashboard/main/version.json'
PIHOLE_GRAVITY_DB = '/etc/pihole/gravity.db'
PIHOLE_FTL_DB = '/etc/pihole/pihole-FTL.db'

# Australia/Brisbane (UTC+10, no DST) — kept for reference; stats now use settings timezone
AEST_OFFSET = timezone(timedelta(hours=10))

def _get_or_create_secret_key():
    """Load secret key from settings, generating one if it doesn't exist."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
            if 'secret_key' in data:
                return data['secret_key']
        # Generate and persist a new key
        key = secrets.token_hex(32)
        data = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
        data['secret_key'] = key
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return key
    except Exception:
        # Fallback: non-persistent but at least random per process
        return secrets.token_hex(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = _get_or_create_secret_key()

# ============== SETUP GUARD ==============

SETUP_EXEMPT = {
    'setup', 'setup_check_internet',
    'settings', 'settings_timezone', 'settings_reset_setup',
    'settings_check_update', 'settings_update', 'settings_update_status_route',
    'gravity_status_route', 'gravity_dismiss', 'static',
}

@app.before_request
def require_setup():
    if request.endpoint in SETUP_EXEMPT:
        return
    s = load_settings()
    if not s.get('setup_completed', False):
        return redirect(url_for('setup'))

# ============== BLOCKLISTS ==============

CATEGORY_LISTS = {
    'vpn': {
        'name': 'VPN & Proxy Services',
        'description': 'Blocks VPN apps and services (enforces social media ban)',
        'icon': 'bi-shield-lock',
        'color': '#ef4444',
        'urls': [
            'https://raw.githubusercontent.com/AuraNet-AU/blocklists/main/vpn-blocklist.txt',
            'file:///home/auranet/vpn_blocklist.txt',
        ]
    },
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
            'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/social-onlydomains.txt',
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
            'https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt',
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
        'description': 'Maximum protection - blocks VPNs, social media, adult content, and gaming',
        'icon': 'bi-emoji-smile',
        'color': '#22c55e',
        'categories': ['vpn', 'adult', 'social', 'gambling', 'malware', 'tracking', 'gaming']
    },
    'family': {
        'name': 'Family Mode',
        'description': 'Balanced protection - blocks VPNs, adult content, gambling, and dangerous sites',
        'icon': 'bi-house-heart',
        'color': '#6366f1',
        'categories': ['vpn', 'adult', 'gambling', 'malware', 'tracking']
    },
    'standard': {
        'name': 'Standard Mode',
        'description': 'Basic protection - blocks ads, trackers, and dangerous sites only',
        'icon': 'bi-shield-check',
        'color': '#0ea5e9',
        'categories': ['malware', 'tracking']
    }
}

# ============== HELPER FUNCTIONS ==============

def load_settings():
    """Load settings from file."""
    default_settings = {
        'enabled_categories': ['malware', 'tracking'],
        'protection_mode': 'standard',
        'devices': {},
        'last_health_check': None,
        'bedtime_enabled': False,
        'bedtime_start': '21:00',
        'bedtime_end': '07:00',
        'setup_completed': False,
        'setup_product': None,
        'timezone': 'Australia/Brisbane',
    }
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            for key, val in default_settings.items():
                if key not in settings:
                    settings[key] = val
            return settings
    except Exception:
        pass
    return default_settings

def save_settings(settings):
    """Save settings to file."""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception:
        return False

def run_pihole_command(command_list, ignore_errors=False):
    """Execute a Pi-hole command via sudo."""
    try:
        result = subprocess.run(
            ['sudo'] + command_list,
            check=True, timeout=300, capture_output=True, text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            return True, "Skipped"
        return False, e.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "The command timed out."
    except Exception as e:
        return False, str(e)

def run_sqlite_query(db_path, query, params=()):
    """
    Execute a parameterised query on a Pi-hole SQLite database.
    Uses Python's sqlite3 module directly — no SQL injection risk.
    Returns (success: bool, result: list of rows | error string).
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return True, rows
    except Exception as e:
        return False, str(e)

def check_url_accessible(url, timeout=10):
    """Check if a URL is accessible."""
    if url.startswith('file://'):
        path = url[7:]
        return os.path.exists(path)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AuraNet/1.0'})
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except Exception:
        return False

def add_adlist(url, comment="Added by AuraNet"):
    """Add an adlist to Pi-hole's gravity database."""
    success, rows = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        "SELECT id FROM adlist WHERE address = ?",
        (url,)
    )
    if success and rows:
        run_sqlite_query(
            PIHOLE_GRAVITY_DB,
            "UPDATE adlist SET enabled = 1 WHERE address = ?",
            (url,)
        )
        return True, "Already exists, enabled"
    success, result = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        "INSERT INTO adlist (address, enabled, comment) VALUES (?, 1, ?)",
        (url, comment)
    )
    return success, str(result)

def remove_adlist(url):
    """Remove an adlist from Pi-hole's gravity database."""
    success, result = run_sqlite_query(
        PIHOLE_GRAVITY_DB,
        "DELETE FROM adlist WHERE address = ?",
        (url,)
    )
    return success, str(result)

def update_gravity_background():
    """Run gravity update in background and track status."""
    def run():
        try:
            with open(GRAVITY_STATUS_FILE, 'w') as f:
                json.dump({'status': 'running', 'started': datetime.now().isoformat()}, f)
            success, message = run_pihole_command(['/usr/local/bin/pihole', '-g'])
            with open(GRAVITY_STATUS_FILE, 'w') as f:
                json.dump({
                    'status': 'done' if success else 'error',
                    'finished': datetime.now().isoformat(),
                    'message': message
                }, f)
        except Exception as e:
            try:
                with open(GRAVITY_STATUS_FILE, 'w') as f:
                    json.dump({
                        'status': 'error',
                        'finished': datetime.now().isoformat(),
                        'message': str(e)
                    }, f)
            except Exception:
                pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

def get_gravity_status():
    """Get current gravity update status."""
    try:
        if os.path.exists(GRAVITY_STATUS_FILE):
            with open(GRAVITY_STATUS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def update_dashboard_background():
    """Run git pull + service restart in background and track status."""
    def run():
        try:
            with open(UPDATE_STATUS_FILE, 'w') as f:
                json.dump({'status': 'running', 'started': datetime.now().isoformat()}, f)
            subprocess.run(
                ['git', '-C', DASHBOARD_DIR, 'pull'],
                check=True, timeout=60, capture_output=True
            )
            with open(UPDATE_STATUS_FILE, 'w') as f:
                json.dump({'status': 'done', 'finished': datetime.now().isoformat()}, f)
            subprocess.run(['sudo', 'systemctl', 'restart', 'auranet'], check=True, timeout=30)
        except Exception as e:
            try:
                with open(UPDATE_STATUS_FILE, 'w') as f:
                    json.dump({'status': 'error', 'message': str(e), 'finished': datetime.now().isoformat()}, f)
            except Exception:
                pass
    threading.Thread(target=run, daemon=True).start()

def get_update_status():
    """Get current dashboard update status."""
    try:
        if os.path.exists(UPDATE_STATUS_FILE):
            with open(UPDATE_STATUS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def apply_category(category_id, enable=True):
    """Enable or disable a category's blocklists."""
    if category_id not in CATEGORY_LISTS:
        return False, "Invalid category"
    category = CATEGORY_LISTS[category_id]
    successful = 0
    for url in category['urls']:
        if enable:
            success, _ = add_adlist(url, f"AuraNet: {category['name']}")
            if success:
                successful += 1
        else:
            remove_adlist(url)
    if enable and successful == 0:
        return False, "Failed to add any blocklists for this category"
    return True, "Success"

def get_pihole_status():
    """Check if Pi-hole blocking is currently enabled."""
    try:
        result = subprocess.run(
            ['sudo', '/usr/local/bin/pihole', 'status'],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.lower()
        if 'blocking' in output and 'enabled' in output:
            return True
        elif 'blocking' in output and 'disabled' in output:
            return False
        return 'not' not in output and 'disabled' not in output
    except Exception:
        return True

def get_stats():
    """Get Pi-hole statistics from FTL database."""
    stats = {
        'queries_today': '0',
        'blocked_today': '0',
        'percent_blocked': 0,
        'domains_blocked': '0'
    }

    # Total domains in blocklist
    try:
        success, rows = run_sqlite_query(
            PIHOLE_GRAVITY_DB,
            "SELECT COUNT(DISTINCT domain) FROM gravity"
        )
        if success and rows:
            stats['domains_blocked'] = f"{rows[0][0]:,}"
    except Exception:
        pass

    # Queries and blocks since midnight in configured timezone
    try:
        tz_name = load_settings().get('timezone', 'Australia/Brisbane')
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            tz = ZoneInfo('Australia/Brisbane')
        now_local = datetime.now(tz)
        today_start = int(now_local.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

        success, rows = run_sqlite_query(
            PIHOLE_FTL_DB,
            "SELECT COUNT(*) FROM query_storage WHERE timestamp >= ?",
            (today_start,)
        )
        total = rows[0][0] if success and rows else 0
        stats['queries_today'] = f"{total:,}"

        success, rows = run_sqlite_query(
            PIHOLE_FTL_DB,
            "SELECT COUNT(*) FROM query_storage WHERE timestamp >= ? AND status IN (2,3,4,5,10,11)",
            (today_start,)
        )
        blocked = rows[0][0] if success and rows else 0
        stats['blocked_today'] = f"{blocked:,}"
        stats['percent_blocked'] = round((blocked / total) * 100, 1) if total > 0 else 0
    except Exception as e:
        print(f"Error getting stats: {e}")

    return stats

def get_last_blocked_domain():
    """Get the most recently blocked domain."""
    try:
        success, rows = run_sqlite_query(
            PIHOLE_FTL_DB,
            "SELECT domain FROM query_storage WHERE status IN (2,3,4,5,10,11) ORDER BY timestamp DESC LIMIT 1"
        )
        if success and rows:
            return rows[0][0]
    except Exception:
        pass
    return None

def get_network_devices():
    """Get list of devices on the network from Pi-hole FTL database."""
    devices = []
    try:
        success, rows = run_sqlite_query(
            PIHOLE_FTL_DB,
            "SELECT id, hwaddr, interface, firstSeen, lastQuery, numQueries, macVendor "
            "FROM network WHERE hwaddr != '' AND hwaddr NOT LIKE 'ip-%' "
            "ORDER BY lastQuery DESC"
        )
        if not success or not rows:
            return devices

        for row in rows:
            device_id = row[0]
            hwaddr    = row[1]
            numQueries = row[5]
            macVendor  = row[6] or ""

            ip_success, ip_rows = run_sqlite_query(
                PIHOLE_FTL_DB,
                "SELECT ip FROM network_addresses WHERE network_id = ? ORDER BY lastSeen DESC LIMIT 1",
                (device_id,)
            )
            ip_address = ip_rows[0][0] if ip_success and ip_rows else "Unknown"
            name = macVendor if macVendor else f"Device ({hwaddr[-8:]})"

            devices.append({
                'mac': hwaddr,
                'ip': ip_address,
                'name': name,
                'vendor': macVendor,
                'queries': int(numQueries) if numQueries else 0,
                'last_seen': row[4]
            })
    except Exception as e:
        print(f"Error getting devices: {e}")
    return devices

# ============== HEALTH CHECK ==============

# Cache: (timestamp, result) — refresh every 5 minutes
_health_cache = (None, None)
HEALTH_CACHE_TTL = 300  # seconds

def run_health_check(force=False):
    """Run health check, returning cached result if fresh enough."""
    global _health_cache
    cached_at, cached_result = _health_cache

    if not force and cached_at and (datetime.now().timestamp() - cached_at) < HEALTH_CACHE_TTL:
        return cached_result

    health = {
        'timestamp': datetime.now().isoformat(),
        'overall_status': 'healthy',
        'checks': {}
    }

    # Pi-hole service
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'is-active', 'pihole-FTL'],
            capture_output=True, text=True, timeout=10
        )
        pihole_running = result.stdout.strip() == 'active'
    except Exception:
        pihole_running = False

    health['checks']['pihole_service'] = {
        'name': 'Protection Service',
        'status': 'ok' if pihole_running else 'error',
        'message': 'Running normally' if pihole_running else 'Protection service is not running'
    }

    # DNS resolution
    try:
        result = subprocess.run(
            ['nslookup', 'google.com', '127.0.0.1'],
            capture_output=True, text=True, timeout=10
        )
        dns_working = result.returncode == 0
    except Exception:
        dns_working = False

    health['checks']['dns_resolution'] = {
        'name': 'Internet Lookup',
        'status': 'ok' if dns_working else 'error',
        'message': 'Working correctly' if dns_working else 'DNS queries are failing'
    }

    # Blocklist database
    try:
        success, rows = run_sqlite_query(PIHOLE_GRAVITY_DB, "SELECT COUNT(*) FROM gravity")
        gravity_count = rows[0][0] if success and rows else 0
        gravity_ok = gravity_count > 1000
    except Exception:
        gravity_ok = False
        gravity_count = 0

    health['checks']['blocklist_database'] = {
        'name': 'Blocklist Database',
        'status': 'ok' if gravity_ok else 'warning',
        'message': f'{gravity_count:,} domains in blocklist' if gravity_ok else 'Blocklist may be empty or corrupted'
    }

    # Internet connection
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

    # Blocklist sources (skip local file:// URLs)
    blocklist_accessible = False
    for cat in CATEGORY_LISTS.values():
        http_urls = [u for u in cat['urls'] if not u.startswith('file://')]
        if http_urls and check_url_accessible(http_urls[0], timeout=5):
            blocklist_accessible = True
            break

    health['checks']['blocklist_sources'] = {
        'name': 'Blocklist Sources',
        'status': 'ok' if blocklist_accessible else 'warning',
        'message': 'Sources accessible' if blocklist_accessible else 'Some blocklist sources may be unavailable'
    }

    # Disk space
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        usage_percent = int(lines[1].split()[4].replace('%', '')) if len(lines) > 1 else 0
        disk_ok = usage_percent < 90
    except Exception:
        disk_ok = True
        usage_percent = 0

    health['checks']['disk_space'] = {
        'name': 'Disk Space',
        'status': 'ok' if disk_ok else 'warning',
        'message': f'{usage_percent}% used' if disk_ok else f'Disk almost full ({usage_percent}% used)'
    }

    # Memory
    try:
        result = subprocess.run(['free', '-m'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        parts = lines[1].split() if len(lines) > 1 else []
        if parts:
            total = int(parts[1])
            available = int(parts[6]) if len(parts) > 6 else int(parts[3])
            memory_percent = round((1 - available / total) * 100)
        else:
            memory_percent = 0
        memory_ok = memory_percent < 90
    except Exception:
        memory_ok = True
        memory_percent = 0

    health['checks']['memory'] = {
        'name': 'Memory Usage',
        'status': 'ok' if memory_ok else 'warning',
        'message': f'{memory_percent}% used' if memory_ok else f'Memory running low ({memory_percent}% used)'
    }

    # Overall status
    statuses = [c['status'] for c in health['checks'].values()]
    if 'error' in statuses:
        health['overall_status'] = 'error'
    elif 'warning' in statuses:
        health['overall_status'] = 'warning'
    else:
        health['overall_status'] = 'healthy'

    health['issues'] = [k for k, v in health['checks'].items() if v['status'] != 'ok']

    # Persist to settings and update cache
    settings = load_settings()
    settings['last_health_check'] = health
    save_settings(settings)

    _health_cache = (datetime.now().timestamp(), health)
    return health

def get_troubleshooting_steps(issue):
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
            'This is usually temporary — blocklist servers may be updating',
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
    return render_template('index.html',
        title='AuraNet - Home Network Protection',
        is_protected=get_pihole_status(),
        settings=settings,
        categories=CATEGORY_LISTS,
        modes=PROTECTION_MODES,
        stats=get_stats(),
        last_blocked=get_last_blocked_domain(),
        gravity_status=get_gravity_status()
    )

@app.route('/devices')
def devices():
    settings = load_settings()
    network_devices = get_network_devices()
    for device in network_devices:
        device_settings = settings.get('devices', {}).get(device['mac'], {})
        device['custom_name'] = device_settings.get('name', '')
        device['icon'] = device_settings.get('icon', 'laptop')
    return render_template('devices.html',
        title='AuraNet - Device Management',
        is_protected=get_pihole_status(),
        devices=network_devices,
        settings=settings
    )

@app.route('/health')
def health():
    settings = load_settings()
    health_data = run_health_check()
    troubleshooting = {issue: get_troubleshooting_steps(issue) for issue in health_data.get('issues', [])}
    return render_template('health.html',
        title='AuraNet - System Health',
        is_protected=get_pihole_status(),
        health=health_data,
        troubleshooting=troubleshooting,
        settings=settings
    )

@app.route('/help')
def help_page():
    settings = load_settings()
    return render_template('help.html',
        title='AuraNet - Help & FAQ',
        is_protected=get_pihole_status(),
        settings=settings
    )

@app.route('/gravity/status')
def gravity_status_route():
    return jsonify(get_gravity_status() or {'status': 'idle'})

@app.route('/gravity/dismiss', methods=['POST'])
def gravity_dismiss():
    try:
        if os.path.exists(GRAVITY_STATUS_FILE):
            os.remove(GRAVITY_STATUS_FILE)
    except Exception:
        pass
    return jsonify({'ok': True})

@app.route('/device/<mac_address>/rename', methods=['POST'])
def rename_device(mac_address):
    custom_name = request.form.get('custom_name', '').strip()
    icon = request.form.get('icon', 'laptop')
    if not custom_name:
        flash('Please enter a name for the device.', 'warning')
        return redirect(url_for('devices'))
    settings = load_settings()
    settings.setdefault('devices', {})[mac_address] = {'name': custom_name, 'icon': icon}
    save_settings(settings)
    flash(f'Device renamed to "{custom_name}".', 'success')
    return redirect(url_for('devices'))

@app.route('/domain', methods=['POST'])
def manage_domain():
    domain_raw = request.form.get('domain', '').strip()
    action = request.form.get('action')
    if not domain_raw:
        flash('Please enter a website address.', 'warning')
        return redirect(url_for('index'))
    domain = domain_raw.replace("http://", "").replace("https://", "").split('/')[0]
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
        '5m': '5 minutes', '15m': '15 minutes', '30m': '30 minutes',
        '1h': '1 hour', '2h': '2 hours'
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

# --- Mode and category now use POST to prevent CSRF/accidental triggers ---

@app.route('/mode/<mode_name>', methods=['POST'])
def set_mode(mode_name):
    if mode_name not in PROTECTION_MODES:
        flash('Invalid protection mode.', 'danger')
        return redirect(url_for('index'))
    mode = PROTECTION_MODES[mode_name]
    settings = load_settings()
    for cat_id in CATEGORY_LISTS:
        apply_category(cat_id, enable=False)
    for cat_id in mode['categories']:
        apply_category(cat_id, enable=True)
    settings['protection_mode'] = mode_name
    settings['enabled_categories'] = mode['categories'].copy()
    save_settings(settings)
    update_gravity_background()
    flash(f'{mode["name"]} is now active! Blocklists are updating in the background — this takes 2-3 minutes. Your protection remains active throughout.', 'success')
    return redirect(url_for('index'))

@app.route('/category/<category_name>/toggle', methods=['POST'])
def toggle_category(category_name):
    if category_name not in CATEGORY_LISTS:
        flash('Invalid category.', 'danger')
        return redirect(url_for('index'))
    settings = load_settings()
    category = CATEGORY_LISTS[category_name]
    enabled = settings.get('enabled_categories', [])
    if category_name in enabled:
        apply_category(category_name, enable=False)
        enabled.remove(category_name)
        action = "disabled"
    else:
        apply_category(category_name, enable=True)
        enabled.append(category_name)
        action = "enabled"
    settings['enabled_categories'] = enabled
    settings['protection_mode'] = 'custom'
    save_settings(settings)
    update_gravity_background()
    flash(f'{category["name"]} blocking has been {action}. Blocklists are updating in the background — this takes 2-3 minutes.', 'success')
    return redirect(url_for('index'))

@app.route('/repair/<issue>')
def repair_issue(issue):
    if issue == 'pihole_service':
        success, _ = run_pihole_command(['systemctl', 'restart', 'pihole-FTL'], ignore_errors=True)
        flash('Protection service has been restarted.' if success else 'Could not restart the service. Try restarting the device.', 'success' if success else 'warning')
    elif issue == 'blocklist_database':
        update_gravity_background()
        flash('Blocklist rebuild started. This will take 2-3 minutes.', 'success')
    elif issue == 'dns_resolution':
        run_pihole_command(['pihole', 'restartdns'], ignore_errors=True)
        flash('DNS service has been restarted.', 'success')
    else:
        flash('Automatic repair is not available for this issue. Please follow the manual steps.', 'info')
    return redirect(url_for('health'))

# ============== SETUP WIZARD ROUTES ==============

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    settings = load_settings()
    step = int(request.args.get('step', 1))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'select_product':
            product = request.form.get('product')
            if product in ('smart_wifi_kit', 'network_supercharger'):
                settings['setup_product'] = product
                save_settings(settings)
            return redirect(url_for('setup', step=2))

        elif action == 'next_step':
            next_s = int(request.form.get('next', step + 1))
            return redirect(url_for('setup', step=next_s))

        elif action == 'rename_device':
            mac = request.form.get('mac', '').strip()
            name = request.form.get('name', '').strip()
            icon = request.form.get('icon', 'laptop')
            if mac and name:
                settings.setdefault('devices', {})[mac] = {'name': name, 'icon': icon}
                save_settings(settings)
            return redirect(url_for('setup', step=4))

        elif action == 'set_mode':
            mode_name = request.form.get('mode')
            if mode_name in PROTECTION_MODES:
                mode = PROTECTION_MODES[mode_name]
                for cat_id in CATEGORY_LISTS:
                    apply_category(cat_id, enable=False)
                for cat_id in mode['categories']:
                    apply_category(cat_id, enable=True)
                settings['protection_mode'] = mode_name
                settings['enabled_categories'] = mode['categories'].copy()
                save_settings(settings)
                update_gravity_background()
            return redirect(url_for('setup', step=6))

        elif action == 'complete':
            settings['setup_completed'] = True
            save_settings(settings)
            return redirect(url_for('index'))

    # GET — render current step
    devices = []
    if step == 4:
        devices = get_network_devices()
        for device in devices:
            ds = settings.get('devices', {}).get(device['mac'], {})
            device['custom_name'] = ds.get('name', '')
            device['icon'] = ds.get('icon', 'laptop')

    return render_template('setup.html',
        title='AuraNet Setup',
        step=step,
        settings=settings,
        modes=PROTECTION_MODES,
        devices=devices,
    )

@app.route('/setup/check-internet')
def setup_check_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=8)
        internet_ok = True
    except Exception:
        internet_ok = False
    try:
        result = subprocess.run(
            ['nslookup', 'google.com', '127.0.0.1'],
            capture_output=True, text=True, timeout=8
        )
        dns_ok = result.returncode == 0
    except Exception:
        dns_ok = False
    return jsonify({'internet': internet_ok, 'dns': dns_ok, 'ok': internet_ok and dns_ok})

# ============== SETTINGS ROUTES ==============

@app.route('/settings')
def settings():
    s = load_settings()
    try:
        with open(VERSION_FILE) as f:
            current_version = f.read().strip()
    except Exception:
        current_version = 'Unknown'
    au_timezones = sorted(tz for tz in available_timezones() if tz.startswith('Australia/'))
    other_timezones = sorted(tz for tz in available_timezones() if not tz.startswith('Australia/'))
    return render_template('settings.html',
        title='AuraNet - Settings',
        active_page='settings',
        is_protected=get_pihole_status(),
        settings=s,
        current_version=current_version,
        au_timezones=au_timezones,
        other_timezones=other_timezones,
        update_status=get_update_status(),
    )

@app.route('/settings/timezone', methods=['POST'])
def settings_timezone():
    tz = request.form.get('timezone', 'Australia/Brisbane')
    s = load_settings()
    s['timezone'] = tz
    save_settings(s)
    flash('Timezone updated.', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/reset-setup', methods=['POST'])
def settings_reset_setup():
    s = load_settings()
    s['setup_completed'] = False
    s['setup_product'] = None
    save_settings(s)
    flash('Setup wizard reset. You will be redirected on your next visit to the dashboard.', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/check-update')
def settings_check_update():
    try:
        with open(VERSION_FILE) as f:
            current = f.read().strip()
    except Exception:
        current = '0.0.0'
    try:
        req = urllib.request.Request(GITHUB_VERSION_URL, headers={'User-Agent': 'AuraNet/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        latest = data.get('version', current)
        changelog = data.get('changelog', '')
        return jsonify({
            'current': current,
            'latest': latest,
            'update_available': latest != current,
            'changelog': changelog,
        })
    except Exception as e:
        return jsonify({'error': str(e), 'current': current})

@app.route('/settings/update', methods=['POST'])
def settings_update():
    update_dashboard_background()
    return redirect(url_for('settings') + '?updating=1')

@app.route('/settings/update/status')
def settings_update_status_route():
    return jsonify(get_update_status() or {'status': 'idle'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
