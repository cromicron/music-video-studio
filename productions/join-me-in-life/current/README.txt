JOIN ME IN LIFE — MERCY IN MINOR
Revision 4: continuous waiting-room passage, held vowel, original band logo

CURRENT EDIT

The HYBRID files contain the current corrections. The three restrained files
are the unchanged Revision 3 comparison cut. This focused revision does not
change the lyric wording, the audio, the summer scene or the narrative ending.

The song answers Join Me in Death and challenges romanticizing suicide.
There is no recovery or decision-to-stay-alive resolution in this excerpt.
They begin apart; he embraces her once during the waiting-room lyric. Her
head supports itself, her hands stay passive, and her gaze remains away.

WAITING ROOM: ONE CONTINUOUS PASSAGE

30.167–34.000 s: the exact first frame of M01_Embrace.mp4 is held while the
camera opens into the framing used by the video. The prior push toward her
and subsequent reset to a wider frame are removed.
34.000–39.000 s: the embrace clip plays uninterrupted. The former 35.5–36.5 s
close-up cutaway is removed. The supporting hand and inward pull remain
visible in the portrait edit.
39.000–42.083 s: the exact movie endpoint is held. No new push begins here.

The wide camera makes one lead-in pullback, then lets the source action play.
The portrait camera opens into the matching crop, keeps the landing hand
visible and follows the pull rightward to reveal him. Shared continuous
camera paths avoid jumps, reversals and repeated endpoints at source joins.
The four timeline source sections are one continuous visual passage, not
four editorial shots. The only transitions are still/video/held endpoint.

SUSTAINED 'YOU'

The automatic alignment ended the first phrase's 'you' at 13.32 s, closing
his mouth while the vowel was still held. native_animation.py now retains
the rounded drawing through frame 339 (14.083 s), the last visible frame
before the 14.125 s cut. Its existing mouth onset and facial geometry remain.
This is a 19-frame exposure extension, not a new generated animation.

OPENING BRANDING

The original silver Mercy in Minor wordmark replaces the plain artist text
in the hybrid editions. It fades over the scene from 0.35 to 4.80 s, with
the song title below it. Portrait placement leaves her face clear; widescreen
placement sits in the upper-left window area. No extra title card is added.
assets/Band_Logo_Original.png is the original unmodified source graphic.
finish.py screens it in planar RGB (gbrp); do not apply Screen to YUV chroma
planes. The graphic and titles are final compositing, not baked into Blender.
brand_source.json records the existing artwork's identity.

DELIVERY

exports/ contains all six MP4s:
  Join_Me_in_Life_Short_Hybrid_Camera.mp4 — current vertical, lyric captions.
  Join_Me_in_Life_Short_Clean_Hybrid_Camera.mp4 — current vertical, no lyrics.
  Join_Me_in_Life_Widescreen_Hybrid_Camera.mp4 — current 1920x1080 website cut.
The three corresponding files without _Hybrid are unchanged restrained
Revision 3 references. All files are 24 fps and 1,439 picture frames.
The supplied stereo AAC is copied unchanged; picture length is 59.958 s
and source audio length is 59.950 s. No external publication was performed.

SOURCE AND REBUILD

Four portable .blend scenes are included. Images/audio are packed; the two
movie sources stay in assets/ using relative paths. Keep that folder beside
the native scenes. Only active artwork and approved references are bundled.

camera_shots_experimental.json — authoritative hybrid source/camera schedule.
camera_shots_simple.json — unchanged restrained reference schedule.
build_film.py — constructs scenes and checks every frame's image coverage.
native_animation.py — mouth exposures and tiny torso-interior controls.
render_existing.py — resumes a saved scene and supports partial ranges.
finish.py — opening logo, captions, original audio and final encoding.
review_revision4.py — targeted camera-join and held-mouth sample rendering.
validate_delivery.py — full decode, dimensions, audio and MP4-index checks.
package_project.py — bundles the six exports and the active portable source.
camera_revision_report.json / waiting_room_seam_checks.json — focused review.
REVIEW_NOTES.txt — earlier review history, with the current correction first.

Tested with bpy 5.2.3, Python 3.13 and FFmpeg/libx264/libass. No API keys or
additional generation credits are needed to render the supplied assets.

  blender -b --python build_film.py -- --cut experimental --format wide --render
  blender -b --python build_film.py -- --cut experimental --format vert --render
  python finish.py --cut experimental --format wide
  python finish.py --cut experimental --format vert --lyrics
  python finish.py --cut experimental --format vert

The encoder writes to the adjacent Revision_4 folder. It validates a complete
temporary MP4 before moving it into the delivery location. Native renders
skip existing JPEGs, so remove affected cached frames after changing source.
Intermediate frame caches are reproducible and omitted from the archive.

LIMITS AND REVIEW

The raw reach has brief hand blur at 1.5–2.0 s into its five-second source.
The prior attempt to hide it with another close-up caused the interruption
identified by the user. This edit keeps the action continuous. Band singing
uses limited drawn-mouth substitutions; it is not phoneme-complete lip sync.
The breathing treatment remains extremely small (under 1.1 source pixels).

Review covers native geometry, numerical camera paths, rendered source joins,
sequential frame samples, encoded samples and video/audio checks. It does not
claim normal-speed audiovisual playback. Additional paid generation: zero.
