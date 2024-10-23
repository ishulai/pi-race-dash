# PI Race Dash

### Requirements

To run this, first install requirements: `pip install -r requirements.txt` or `pip3 install -r requirements.txt`.

### Simulation Mode

If you want to enable simulation mode to run this on a dev computer without live GPIO data, set the `SIMULATION_MODE` environment variable to `True`: `export SIMULATION_MODE=True`. Enabling this will open a second window for both the CLI and UI app with controls that allow you to modify the input values.

### CLI App

There's a CLI app for monitoring data without rendering a UI window. You can run it via `python3 cli.py`. It'll automatically update with live or simulated values.

### UI App

To run the UI app, run `python3 dash.py`. This will open a new window with the dash UI.