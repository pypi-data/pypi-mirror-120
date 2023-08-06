from flask import Flask, Blueprint

from . import discover_devices, discover_media, player

bp = Blueprint('endpoints', __name__)

@bp.route("/discover_chromecasts")
def home():
    services = discover_devices.discover_chromecasts()
    chromecasts = []

    for chromecast in services or []:
        chromecasts.append({
            "ip": chromecast.host,
            "port": chromecast.port,
            "uuid": str(chromecast.uuid),
            "type": chromecast.model_name,
            "name": chromecast.friendly_name
        })

    return {"devices": chromecasts}

@bp.route("/oldcast/<ip>/<port>")
def oldcast(ip, port):
    player.play_file_to_chromecast(ip, port)
    return f"Success to {ip} and {port}??"

@bp.route("/cast/<input>/<ip>/<port>")
def cast(input, ip, port):
    player.play_media_to_chromecast(input, ip, port)
    return f"Success to {ip} and {port}??"

@bp.route("/discover_media")
def test():
    discover_media.discover_inputs()
    return {"inputs": discover_media.discover_inputs()}

@bp.route("/play")
def play():
    player.play()
    return "All good"

@bp.route("/stop")
def stop():
    player.stop()
    return "All good 1"