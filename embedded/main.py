from flask import Flask, render_template, request
import threading
import control

app = Flask(__name__)
control.setup()

@app.route('/')
def system_startup():
    control.startup()
    return "SYSTEM INITIALIZED"

@app.route('/cycle', methods=['POST'])
def cycle():
    threading.Thread(target = control.main_cycle, args = ()).start()
    return "CYCLE INITIALIZED"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug = True)