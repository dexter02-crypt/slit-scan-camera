# slit-scan-camera 0.1.0

Slit Scan Camera is a small local OpenCV experiment that builds a time-warp image by combining strips captured at different moments.

## Highlights

- Horizontal and vertical slit-scan sweeps.
- Pause and reset controls.
- Local camera indexes only.
- No automatic recording or uploads.
- Still-image snapshots are disabled unless explicitly enabled.
- Synthetic demonstration and deterministic regression tests.

## Local validation

The maintainer Apple-Silicon Mac used:

- CPython 3.12.14
- OpenCV 4.13.0
- NumPy 2.3.5

The release-candidate test suite passed locally.

A bounded local-camera smoke check read 60 usable frames from camera index 0.

The synthetic demonstration created a readable 640 × 360 PNG.

## Scope

Slit-scan composites are visual effects. They are not reliable representations of physical shape, object identity, motion history, or measurement.

Physical camera acquisition is verified separately from GUI-control and visual-quality assessment.
