from flask import Flask, jsonify
import threading
import autosurf_worker

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Autosurf bot attivo su Render",
        "last_run": autosurf_worker.last_run_time,
        "running": autosurf_worker.is_running()
    })

@app.route("/start")
def start():
    if not autosurf_worker.is_running():
        t = threading.Thread(target=autosurf_worker.run_loop, daemon=True)
        t.start()
        return "✅ Worker avviato", 200
    return "⚠️ Worker già in esecuzione", 200

@app.route("/stop")
def stop():
    autosurf_worker.stop()
    return "⛔ Worker fermato (richiesta inviata)", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
