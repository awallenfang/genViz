# gen_viz

A visualizer generate for music videos with full GLSL shader support.

## Current status

I am currently still planning out the whole API and interactions that will allow me to add any amount of different visualizers. Most important is the ability to apply shaders in a nice way to each visualizer.

The end goal is to be able to bind a fragment shader to a visualizer and then position it on the screenspace. Then an audio stream is loaded, which is then used to do offline rendering for a video.

By binding the stream to the visualizer directly it'll also be possible to apply different streams to visualizers, as well as applying different filters before visualizing it