from flask import Flask, render_template, request, redirect, url_for, jsonify
from wakeonlan import send_magic_packet
import json
import os

app = Flask(__name__)

DATA_FILE = '/app/data/pcs.json'

# Load PCs from a JSON file
def load_pcs():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# Save PCs to a JSON file
def save_pcs(pcs):
    with open(DATA_FILE, 'w') as f:
        json.dump(pcs, f)

@app.route('/')
def index():
    pcs = load_pcs()
    return render_template('index.html', pcs=pcs)

@app.route('/add', methods=['POST'])
def add_pc():
    name = request.form['name']
    mac = request.form['mac']
    pcs = load_pcs()
    pcs.append({'name': name, 'mac': mac})
    save_pcs(pcs)
    return redirect(url_for('index'))

@app.route('/wake/<mac>')
def wake_pc(mac):
    send_magic_packet(mac)
    return jsonify(success=True)

@app.route('/delete/<mac>', methods=['POST'])
def delete_pc(mac):
    pcs = load_pcs()
    pcs = [pc for pc in pcs if pc['mac'] != mac]
    save_pcs(pcs)
    return jsonify(success=True)

@app.route('/wake_all')
def wake_all():
    pcs = load_pcs()
    for pc in pcs:
        send_magic_packet(pc['mac'])
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)