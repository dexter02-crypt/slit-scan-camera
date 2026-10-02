# Slit Scan Camera

Build a time-warp image from camera strips captured at different moments.

![Synthetic demonstration](docs/demo.png)

## Run independently

Use a standard desktop Python 3.12 installation. On Apple Silicon the pinned
OpenCV wheel requires macOS 13 or later. Do not install several different OpenCV
packages into the same environment.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python app.py check
.venv/bin/python app.py camera
```

## Controls

R restarts. V sweeps vertically; H sweeps horizontally. Space pauses. Move while the line advances. Q or Esc exits. Close one camera application before opening another.

No recording, network camera input, operating-system controls, or automatic uploads.
To allow an individual processed-image save, start `app.py camera --allow-snapshots`
and press S. Files are saved with unique names under ignored `outputs/`.

## Demonstration and limitations

`app.py demo` writes one synthetic demonstration. `docs/demo.gif` is a synthetic
sequence rendered by the application, not a measured camera performance result.

Time composites are visual effects, not evidence of physical shape or object identity.

Actual image processing and deterministic tests were exercised locally and in hosted CI.

On the maintainer Apple-Silicon Mac, Python 3.12.14 with OpenCV 4.13.0 and NumPy
2.3.5 passed the full test suite. A separate bounded camera-access smoke check read
60 consecutive frames from local camera index 0. That establishes camera acquisition,
not validation of the GUI controls or visual-effect quality.

See [validation](docs/VALIDATION.md) and [design](docs/DESIGN.md).

## License

MIT for the application; preserve [third-party notices](THIRD_PARTY.md).
