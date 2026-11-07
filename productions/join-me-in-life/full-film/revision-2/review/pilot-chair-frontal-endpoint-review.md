# V2C01 frontal chair rise — static endpoint source review

**PASS: STATIC ENDPOINTS ONLY, for a bounded self-supported rise pilot.** This does not approve generated motion or production use of the shot. It supersedes the framing problem of [sheet v1](pilot-chair-source-v1-review.md) only for the exact corrected crops below.

Independent reviewer: `/root/v2_outside_critic`, 7 November 2026. I inspected the whole [corrected sheet v2](../assets/pilot-guides/chair-rise-sheet-v2.png), then the actual start/end PNGs at native 616×352 size. The operator used the same relative FFmpeg crop for both endpoints; [crop provenance](../research/chair-rise-v2-crop-provenance.json) and the [machine review record](pilot-chair-frontal-endpoint-review.json) bind exact bytes and coordinates.

| Endpoint | Exact PNG SHA-256 |
| --- | --- |
| [Start](../assets/motion/pilot-inputs/chair-rise-v2/V2C01-start.png) | `2ad42ead32183f3af6e4a52ab1ca495609ed0a38d6ffa532ff4eedc679c40277` |
| [End](../assets/motion/pilot-inputs/chair-rise-v2/V2C01-end.png) | `ed386691b79eefdd818c57b4cef9adc405e5008f3add66e8fff9725e3a317736` |

Both crowns and complete shoes now have comfortable clearance. The same four foreground chairs, coat on A, woman at B, seated Jaro at C and available clinician behind/right remain visible. Window divisions, door and floor geometry are compatible. Character sides, clothes and adult proportions remain coherent; no duplicated actor or extra limb is visible. The standing woman's gaze is directed toward the care side rather than a celebratory look at the camera.

At start the woman leans forward with two separate hands bearing on her own armrests; both feet are supported on the floor. At end she stands in front of her seat with arms released to her sides. Jaro does not pull, lift or touch her, and the clinician remains available rather than helping physically. Frontal foot contacts are close enough for a natural supported rise; slight toe/orientation differences are not a promise of pixel-identical anchors.

**Approved pilot contract:** she settles her feet under herself, transfers weight forward, presses through her feet/armrests and rises under her own support, releasing the armrests after support has transferred. Keep the chairs fixed, both other people spatially stable, and all of her head/body/feet in frame. A floating pelvis, growing legs, simultaneous arm/leg morph, skating soles, chair movement or an invisible helper fails the motion test.

**Limits:** source faces and fingers are small and will be enlarged for model conditioning. Endpoint anatomy does not prove the intervening mechanics. The hospital cups/table are not visible in this diagnostic framing, so this review does not verify final V2-40 prop continuity or authorize direct insertion into the film. Any final performance still needs actual full-speed and dense-frame motion review, then a context/cut review with the song.
