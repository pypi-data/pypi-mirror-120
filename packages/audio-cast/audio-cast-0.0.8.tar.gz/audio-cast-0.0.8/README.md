# Application to cast streams to chromecast

## Usage

- When using VS Code, just run the debugger.
- When starting from termimal.
  1. Set environment variable for `FLASK_APP`.
     - Linux/osX: `export set FLASK_APP=src.audio_cast.webapp`
     - Windows: `set FLASK_APP=src.audio_cast.webapp`
  2. Launch the server with `python -m flask run`.

## Next steps

- [ ] Run it in the Rpi
- [ ] Run new version to fix `No chromecasts found`.
- [ ] Figure out why no chromecasts are found.
- [ ] Check local debugger works.
  - [ ] Delete `webapp` file.
- [ ] Update README.md with new instructions.
- [ ] Check tutorial to upload package using apt.
  - [Package python for apt](https://monadical.com/posts/how-to-package-python-for-apt-deb.html)
  - [Packaging Python](https://docs.python-guide.org/shipping/packaging/)
  - [Deploying demo flask project](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/)
  - [Installing demo flask project](https://flask.palletsprojects.com/en/2.0.x/tutorial/install/)
- [ ] Enable CLI
  - [Enabling CLI demo flask project](https://flask.palletsprojects.com/en/2.0.x/cli/)
- [ ] Check how to get inputs in linux using Rpi.

## Cheatsheet

- To upload:
  - Build: `py -m build`
  - Deploy: `py -m twine upload dist/*`
- To run locally:
  - Set environment variable `FLASK_APP=audio_cast`
- To run after installation from package:
  - Install waitress `python3 -m pip install waitress`
  - Run waitress `waitress-serve --call --host=localhost --port=5000 'audio_cast.create_app'`
- Virtual environment:
  - Create: `python3 -m venv <DIR>`
  - Start: linux - `source <DIR>/bin/activate` - windows - `<DIR>/Scripts/activate`
  - Stop: `deactivate`
  - To clear delete the directory and create again `rm -r <DIR>`
- Token for Pypi is in the local projects folder.
- Install packages from `requirements.txt` `pip install -r requirements.txt`.
