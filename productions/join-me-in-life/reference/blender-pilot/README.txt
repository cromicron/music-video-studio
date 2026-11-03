MELANCHOLY — BLENDER ANIMATION PROOF OF CONCEPT

Eight seconds, 24 fps, 1280 x 720, silent.

Open Melancholy_Blender_Pilot.blend in Blender 5.2 or newer.
All source images are packed into the project. Press Space to preview the
timeline; render with Blender's Render Animation command.

The project uses existing Blender features:
- A four-bone portrait armature with native keyframes for breathing, a small
  head tilt, and hair movement.
- Generated expression drawings combined in Blender's material nodes.
- A separate procedural mist layer and an orthographic camera.
- An editorial cut at frame 97 to the three-quarter portrait.
- Blender Cycles for rendering. No generative video service is used.

The original drawings were generated in ChatGPT. This is limited 2D animation,
not a fully rigged face or a continuous head-turn system. It demonstrates a
free rendering workflow; richer acting still needs more asset and rig work.

The MP4 was encoded with FFmpeg. No external paid API, subscription, or video
credits were used to make this proof of concept. Local or hosted compute still
requires a machine; this run used the existing conversation workspace.

The optional build_scene.py recreates the scene through Blender's API. It
automates Blender's tools; it does not implement a separate animation engine.
Run it with Blender's bpy Python module, or adapt it for Blender background
execution. Its default scene is 1920 x 1080; the delivered test is 720p.

Artwork and timing are provisional for testing the workflow.
