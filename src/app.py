from flask import Flask, render_template_string, request, redirect, url_for, jsonify, flash
from flask_cors import CORS
import json
import os
from src.notifier import notify_all

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/config.json')
STATUS_PATH = os.path.join(os.path.dirname(__file__), '../data/status.json')
LOG_PATH = os.path.join(os.path.dirname(__file__), '../data/notification_log.json')

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
CORS(app)  # Enable CORS for React frontend

# Modern HTML template with Google Fonts and CSS transitions
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ticketmaster Bot Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', Arial, sans-serif; margin: 40px; background: #f8fafc; }
        h1 { color: #2563eb; font-size: 2.5rem; margin-bottom: 0.5em; letter-spacing: -1px; }
        h2 { color: #334155; margin-top: 2em; margin-bottom: 0.5em; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; background: #fff; box-shadow: 0 2px 8px #0001; border-radius: 12px; overflow: hidden; }
        th, td { border: none; padding: 14px 16px; text-align: left; }
        th { background: #e0e7ef; color: #1e293b; font-weight: 700; font-size: 1.1em; }
        tr { transition: background 0.2s; }
        tr:hover { background: #f1f5f9; }
        td a { color: #2563eb; text-decoration: none; transition: color 0.2s; }
        td a:hover { color: #1d4ed8; text-decoration: underline; }
        form { margin-bottom: 20px; }
        .remove-btn { color: #ef4444; border: none; background: none; cursor: pointer; font-size: 1.1em; transition: color 0.2s, transform 0.2s; }
        .remove-btn:hover { color: #b91c1c; transform: scale(1.2) rotate(-10deg); }
        .edit-btn { color: #f59e42; border: none; background: none; cursor: pointer; font-size: 1.1em; margin-right: 8px; transition: color 0.2s, transform 0.2s; }
        .edit-btn:hover { color: #b45309; transform: scale(1.2) rotate(10deg); }
        .edit-form { display: flex; gap: 8px; }
        .edit-form input[type=url] { flex: 1; padding: 8px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1em; }
        .edit-form button { background: #2563eb; color: #fff; border: none; border-radius: 8px; padding: 8px 18px; font-size: 1em; font-weight: 700; cursor: pointer; transition: background 0.2s, transform 0.2s; }
        .edit-form button:hover { background: #1d4ed8; transform: scale(1.04); }
        .add-form { display: flex; gap: 12px; margin-top: 1em; }
        .add-form input[type=url] { flex: 1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1em; transition: border 0.2s; }
        .add-form input[type=url]:focus { border: 1.5px solid #2563eb; outline: none; }
        .add-form button { background: linear-gradient(90deg, #2563eb 60%, #60a5fa 100%); color: #fff; border: none; border-radius: 8px; padding: 12px 28px; font-size: 1.1em; font-weight: 700; cursor: pointer; box-shadow: 0 2px 8px #2563eb22; transition: background 0.2s, transform 0.2s; }
        .add-form button:hover { background: linear-gradient(90deg, #1d4ed8 60%, #38bdf8 100%); transform: translateY(-2px) scale(1.04); }
        .notify-btn { background: linear-gradient(90deg, #22c55e 60%, #38bdf8 100%); color: #fff; border: none; border-radius: 8px; padding: 12px 28px; font-size: 1.1em; font-weight: 700; cursor: pointer; box-shadow: 0 2px 8px #22c55e22; transition: background 0.2s, transform 0.2s; margin-bottom: 1.5em; }
        .notify-btn:hover { background: linear-gradient(90deg, #16a34a 60%, #2563eb 100%); transform: translateY(-2px) scale(1.04); }
        .flash { background: #d1fae5; color: #065f46; border: 1px solid #10b981; border-radius: 8px; padding: 12px 20px; margin-bottom: 1.5em; font-size: 1.1em; animation: fadeIn 0.7s; }
        .log-table { margin-bottom: 2em; }
        .log-table th { background: #bbf7d0; color: #166534; }
        .log-table td { font-size: 0.98em; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px);} to { opacity: 1; transform: none;} }
        @media (max-width: 700px) {
            body { margin: 10px; }
            table, th, td { font-size: 0.95em; }
            .add-form button, .notify-btn { padding: 10px 12px; font-size: 1em; }
        }
    </style>
    <script>
      function showEditForm(idx) {
        document.querySelectorAll('.edit-form').forEach(f => f.style.display = 'none');
        document.getElementById('edit-form-' + idx).style.display = 'flex';
        document.getElementById('event-row-' + idx).style.display = 'none';
      }
      function cancelEdit(idx) {
        document.getElementById('edit-form-' + idx).style.display = 'none';
        document.getElementById('event-row-' + idx).style.display = '';
      }
    </script>
</head>
<body>
    <h1>Ticketmaster Bot Dashboard</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    <form method="get" action="/notify">
        <button class="notify-btn" type="submit">Send Notification ✉️</button>
    </form>
    <h2>Notification Log</h2>
    <table class="log-table">
        <tr><th>Time</th><th>Subject</th><th>Message</th></tr>
        {% for log in notification_log %}
        <tr>
            <td>{{ log.timestamp }}</td>
            <td>{{ log.subject }}</td>
            <td>{{ log.message }}</td>
        </tr>
        {% endfor %}
        {% if notification_log|length == 0 %}
        <tr><td colspan="3" style="text-align:center; color:#888;">No notifications sent yet.</td></tr>
        {% endif %}
    </table>
    <h2>Monitored Events</h2>
    <table>
        <tr><th>Event URL</th><th>Status</th><th>Edit</th><th>Remove</th></tr>
        {% for url in urls %}
        <tr id="event-row-{{ loop.index0 }}">
            <td><a href="{{ url }}" target="_blank">{{ url }}</a></td>
            <td>{{ statuses.get(url, 'Unknown') }}</td>
            <td>
                <button class="edit-btn" type="button" onclick="showEditForm({{ loop.index0 }})" title="Edit">✎</button>
            </td>
            <td>
                <form method="post" action="/remove" style="display:inline;">
                    <input type="hidden" name="url" value="{{ url }}">
                    <button class="remove-btn" type="submit" title="Remove">✕</button>
                </form>
            </td>
        </tr>
        <tr id="edit-form-{{ loop.index0 }}" class="edit-form" style="display:none;">
            <form method="post" action="/edit">
                <input type="hidden" name="old_url" value="{{ url }}">
                <td colspan="2"><input type="url" name="new_url" value="{{ url }}" required style="width:100%"></td>
                <td colspan="1">
                    <button type="submit">Save</button>
                    <button type="button" onclick="cancelEdit({{ loop.index0 }})" style="background:#e5e7eb;color:#334155;">Cancel</button>
                </td>
            </form>
        </tr>
        {% endfor %}
    </table>
    <h2>Add Event</h2>
    <form class="add-form" method="post" action="/add">
        <input type="url" name="url" placeholder="Ticketmaster Event URL" required>
        <button type="submit">Add Event</button>
    </form>
</body>
</html>
'''

NOTIFY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Send Notification</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', Arial, sans-serif; margin: 40px; background: #f8fafc; }
        h1 { color: #2563eb; font-size: 2.2rem; margin-bottom: 1em; }
        form { background: #fff; padding: 32px 24px; border-radius: 12px; box-shadow: 0 2px 8px #0001; max-width: 500px; margin: 0 auto; display: flex; flex-direction: column; gap: 18px; }
        label { font-weight: 700; color: #334155; margin-bottom: 4px; }
        input[type=text], textarea { padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1em; transition: border 0.2s; }
        input[type=text]:focus, textarea:focus { border: 1.5px solid #2563eb; outline: none; }
        textarea { min-height: 80px; resize: vertical; }
        button { background: linear-gradient(90deg, #2563eb 60%, #60a5fa 100%); color: #fff; border: none; border-radius: 8px; padding: 12px 28px; font-size: 1.1em; font-weight: 700; cursor: pointer; box-shadow: 0 2px 8px #2563eb22; transition: background 0.2s, transform 0.2s; }
        button:hover { background: linear-gradient(90deg, #1d4ed8 60%, #38bdf8 100%); transform: translateY(-2px) scale(1.04); }
        a { color: #2563eb; text-decoration: none; font-size: 1em; margin-top: 1em; display: inline-block; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Send Notification</h1>
    <form method="post" action="/notify">
        <label for="message">Message</label>
        <textarea id="message" name="message" required placeholder="Type your notification message..."></textarea>
        <label for="subject">Subject (optional)</label>
        <input type="text" id="subject" name="subject" placeholder="Ticket Alert!">
        <button type="submit">Send Notification</button>
        <a href="/">← Back to Dashboard</a>
    </form>
</body>
</html>
'''

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def load_status():
    if os.path.exists(STATUS_PATH):
        with open(STATUS_PATH, 'r') as f:
            return json.load(f)
    return {}

def load_notification_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            return json.load(f)[:10]  # show 10 most recent
    return []

@app.route('/')
def dashboard():
    config = load_config()
    urls = config.get('urls', [])
    statuses = load_status()
    notification_log = load_notification_log()
    return render_template_string(TEMPLATE, urls=urls, statuses=statuses, notification_log=notification_log)

@app.route('/notify', methods=['GET', 'POST'])
def send_notification():
    if request.method == 'POST':
        message = request.form['message']
        subject = request.form.get('subject') or None
        notify_all(message, subject=subject)
        flash("Notification sent! Check your Telegram, Discord, or Slack.")
        return redirect(url_for('dashboard'))
    return render_template_string(NOTIFY_TEMPLATE)

@app.route('/add', methods=['POST'])
def add_event():
    url = request.form['url']
    config = load_config()
    urls = config.get('urls', [])
    if url not in urls:
        urls.append(url)
        config['urls'] = urls
        save_config(config)
    return redirect(url_for('dashboard'))

@app.route('/remove', methods=['POST'])
def remove_event():
    url = request.form['url']
    config = load_config()
    urls = config.get('urls', [])
    if url in urls:
        urls.remove(url)
        config['urls'] = urls
        save_config(config)
    return redirect(url_for('dashboard'))

@app.route('/edit', methods=['POST'])
def edit_event():
    old_url = request.form['old_url']
    new_url = request.form['new_url']
    config = load_config()
    urls = config.get('urls', [])
    if old_url in urls and new_url:
        idx = urls.index(old_url)
        urls[idx] = new_url
        config['urls'] = urls
        save_config(config)
        flash('Event URL updated!')
    return redirect(url_for('dashboard'))

# API Endpoints for React Frontend
@app.route('/api/events', methods=['GET'])
def api_get_events():
    """Get all monitored events"""
    config = load_config()
    urls = config.get('urls', [])
    statuses = load_status()
    
    events = []
    for url in urls:
        events.append({
            'url': url,
            'status': statuses.get(url, 'Unknown')
        })
    
    return jsonify({'events': events})

@app.route('/api/events', methods=['POST'])
def api_add_event():
    """Add a new event to monitor"""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    config = load_config()
    urls = config.get('urls', [])
    
    if url not in urls:
        urls.append(url)
        config['urls'] = urls
        save_config(config)
        return jsonify({'message': 'Event added successfully'}), 201
    else:
        return jsonify({'message': 'Event already exists'}), 200

@app.route('/api/events', methods=['DELETE'])
def api_remove_event():
    """Remove an event from monitoring"""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    config = load_config()
    urls = config.get('urls', [])
    
    if url in urls:
        urls.remove(url)
        config['urls'] = urls
        save_config(config)
        return jsonify({'message': 'Event removed successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    """Get recent notification log"""
    log = load_notification_log()
    return jsonify({'log': log})

@app.route('/api/notify', methods=['POST'])
def api_send_notification():
    """Send a notification via all configured channels"""
    data = request.get_json()
    message = data.get('message')
    subject = data.get('subject')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        notify_all(message, subject=subject)
        return jsonify({'message': 'Notification sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable (for production deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 