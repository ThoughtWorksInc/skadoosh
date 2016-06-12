# Set the path
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from agent_portal import app, socketio

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("run", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=5000)
)

# Turn off debugger for production
manager.add_command("prod", Server(
    use_debugger=False,
    use_reloader=False,
    host='127.0.0.1',
    port=8080)
)

if __name__ == "__main__":
  # manager.run()
  socketio.run(app,debug=True,port=5000)