from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent;P=D.parents[1];R=Path('/workspace/music-video-studio')
def ref(p):
 p=Path(p);return {'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,d):
 assert not p.exists(),f'Immutable review already exists: {p}'
 p.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(ref(p)))
verification=json.loads((P/'research/middle-c-v2-output-verification.json').read_text())
play=json.loads((D/'playback-unmuted-v1.json').read_text())
joined=P/'exports/C20_C26_Middle_C_Unbound_Diagnostic_v1.mp4'
assert ref(joined)['sha256']=='7031cddd661238541b33d93d84bd014f8ca29143948d00dac15cff26c20fa6da'
observations={
'C21':[
'The anatomical right forearm withdraws from the screen-left gold display and lowers onto his own knee/lap behind the cream mug; the left hand stays on his own thigh. His head turns toward the woman; she stays closed/downcast. The gold plane recedes.',
'Consecutive native hand/prop crops raw64–114 show a monotonic withdrawal and settle, no hand switch, cup displacement, grasp or crossing through the mug. The mug occludes the lowering fingers near raw88 onward. Fine finger lines soften/smear during the turn around raw72–81, but the connected hand silhouette and arm trajectory remain readable.',
'Exact raw6 and raw157 plus consecutive entry/exit windows preserve identity, anatomy and supported props. No blocking endpoint redraw found.'
],
'C22':[
'Actual action differs from frozen plan: he lifts his anatomical right hand from his knee toward his own lowered face, holds it open with curled/tensed fingers, then lowers it open to the knee. He does not show the planned grounded wrist with a closed fist then release. His left hand stays on his thigh. This is a self-contained gesture; he does not reach toward or control her.',
'Consecutive native raw30–137 show connected wrist/forearm, readable finger flexion and coherent lift/lower. Some intermediate finger/wrist detail softens around raw40–42 and raw128–130, without an extra limb, persistent malformed hand or broken trajectory. A tentative sheet-based suspicion of raw35→36 reversal was explicitly retracted after exact full-native raw33–38 examination: raw34/35/36 are the same lifted pose with texture changes, then raw37 advances upward.',
'She briefly opens her eyes toward his side/downward while he lowers his head, then returns to closed/downcast eyes; there is no smile, touch or reciprocal comforting gesture. Exact raw6/raw146 and their consecutive boundary windows remain coherent.',
'Mechanics and isolated insertion pass for the literal raised-hand action. Root must explicitly reconcile the creative departure from the agent-authored clench contract before editorial adoption; this review does not silently rewrite that contract.'
],
'C23':[
'Three bounded gold season planes rotate inward around the seated blue-room pair. The real table, two supported cream cups, chairs, connected hands on own thighs/lap, blue jeans and low canvas footwear remain stable. He glances slightly down then toward her; she stays withdrawn.',
'Dense full-range every4 samples, ranked transition/reversal neighborhoods and native entry/exit windows show no blocking real-table warp, cup slide, identity replacement or anatomy break. Motion comes chiefly from gold planes and slight acting, not an inferred meaning from unique frame counts.'
],
'C24':[
'The foreground gold season plane turns across the camera view, substantially occluding the couple around the middle, then clears to reveal the same seated pair. The room also makes a modest lateral perspective shift. This is a more prominent pane passage than a simple edge-on fold.',
'Dense samples, ranked changes and consecutive raw118–139 reveal samples preserve the two people, separate own hands, supported mugs, rigid table edges/legs and shoe positions through the reveal. The table and people translate/perspective-shift together; no independent stretching or mug teleport is visible. Gold imagery is an overlay/occluder, not a replacement physical kitchen.',
'Native raw6/raw173 and consecutive boundary windows have no blocking pose/identity redraw. Small texture/line shimmer persists, especially on luminous panes and floor reflections.'
],
'C25':[
'The tall warm kitchen plane steadily narrows behind her while the blue-room couple remain grounded and separate. Both cream cup handles retain their screen-left orientation and the mugs remain fixed on the table; no hand/prop action is invented. She closes/lowers her eyes and he continues searching her face.',
'At final retained raw154 the plane is a narrow gold sliver with a trace of warm interior, not yet the almost zero-width line reached around raw165–168 outside keeper. The cut to C26 removes the remaining sliver by an editorial elision; no range change is recommended.',
'Native entry/exit windows and full-range dense samples show stable people, hands, room/table and cups. No blocking endpoint jump or geometry failure found.'
]}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
shots=[]
for take in verification['takes']:
 s=take['take_id'];seg=take['planned_intervals']['segments'][0];src=R/take['video'];assert ref(src)['sha256']==take['video_sha256']
 run=next(x for x in play['runs'] if x['shot']==s)
 assert run['telemetry']['ended'] and run['telemetry']['quality']['dropped']==0
 shots.append({'shot':s,'source':ref(src),'raw_frames':take['frames'],'proposed_keeper':seg['source_frames'],'proposed_master_range':seg['timeline_frames'],'approved_ranges':[{'raw':seg['source_frames'],'master':seg['timeline_frames']}],'verdict':'PASS_SCOPED_MECHANICS_AND_ISOLATED_INSERTION','story_reconciliation_required':s=='C22','literal_observations':observations[s],'frozen_action_contract':take['action_contract'],'original_song_diagnostic':ref(Path(run['source'])),'triage_sidecar':ref(P/f'research/middle-c-v2-{s}-temporal-triage.json'),'decoded_frame_selection':ref(D/f'{s}-inspection-selection.json'),'ranked_selection':ref(D/f'{s}-ranked-selection.json'),'consecutive_contact_selection':ref(D/f'{s}-consecutive-selection.json') if s in ['C21','C22'] else None})
manifest=[]
for f in sorted(D.iterdir()):
 if f.is_file() and f.name not in ['evidence-manifest-v1.json','write_reviews.py']:manifest.append(ref(f))
write(D/'evidence-manifest-v1.json',{'schema':'jml-review-evidence-manifest/v1','files':manifest,'storage':'Bounded streamed decode and JPEG/native crop evidence, no full RGB dumps. Source pictures remain unchanged. Joined cut sheets are decoded at1920x1080 then scaled896x504; source native frames are896x512.'})
limits=['This is an independent scoped mechanics/insertion review, not user creative acceptance or full-film acceptance.','Actual complete 1x browser execution and inspected captures are evidenced; telemetry is not subjective hearing, physical audio-device confirmation, exact lip sync or every-frame human watching.','Dense every4 overview plus native consecutive risky hand actions and exact boundary windows cannot establish that every possible defect in every uninspected frame is absent.','C20/C26 pre-existing source acceptance is not re-reviewed here; only their newly adjacent cuts are covered.','C22 passes mechanics for its actual raised-hand gesture; planned knee clench is absent. Root story reconciliation remains separate.','No source/range/timing edit, binding, provider job, still hold, repeat/loop, reversal or generated replacement was made by this reviewer.']
source_review=P/'review/middle-c-v2-motion-review-v1.json'
write(source_review,{'schema':'jml-independent-motion-review/v1','reviewer':'c_final_middle_review','reviewed_at_utc':now,'verdict':'PASS_FIVE_SCOPED_SOURCE_MECHANICS_WITH_C22_STORY_RECONCILIATION','shots':shots,'evidence_manifest':ref(D/'evidence-manifest-v1.json'),'playback':ref(D/'playback-unmuted-v1.json'),'technical_verification':ref(P/'research/middle-c-v2-output-verification.json'),'limits':limits})
notes=[
('C20','C21',196,3820,'Gold-bordered imagined window life cuts to the blue real seated pair, with his right open palm directed at the retreating display. This is a clear imagined-to-present transition and intentional pose/location discontinuity, not a continuous standing-to-seated action. Screen-left/right identities remain coherent.'),
('C21','C22',348,3972,'Closer hand/torso framing follows the completed withdrawal. His right hand remains on his own knee; small framing/line-detail reset is readable as a cut, not a contact discontinuity.'),
('C22','C23',489,4113,'The open hand has returned to the knee before the wide gold-plane shot. His head changes from down to toward her in a deliberate wider editorial beat. The room and emotional separation remain consistent; not a seamless head-action match.'),
('C23','C24',657,4281,'A closer perspective resets pane angles before the foreground sweep. The pane arrangement jumps in an explicit shot cut; the two seated people, stable hands/props and same room continue. No claim of uninterrupted geometric rotation across the cut.'),
('C24','C25',825,4449,'The travelling multi-pane wide view cuts tighter to a single warm possibility behind her. Rigid people/table/cups remain coherent; modest framing and her eye-pose reset are retained as editorial elision.'),
('C25','C26',974,4598,'The remaining narrow gold sliver cuts away to his frightened blue-room close-up. His facing direction changes at the closer angle. The thought-space collapse reads as completed by the cut; no cure, new room or physical event is asserted. The C25 keeper itself has not reached a zero-width line.')]
cuts=[]
for a,b,local,master,note in notes:
 cuts.append({'from':a,'to':b,'local_cut_frame':local,'master_cut_frame':master,'verdict':'PASS_SCOPED_JOIN','observations':note,'exact_cut_evidence':ref(D/f'joined-cut-{local}-000.jpg'),'examined_local_frames':list(range(local-3,local+3))})
run=next(x for x in play['runs'] if x['shot']=='C20-C26')
write(P/'review/middle-C20-C26-unbound-v1-joined-review.json',{'schema':'jml-independent-joined-review/v1','reviewer':'c_final_middle_review','reviewed_at_utc':now,'verdict':'PASS_SCOPED_JOINS_WITH_C22_LITERAL_ACTION_RECONCILIATION','artifact':ref(joined),'diagnostic_metadata':ref(P/'exports/C20_C26_Middle_C_Unbound_Diagnostic_v1.json'),'master_range':[3624,4728],'frames':1104,'fps':24,'duration_seconds':46,'source_review':ref(source_review),'cuts':cuts,'sequence_read':'The gold imagined winter leads back to his care directed at the real woman; his helpless self-contained hand gesture gives way to seasonal possibilities closing around the same unavailable pair, then to the frightened close-up. The physical room and emotional impasse survive the motion and cuts. C22 actual gesture requires root reconciliation, not relabelling as the absent fist.','playback':ref(D/'playback-unmuted-v1.json'),'playback_telemetry':run['telemetry'],'evidence_manifest':ref(D/'evidence-manifest-v1.json'),'limits':limits})
