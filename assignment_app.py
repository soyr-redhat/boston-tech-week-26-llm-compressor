#!/usr/bin/env python3
"""
Workshop User Assignment App
Automatically assigns participants to pre-provisioned JupyterLab instances
"""

from flask import Flask, render_template_string, redirect, session, jsonify
import json
import os
import subprocess
from pathlib import Path
from threading import Lock

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'workshop-secret-key-change-in-prod')

# Configuration
TOTAL_USERS = int(os.environ.get('TOTAL_USERS', '50'))
BASE_URL = os.environ.get('BASE_URL', 'https://jupyter-{user_id}.apps.ocp.ntdrq.sandbox503.opentlc.com')
ASSIGNMENTS_FILE = Path('/tmp/assignments.json')
AUTO_PROVISION = os.environ.get('AUTO_PROVISION', 'true').lower() == 'true'
NAMESPACE = os.environ.get('NAMESPACE', 'workshop')

# Thread-safe lock for assignments
assignments_lock = Lock()

def load_assignments():
    """Load assignment state from disk"""
    if ASSIGNMENTS_FILE.exists():
        with open(ASSIGNMENTS_FILE, 'r') as f:
            return json.load(f)
    return {
        'next_available': 1,
        'assignments': {},  # session_id -> user_number
        'used': []  # list of used user numbers
    }

def save_assignments(state):
    """Save assignment state to disk"""
    with open(ASSIGNMENTS_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def provision_user(user_number):
    """Provision a new JupyterLab instance for user"""
    user_id = f'user{user_number}'

    try:
        # Run oc process and apply
        cmd = f"""
        oc process -f /app/jupyter-user-template.yaml \
          -p USER_ID={user_id} \
          --namespace={NAMESPACE} \
          | oc apply -n {NAMESPACE} -f -
        """

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ Failed to provision {user_id}: {result.stderr}")
            return False

        print(f"✓ Auto-provisioned {user_id}")
        return True

    except Exception as e:
        print(f"❌ Error provisioning {user_id}: {e}")
        return False

def get_assignment(session_id):
    """Get or create assignment for this session"""
    with assignments_lock:
        state = load_assignments()

        # Check if this session already has an assignment
        if session_id in state['assignments']:
            return state['assignments'][session_id]

        # Find next available user
        next_user = state['next_available']

        # Auto-provision if we've exceeded pre-provisioned capacity
        if next_user > TOTAL_USERS and AUTO_PROVISION:
            print(f"Capacity exceeded ({TOTAL_USERS}), auto-provisioning user{next_user}...")
            if not provision_user(next_user):
                return None  # Failed to provision
        elif next_user > TOTAL_USERS:
            return None  # No auto-provisioning, workshop full

        # Assign user
        state['assignments'][session_id] = next_user
        state['used'].append(next_user)
        state['next_available'] = next_user + 1

        save_assignments(state)
        return next_user

LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boston Tech Week 2026 - LLM Quantization Workshop</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Red Hat Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #2f383e 0%, #1a1f23 100%);
            color: #d3c6aa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            background: rgba(47, 56, 62, 0.9);
            border: 2px solid #4a5459;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        h1 {
            color: #ee0000;
            font-size: 2em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        h2 {
            color: #a7c080;
            font-size: 1.5em;
            margin-bottom: 30px;
            font-weight: 400;
        }

        .info {
            background: rgba(26, 31, 35, 0.6);
            border-left: 4px solid #a7c080;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 4px;
        }

        .info p {
            line-height: 1.6;
            margin-bottom: 10px;
        }

        .info strong {
            color: #e68183;
        }

        .button {
            display: block;
            width: 100%;
            background: linear-gradient(135deg, #ee0000 0%, #c00000 100%);
            color: white;
            border: none;
            padding: 18px 32px;
            font-size: 1.2em;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(238, 0, 0, 0.3);
        }

        .button:hover {
            background: linear-gradient(135deg, #c00000 0%, #a00000 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(238, 0, 0, 0.4);
        }

        .stats {
            margin-top: 30px;
            text-align: center;
            font-size: 0.9em;
            color: #a7c080;
        }

        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #4a5459;
            text-align: center;
            font-size: 0.85em;
            color: #859289;
        }

        .footer a {
            color: #a7c080;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Boston Tech Week 2026</h1>
        <h2>LLM Quantization Workshop</h2>

        <div class="info">
            <p><strong>Duration:</strong> 60 minutes</p>
            <p><strong>Format:</strong> Interactive notebook in your browser</p>
            <p><strong>What you'll do:</strong></p>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>Benchmark an FP16 model</li>
                <li>Benchmark an INT4 quantized model</li>
                <li>Compare performance with interactive charts</li>
            </ul>
        </div>

        <a href="/assign" class="button">Get My Workspace</a>

        <div class="stats">
            <p>{{ assigned }} / {{ total }} workspaces assigned</p>
        </div>

        <div class="footer">
            <p>Powered by vLLM, guidellm, and OpenShift</p>
            <p><a href="https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor" target="_blank">View on GitHub</a></p>
        </div>
    </div>
</body>
</html>
"""

ASSIGNED_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Workshop Workspace</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Red Hat Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #2f383e 0%, #1a1f23 100%);
            color: #d3c6aa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            background: rgba(47, 56, 62, 0.9);
            border: 2px solid #4a5459;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            text-align: center;
        }

        h1 {
            color: #a7c080;
            font-size: 2em;
            margin-bottom: 20px;
        }

        .user-id {
            font-size: 3em;
            color: #ee0000;
            font-weight: 700;
            margin: 20px 0;
        }

        .info {
            background: rgba(26, 31, 35, 0.6);
            border-left: 4px solid #a7c080;
            padding: 20px;
            margin: 30px 0;
            border-radius: 4px;
            text-align: left;
        }

        .url {
            background: rgba(26, 31, 35, 0.8);
            padding: 15px;
            border-radius: 6px;
            font-family: 'Red Hat Mono', monospace;
            font-size: 0.9em;
            word-break: break-all;
            margin: 20px 0;
            border: 1px solid #4a5459;
        }

        .button {
            display: inline-block;
            background: linear-gradient(135deg, #ee0000 0%, #c00000 100%);
            color: white;
            border: none;
            padding: 18px 32px;
            font-size: 1.2em;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(238, 0, 0, 0.3);
            margin-top: 20px;
        }

        .button:hover {
            background: linear-gradient(135deg, #c00000 0%, #a00000 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(238, 0, 0, 0.4);
        }

        .countdown {
            margin-top: 20px;
            font-size: 0.9em;
            color: #859289;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Workspace is Ready!</h1>

        <div class="user-id">User {{ user_number }}</div>

        <div class="info">
            <p><strong>Your personal JupyterLab:</strong></p>
            <div class="url">{{ workspace_url }}</div>
            <p style="margin-top: 15px;"><strong>Bookmark this page</strong> so you can return to your workspace later!</p>
        </div>

        <a href="{{ workspace_url }}" class="button">Open JupyterLab</a>

        <div class="countdown">
            <p>Redirecting automatically in <span id="countdown">5</span> seconds...</p>
        </div>
    </div>

    <script>
        let seconds = 5;
        const countdownEl = document.getElementById('countdown');
        const workspaceUrl = "{{ workspace_url }}";

        const interval = setInterval(() => {
            seconds--;
            countdownEl.textContent = seconds;
            if (seconds <= 0) {
                clearInterval(interval);
                window.location.href = workspaceUrl;
            }
        }, 1000);
    </script>
</body>
</html>
"""

FULL_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workshop Full</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Red Hat Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #2f383e 0%, #1a1f23 100%);
            color: #d3c6aa;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            background: rgba(47, 56, 62, 0.9);
            border: 2px solid #4a5459;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            text-align: center;
        }

        h1 {
            color: #e68183;
            font-size: 2em;
            margin-bottom: 20px;
        }

        p {
            line-height: 1.6;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Workshop Full</h1>
        <p>All {{ total }} workspaces have been assigned.</p>
        <p>Please contact the workshop instructor for assistance.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Landing page"""
    state = load_assignments()
    assigned = len(state['assignments'])

    return render_template_string(
        LANDING_PAGE,
        assigned=assigned,
        total=TOTAL_USERS
    )

@app.route('/assign')
def assign():
    """Assign workspace to user"""
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()

    session_id = session['session_id']

    # Get assignment
    user_number = get_assignment(session_id)

    if user_number is None:
        # Workshop is full
        return render_template_string(FULL_PAGE, total=TOTAL_USERS)

    # Store in session for easy retrieval
    session['user_number'] = user_number

    # Build workspace URL
    workspace_url = BASE_URL.format(user_id=f'user{user_number}')

    return render_template_string(
        ASSIGNED_PAGE,
        user_number=user_number,
        workspace_url=workspace_url
    )

@app.route('/status')
def status():
    """API endpoint to check assignment status"""
    state = load_assignments()
    return jsonify({
        'total_users': TOTAL_USERS,
        'assigned': len(state['assignments']),
        'available': TOTAL_USERS - len(state['assignments']),
        'next_available': state['next_available'] if state['next_available'] <= TOTAL_USERS else None
    })

@app.route('/reset')
def reset():
    """Reset all assignments (admin only)"""
    # In production, add authentication here
    if ASSIGNMENTS_FILE.exists():
        ASSIGNMENTS_FILE.unlink()
    return jsonify({'status': 'reset', 'message': 'All assignments cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
