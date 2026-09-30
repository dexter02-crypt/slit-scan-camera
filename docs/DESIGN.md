# Design

An in-memory canvas receives the current frame only in the strip crossed since
the last timestamp. Speed is expressed in processed pixels per second. A long
processing gap is capped so it does not overwrite an enormous region at once.
The completed image stays frozen until reset. Horizontal/vertical switches reset
the canvas. Only one canvas is retained; there is no accumulated video history.
