# Validation boundary

The final pack verifier reruns this repository's complete unittest suite and
`app.py check` after fresh ZIP extraction. It records counts and exit status in
the pack's `validation/` directory. Image-processing checks use real OpenCV.
Camera failure/cleanup checks may use test doubles. No physical webcam, macOS GUI
or remote GitHub Actions execution is claimed.
