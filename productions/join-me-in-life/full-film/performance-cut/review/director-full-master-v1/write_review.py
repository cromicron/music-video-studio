from pathlib import Path
import json,hashlib,datetime,shutil
D=Path(__file__).resolve().parent
root=next(p for p in D.parents if (p/'studio.json').exists())
P=root/'productions/join-me-in-life/full-film/performance-cut'
index=json.loads((D/'evidence-index-v1.json').read_text())
edit=json.loads((P/'edit/edit-v009.json').read_text())
notes=[
('Time/angle ellipse','Standing record-box task cuts to seated withdrawal; both remain in the blue apartment. The omitted sit and removal of the box are a deliberate time ellipse, not a continuous-action match.'),
('Reverse coverage','Her downcast close coverage answers his worried reverse. Screen-left man and screen-right woman, cream cups and blue kitchen remain legible.'),
('Movie to band','His open palm cuts to the bearded keyboardist at the silver keys. Curtain, leather outfit, fuller beard and sole cross distinguish the stage character from narrative Yaro.'),
('Band to movie','The keyboard phrase returns to her self-contained cloth/cup task. This is an alternating performance edit, not a claim that the keyboardist occupies the kitchen.'),
('Routine to emotional distance','Cloth rests on the counter and the cup is supported; closer seated coverage keeps her affect closed and his attention on her. A small face/pose change crosses a changed angle/time.'),
('Close to wide','The withdrawn face gives way to a wide view in which he begins to rise. Hands remain self-owned; her still seated posture contrasts with his restlessness.'),
('Movie to guitar','His standing worry cuts to the blonde guitarist on the established curtain stage. Instrument, costume and setting clearly separate her from the redhead.'),
('Guitar to ensemble','The five-person lineup establishes keyboardist rear-left, guitarist front-left, singer center, drummer rear and bassist right. It supports the isolated performance coverage.'),
('Ensemble to drums','A cut into the long dark-haired drummer preserves ornate dark clothing and black kit. Sticks are held by his own hands; no unattached hand appears at the boundary.'),
('Drums to lead vocal','Rhythm coverage gives way to a supported handheld microphone and open singing mouth. Center singer identity and disc pendant remain distinct from the keyboardist.'),
('Vocal coverage change','Handheld medium coverage cuts to the repaired supported stand microphone close angle. This is a visible performance/time ellipse, not one uninterrupted mic handoff; the stand and cable are physically readable.'),
('Voice to instrument','The vocal close-up cuts to tighter guitar coverage. Clipped upper hair is a deliberate framing cost; eyes, face, picking hand, fretting hand and instrument remain readable.'),
('Band to present','The guitar passage returns to the familiar seated pair and two cups. Her faint, self-contained face and separate hands do not imply recovery or an invitation to duet.'),
('Present to bass','A brief closed near-glance leads to the tied-blond bassist on stage; the return to performance does not convert her courtesy into an emotional resolution.'),
('Bass to present','The bassist bows toward his instrument; the next image is her folded/downcast private posture. The contrast is intelligible and the cream cups return as established props.'),
('Girl to fearful observer','Her hands settle into her lap before tighter coverage of his drawn face. This directs attention to his inability to reach her rather than to a new location.'),
('Present to summer memory','His apprehensive blue-kitchen look cuts to both laughing with shared earbuds in the courtyard. Warm practical lights and their open expressions plainly mark the sole happy recollection.'),
('Memory continuity','The final dusk courtyard pose and first original summer-source pose are closely aligned. Shared earbuds, seated order and clothes preserve the same private memory.'),
('Memory angle/time change','Dusk courtyard coverage cuts to a brighter golden close angle of their shared laughter. The lighting/scale change is noticeable, but the same earbuds, shirts, brick setting and activity read as a compressed summer recollection, not an imagined future.'),
('Memory to present','Their mutual laughter cuts decisively back to blue-kitchen silence, his concern and her closed eyes. This is the required joy/depression contrast, with no extra dream world.'),
('Practiced-courtesy callback','The closer withdrawn pair cuts to the wider unused C05 tail. His lean/posture and her table hand reset across the angle/time ellipse. Her short lidded look and faint courtesy remain contained, with no reach, tears or broad joyful answer.'),
('Callback to lead vocal','Her face settles flatter before the cut to Yaro singing on stage. The leather/burgundy stage outfit, curtain and handheld mic make the two modes clear at the next phrase.'),
('Vocal to drums','Close vocal coverage cuts to an active drum image. Peripheral fringe/reflection softness stays at the outer curtain edges, while the drummer, owned hands and central kit remain legible.'),
('Drums to present cup','The brief drum insert returns to her hand on the supported cream mug. The stage motion does not create a kitchen action jump; the private scene remains closed and quiet.'),
('Present time ellipse','Her cup and hand are settled at the outgoing boundary; his next open palm and changed head direction are a visible time/coverage reset. The warm left light patch is localized in the same blue apartment, not a return to the golden memory.'),
('Tighter present coverage','The cut moves closer to his self-directed frustration; the table drops below the crop, her separate folded hands remain visible. His raised hand is directed near his own head, not toward her body.'),
('Movie to repaired keys','His downcast posture cuts to the corrected keyboard take. Both keyboard hands are owned, cross and beard remain clear, and the rejected ornate-cuffed foreground arms are absent.'),
('Keys to bass','The repaired keyboard coverage passes to the tied-blond bassist in the same stage palette. No new performer or instrument ownership change is suggested.'),
('Bass to ensemble','The bassist close coverage expands to all five performers in their established positions. The medium-wide composition clips some lower extremities/stand feet but preserves all identities and instruments.'),
('Ensemble to recognition','The instrumental/ensemble passage cuts out to his fearful kitchen face at the recognition bridge. The band then stays away throughout the private recognition and four pleas.'),
('Fear to composed girl','His tense look is answered by her quiet cup-side composition. Her composure reads as emotional distance rather than reassurance; his fear remains unanswered.'),
('Changed angle before pleas','Her near-glance in C27 cuts to downcast O03 with a different visible hand pose and angle. This is an editorial time ellipse, not a seamless cup-action match. The mug remains table-supported; her affect stays closed.'),
('First forceful plea','O03 ends on a small near/upward gaze with a closed mouth, not comfort. The immediate cut to his already tearful open plea makes the recognition painful from the first call.'),
('Second forceful plea','A changed close performance angle continues the tearful strain into the second call. The face and mouth do not become a smile or new identity; this is emphatic rhythmic coverage rather than one continuous take.'),
('Third forceful plea','The second call gives way to another tight, open-mouthed plea. Similar scale and kitchen geography preserve intensity; no band, memory or hopeful cut interrupts it.'),
('Fourth forceful plea','His briefly closing eyes at the third ending cut to the fourth open, strained call. It sustains desperation rather than resetting to a gentle verse delivery.'),
('Plea to private aftermath','The fourth close plea cuts to the wider pair, with his open hand still unanswered. Her downcast posture prevents the wider scale from reading as sudden repair; distant tear detail is less visible.'),
('Aftermath coverage reset','Nearly matching wide coverage continues into a small hand hover. There is a modest hand/head timing reset at the cut, but separate bodies, cups and the unresolved distance remain clear.'),
('Girl self-containment','His watching posture cuts closer to her own clasped hands. The omitted hand movement is a small angle/time ellipse; it is self-soothing/containment, not mutual handholding or a new narrative event.'),
('Last energetic band insert','Her clasped, closed posture cuts to the late drum accent. The disjoint source interval supplies fresh rhythm without inserting the band into the private recognition sequence.'),
('Drums to exhausted pair','The late accent returns to his heavy, open-mouthed breath and her bowed head. There is no victory gesture, grin or recovered duet.'),
('Quiet final band coverage','His exhausted face passes to a restrained guitar close-up, not a triumphant ensemble. Tight crown/headstock-edge framing remains a disclosed compromise; face and hands stay readable.'),
('Band exit to private ending','The guitar player begins to lift her listening gaze; the cut returns to the two private characters. The final 18.5 seconds then remain entirely in the apartment.'),
('Pair to cup close coverage','The pair angle cuts to her alone beside the mug; a small lap-to-cup hand lift is not shown across the cut. It is an acceptable coverage ellipse, not a continuous contact match or a miraculous prop move.'),
('Tighter final angle','C38 exits downcast, with her hand to the left of the left-handled mug. O04 begins with the same hand/mug/table relationship in a tighter two-person angle and him plausibly visible at left. Subsequent tears and the sustained look do not reverse this geography.')
]
assert len(notes)==45
for j,(kind,note) in zip(index['joins'],notes):
 j['assessment']='PASS_SCOPED_JOIN';j['editorial_kind']=kind;j['actual_finding']=note
 j['viewed_as_panel']=f"join-panel-{(j['index']-1)//5+1:02}.jpg"
summary={
 'schema':'jml-performance-final-director-findings-draft/v1',
 'state':'STATIC_REVIEW_COMPLETE_FULL_PLAYBACK_PENDING',
 'master':index['master'],'edit':index['edit'],
 'actually_inspected_join_count':45,'join_reviews':index['joins'],
 'chronological_overviews_actually_viewed':[f'overview-{i:02}.jpg' for i in range(4)],
 'output_native_targets_actually_viewed':index['native_targets'],
 'global_directorial_findings':[
  {'area':'Opening order and false peace','finding':'The record sleeves lower into an open box before later cloth/cup tidying; his watchful tense face and her economical, withdrawn routine establish a frightening calm. This is fictional character direction in the song context, not a claim that ordinary tidiness diagnoses suicidality. The sit between O01 and C02 is omitted as a clear time ellipse.'},
  {'area':'Only one happy memory','finding':'Only C15/C16/C17 leave the present for the same shared-earbud courtyard memory, at114.75–134.375s. Their laughter and amateur private singing create the needed contrast. The redhead remains a narrative character, not an additional band vocalist. No clinic or imagined future is used.'},
  {'area':'Band cast and integration','finding':'Isolated keys, guitar, bass, drums, three usable lead-vocal shots and two ensembles form a coherent stage thread. The bearded spiky-haired keyboardist has the clearly readable cross; Yaro has the round disc, the guitarist an ornate medallion and the other musicians no clearly depicted cross. Five distinct identities and established positions remain legible. Repaired B10 has no disconnected foreground arms.'},
  {'area':'Present-time courtesy is not a cure','finding':'The C05 return/callback includes small lidded near-glances and a faint courteous mouth shape, not an absolute mask with no micro-expression. Her hands stay separate, face settles flatter, and the cold room/next withdrawal keep it a failed contact. That preserves a meaningful difference from the final wet, vulnerable look.'},
  {'area':'Recognition and all four pleas','finding':'After the B12 exit at191.583s, his fear, her composed routine and O03 closed affect remain private. The entire C29/C30/C31/C32 sequence207.875–223.5s is intact and forceful from the first plea. The rising emotional texture comes from sustained strain and tears across changed close angles, not anger directed physically at her. There is no cutaway band or future-image comfort during it.'},
  {'area':'Late musical energy and withdrawal','finding':'The final drum accent at241.958–247.125s supplies rhythm before his exhaustion; restrained guitar at254.625–259.292s serves as the last band image. The last18.5s are private, and the original song continues under them.'},
  {'area':'Ambivalent ending','finding':'O04 starts downcast, the tear appears before the look turns toward him, and the final picture holds the tearful near-contact. The face is vulnerable, the mouth slightly parted/quiet, and neither character supplies a smile, nod, forced embrace or a completed recovery. The cause of the tears remains open to grief or fragile connection. The ending does not turn down again after the final look.'}
 ],
 'nonblocking_limits':[
  'Native source detail is limited and generally upscaled into1920x1080; fine hair, eyelids, small jewelry and instrument edges can soften. Output-native evidence is not a claim of native1080 source generation.',
  'B06 is visibly tighter than B02 and clips the crown/occasionally a headstock edge; the crop is acceptable performance coverage because the face, hands and guitar action stay readable.',
  'B09 outer curtain tassel/reflection/smoke contours soften. Those peripheral forms do not establish extra players and are not an excuse for malformed body anatomy; central hands/sticks/face remain legible in inspected actual-master frames and accepted source review.',
  'This is an elliptical music-video edit: standing-to-seated opening, repeated kitchen angles, handheld-to-stand vocal coverage, courtyard lighting change, callback posture reset and final lap-to-cup omission are visible angle/time changes, not seamless continuous action.',
  'All45actual cut pairs were visually inspected as9compact JPEG panels, each containing5pairs;46shot midpoints were inspected in4chronological overviews, plus13output-native targets. This is not direct visual inspection of all6667master frames. Existing hash-bound native-motion source gates and the separate all-frame master verifier remain part of the evidence.',
  'Actual unmuted normal-speed browser execution records playback behavior and captured moments; it is not a claim of subjective human hearing, perfect instrument/note synchronization or perfect phoneme alignment.'
 ]
}
(D/'findings-draft-v1.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print('Saved static findings for all45joins; no global PASS frozen before actual complete playback')
