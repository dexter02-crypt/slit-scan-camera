# Validation boundary — 2 October 2026

## Maintainer Mac

The release candidate was validated on an Apple-Silicon Mac using:

- CPython 3.12.14
- OpenCV 4.13.0
- NumPy 2.3.5

The complete local unittest suite passed.

`app.py check` passed using real NumPy/OpenCV processing.

`app.py demo` created a readable 640 × 360 three-channel PNG from the synthetic demonstration.

A separate bounded physical-camera acquisition smoke check opened local camera index 0 and returned 60 usable frames from 60 read attempts.

That camera check establishes local camera access only. It does not establish GUI interaction, snapshot-button behavior on real hardware, timing quality, or visual-effect quality.

## Automated scope

Tests cover:

- frame validation
- local-camera source restrictions
- failed-camera cleanup
- processing-error cleanup
- explicit unique local image saves
- symlink-output refusal
- panel input preservation
- temporal strip composition
- pause/reset behavior
- horizontal and vertical scan behavior
- completed-scan stability
- frame-shape changes
- bounded time gaps
- time-reversal rejection
- invalid speed rejection
- release version identity

The synthetic demonstration is not a camera-performance benchmark.

No physical-shape, identity, recognition, or measurement claim is made from slit-scan output.
