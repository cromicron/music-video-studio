# Corrected quiet motion — exact insertion implementation

7 November 2026. Root implementation report; outside source and sequence judgments remain separately hash-bound. This is not whole-film acceptance.

The active edit adopts R1L04 source `[3,135)` for S019 and successive R1L05 `[3,101)` / `[101,197)` for S030/S032. All326 selected frames play once at natural24fps, with full-image containment and no added lead/tail hold. The original exterior S031 separates the two held portions. Older L05/S030 is an inactive alternate. Original master and all shot boundaries remain unchanged.

[Source R1L04](ltx23-correction-R1L04-review.md) and [source R1L05](ltx23-correction-R1L05-review.md) pass. [First insertion review](r1-quiet-sequence-review.md) independently reconstructs every selected frame exactly and passes the motion/cadence/contact; it requires outgoing same-composition cut repairs. [Geometry-only correction](r1-waiting-seam-v2-review.md) fixes padding but still fails the residual face/detail reset.

The next candidate uses an intentional stationary S020 close-up of his anxious face, camera2.0 at(.67,.25), using the supplied original eye exposures. S021 returns to the original wide drawing. No new acting or generation is implied. Editor1.6.2 permits this explicit stationary close-up up to2.0 while retaining the ordinary1.5 ceiling; moving close-ups and larger crops fail validation. The abandoned guide-canvas renderer branch is removed. The [separate final close-up review](r1-waiting-closeup-review.md) now passes the exact V4 context and 1080p S020 crop, retaining very tight native crown headroom. Root adopts this deliberate cut. S032→S033 is deferred to the actual P1L06 replacement now generating.

| Export in `exports/` | Frames | SHA-256 |
|---|---:|---|
| `Join_Me_in_Life_Waiting_Correction_Proof.mp4` | 132 | `1fd2f4b81592fdb8702322410840a55d9a4065469224383cbce628d080bbd978` |
| `Join_Me_in_Life_Held_Correction_S030_Proof.mp4` | 98 | `41fe5fb16d18732537cb44f55eafd8351c53527810f63eaf489d5cf9b55fbd0c` |
| `Join_Me_in_Life_Held_Correction_S032_Proof.mp4` | 96 | `7a3f1b928cc6a2f44dfa90c21c2712f027bedd990235c7dc2afc885804aa0725` |
| `Join_Me_in_Life_Waiting_Correction_Context_Proof_v4.mp4` | 649 | `bddab2a000823c2298679bb698be43c80daa36cee8ab8316ad5578dcbfbf7a10` |

All listed proofs fully decode and retain zero-lag original-master excerpts (individual measurements in adjacent manifests). V4 covers S018–S022,649frames/27.041667s. Its internal S019 source interval is unchanged. Separate final-size S020 proof was rendered at1920×1080 in ignored `build/r1-waiting-closeup-1080.mp4`; that is a crop/detail check, not a finished full film.

Reproduce V4 from repository root:

```sh
python3 productions/join-me-in-life/full-film/edit.py --edit productions/join-me-in-life/full-film/edit-production-candidate.json --render --shots 18:22 --crf 18 --output productions/join-me-in-life/full-film/exports/Join_Me_in_Life_Waiting_Correction_Context_Proof_v4.mp4 --work-dir build/r1-waiting-context-v4
```

35 repository tests pass, including unchanged source/interval/hash gates, real cadence, contain borders, supplied exposure behavior and bounded explicit close-up validation. Fourteen story-wrapper tests also pass for all positive queues and original generation controls. Normal-speed playback and visual findings are recorded by the outside reviewer rather than inferred from decoding.
