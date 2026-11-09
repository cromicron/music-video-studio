from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent;P=D.parents[1];F=P.parent;R=Path('/workspace/music-video-studio')
def sha(p):return hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest()
def ref(p):
 p=Path(p);p=p if p.is_absolute() else P/p
 return {'file':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}
S=R/'build/performance-cut-final-v1/Join_Me_in_Life_Movie_and_Band.mp4';pb=json.loads((D/'playback-v1.json').read_text());prep=json.loads((D/'preparation-v1.json').read_text());edit=json.loads((P/'edit/edit-v009.json').read_text());tech=json.loads((P/'research/editor-full-master-v1-technical-verification.json').read_text());t=pb['telemetry']
expected='fabe33c576aaa0473e82c6ed755e884e3b6bc9103f392551138f6527099f2fdb'
assert pb['sha256']==expected==prep['master_sha256']==tech['master']['sha256']
assert sha(S)==expected and S.stat().st_size==196409309
assert pb['preloaded_bytes']==196409309 and t['ended'] and t['rate']==1 and not t['muted'] and t['volume']==1 and t['error'] is None
assert t['quality']=={'total':6667,'dropped':2,'corrupted':0} and [e['event'] for e in t['events']]==['ended']
assert '--mute-audio' not in pb['actual_browser_command_line']['arguments']
assert len(pb['captures'])==48 and len(edit['shots'])==46
assert tech['all_ordered_chunk_pictures_identical'] and tech['source_padding_frames']==0 and tech['reused_source_interval_frames']==0
# All26 decoded compact/native proof images and all12 actual browser overviews were manually inspected before this freeze.
viewed=[ref(D/n) for n in prep['proof_files']]+[ref(D/f'actual-playback-overview-{i:02}.jpg') for i in range(1,13)]
for c in pb['captures']:assert sha(c['file'])==c['sha256']
join_notes={
1:'Standing record-box organization to seated close-up is a deliberate time elision; not a continuous sit or unexplained body morph.',
3:'First move from intimate present to sole-cross keyboardist clearly establishes a performing world.',
4:'Return from stage to her counter-supported wiping continues the order/withdrawal motif rather than opening another world.',
5:'Supported cup ends on counter, then her composed face is countered by his concern; no implied spontaneous recovery.',
8:'Guitar close/wide to full five-person stage retains identities/placement; no cloned narrative redhead.',
11:'Handheld singer medium to physically clipped boom-supported close-up is an intentional performance cut, not a single continuous mic hand-off.',
12:'Tighter guitarist framing follows singer; the exact lossless crop keeps functional hands and removes the unrelated corner glyph.',
17:'Worried present face motivates the only remembered summer setting.',
18:'C15/C16 shared-earbud continuity is recognizable with the retained rounder C16 style exception.',
19:'C16 to brighter C17 intensifies the same private summer joy; no second memory or band duet.',
20:'C17 happy eye contact cuts hard to blue present nonresponse, preserving the central contrast.',
21:'C18 to disjoint C05 callback widens the same present; a brief practiced courtesy does not become an emotional reunion.',
22:'Callback returns to the actively articulating accepted B08B source; failed frozen-mouth B08A is absent.',
23:'Singer pullback reveals limited cymbal rims before the actual drummer shot; it does not establish an empty central kit.',
25:'A narrow warm light patch remains inside the same blue kitchen; no wished-for future location is introduced.',
27:'Unclaimed hand/frustrated self-check cuts to two-hand synth performance, not another actor entering the apartment.',
29:'Bass attention turns screen-right generally; no claim it turns toward the keyboardist.',
30:'Band pressure resolves into his recognition close-up; present identity/costume remains distinct from stage clothing.',
32:'Her composed glance to renewed small cup-ordering gesture reads as practiced withdrawal in this sequence; no medical conclusion follows from tidying alone.',
33:'Recognition/order cuts directly into the first full-force plea; his tearful frightened face carries the dramatic break.',
34:'First plea release to the second closer attack is an expressive music-video cut, not a seamless continuous camera match.',
35:'Second to third plea preserves the same frightened speaker/room with changed attack and framing.',
36:'Third release to fourth renewed plea remains intense and caring, not an aggressive new character or recovery beat.',
37:'Fourth plea gives way to an unresolved two-person quiet; no answer or cure is inserted.',
38:'C33/C34 small hand/posture reset is a disclosed time elision, not an exact action match.',
39:'Her self-clasp is her own connected hands, not a supportive touch from him.',
40:'A short late drummer passage keeps the music-video performance world alive without replacing the final emotional resolution.',
42:'Late guitar insert has restrained touches and listening attention rather than a broad strumming victory.',
43:'Absorbed guitar lift returns to the silent couple; no ambiguous third story location.',
44:'Her own small cup movement remains self-directed and unforced.',
45:'The tighter final shot preserves her own hand/cup geography and leaves room for tears and a tentative look; no sip/smile/embrace is required to close the scene.'}
cuts=[]
for i,(a,b) in enumerate(zip(edit['shots'],edit['shots'][1:]),1):
 k=b['start_frame'];cuts.append({'index':i,'left':a['id'],'right':b['id'],'master_frame':k,'seconds':k/24,'inspected_final_indices':[k-2,k-1,k,k+1],'status':'PASS_EDITORIAL_JOIN_WITH_DISCLOSED_SCOPE','observation':join_notes.get(i,'Intentional shot-scale or present/stage cut; identity, world, connected bodies and prop ownership remain understandable at the exact boundary.')})
world={}
for s in edit['shots']:world[s['world']]=world.get(s['world'],0)+s['end_frame_exclusive']-s['start_frame']
review={'schema':'jml-independent-full-film-review/v1','reviewer':'recut_vocal_review_r2','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_COMPLETE_FILM_WITH_DISCLOSED_LIMITATIONS',
 'scope':'Exact277.791667s Movie and Band master only: all45 exact final cut windows, complete1x original-song execution, actual shot captures, seven output-native repaired/critical frames and global story/band/emotional progression. Source motion is inherited only through pinned accepted ranges and independently verified assembly provenance. Root adoption/director review/user personal approval remain separate.',
 'candidate':ref(S),'manifest':ref(S.with_suffix('.manifest.json')),'edit':ref(P/'edit/edit-v009.json'),'editorial_plan':ref(P/'story/editorial-plan-v3.json'),'provider_plan':ref(P/'story/shot-plan-v1.json'),
 'technical_verification':ref(P/'research/editor-full-master-v1-technical-verification.json'),'frame_reference_index':ref(P/'research/editor-full-master-v1-technical-verification.frame-references.json'),
 'pictures':6667,'fps':24,'duration_seconds':6667/24,'shots':46,'world_frames':world,
 'source_and_review_chain':{'preparation':ref(D/'preparation-v1.json'),'exact_source_hashes_checked':43,'all_selected_gate_hashes_checked':True,'all_keepers_inside_accepted_ranges':True,'no_repeated_source_intervals':True,'technical_inheritance':'Editor verifies all6667 decoded master pictures match ordered strict rendered chunks,24fps/no insertion/padding/reused interval; full waveform alignment has zero lag. This is not a claim that scaled/lossy master pixels equal unscaled raw pixels.','source_ranges':[{'shot':s['id'],'master':[s['start_frame'],s['end_frame_exclusive']],'source':s['source']} for s in edit['shots']]},
 'all45cuts':cuts,
 'playback':{'record':ref(D/'playback-v1.json'),'launch_record':ref(D/'launch-v1.json'),'presented_frame_callbacks':ref(D/'presented-frame-callbacks-v1.json'),'telemetry':t,'full_file_preloaded_bytes':pb['preloaded_bytes'],'actual_launch_mute_audio_absent':True,'no_seeking_or_rate_changes':True,'actual_captures':48,'capture_montages':ref(D/'montage-v1.json'),'presentation_limit':'Completed one continuous1x pass with2/6667 presentation drops and0corrupted frames. Only ended event; no waiting/stall/error/seek/rate-change. Max observed callback media gap83.333ms. This is not a zero-drop claim; no source freeze/assembly gap is inferred from a presentation drop.','honest_limit':'Instrumented full-film execution plus inspected actual browser captures/exact decoded cut/native evidence. Not subjective human hearing, physical speaker-output certification, exact notes/phonemes, or a claim of human observation of every displayed native frame.'},
 'global_read':{
 'opening':'Her controlled lowering/squaring of ordinary record sleeves, then composed nonresponse and counter-supported mug wiping establish the frightening calm before he can reach her. His unanswered open palm and concern supply context; the film does not claim that ordinary tidying by itself diagnoses suicidal intent.',
 'movie_and_band':'The performing stage is established on keys before the first full-band refrain; all five identities/instruments return in coherent wide and individual views. Repeated visible playing, active accepted singer sources and the fixed supported-mic repair read as a band performing through the song. The apartment story remains the emotional thread. No held B05B/B08A raw or original uncropped B06 appears.',
 'cast_and_props':'Keyboardist remains the sole clearly cross-wearing band member, with supplied spiky hair/beard/leather outfit and silver keyboard. Lead remains Yaro/light stubble/round pendant, blonde female guitarist is distinct from redhead, tied dirty-blond bassist has four-string instrument, drummer has long dark hair. Guitar/bass/keyboard/drum contacts and supports inherit their dense accepted source checks and survive actual final framing. No new ghost actor, independent arm, unsupported microphone, extra prop or corner glyph was found.',
 'summer_contrast':'Only C15–C17 form the remembered Stupid Summer Songs interval: shared earbuds, wrong-word/private singing play and her joyful laughter. She is not a band duet singer. The hard return to her closed blue present is heart-tearing and clear without clinic, imagined future or extra memory locations.',
 'callback':'New C05_CALLBACK[118,218) occupies the second-chorus opening as a brief practiced courtesy returning toward withdrawal. It is disjoint from earlier C05_RETURN[6,118), not repeated footage; it does not reward his plea or imply recovery.',
 'recognition_and_pleas':'C26/C27/O03 build from his noticing to her small rehearsed/orderly gesture, then all four contiguous C29–C32 pleas remain intact at master[4989,5364). His changing attacks, tears and releases are desperate, hopeful and caring. No new band insert interrupts those four pleas; exact phoneme accuracy is not asserted.',
 'aftermath':'Two ordinary people remain in unresolved silence after the pleas. Late stage inserts let the musical performance breathe; the cropped guitarist grows restrained/listening rather than triumphant. Her self-clasp and cup movement stay her own actions, not forced rescue gestures.',
 'ending':'O04 keeps the final7.916667s on her: damp eyes become visible tears and she tentatively looks toward him. The actual final-tail browser capture and output-native frame6650 show sadness/possible connection without a smile, hug, clinic, promised safety or instant cure. Relief that emotion can surface coexists with uncertainty over whether it is grief or opening.'},
 'viewed_evidence':viewed,
 'retained_review_tools':[ref(D/n) for n in ['prepare.py','playback.py','run-playback-detached.py','montage.py']],
 'limitations':['Native896x512 sources are upscaled; wide faces/fine finger lines remain soft, especially some apartment wide views. This is not a guarantee of perfect anatomy at every pixel.','C16 retains the accepted rounder/blue-eyed summer stylization; recognizability holds, but style is not pixel-identical across C15–C17.','B06 is an intentional fixed lossless portrait crop: some hair crown is cropped, and the headstock/tuner tip can leave the right edge during the late lift. Both functional hands and facial features remain visible; no all-six-tuners-every-frame claim.','B09 side curtain/tassel/fabric and haze have generative texture movement. At actual viewing scale these remain background fabric/stage atmosphere, not an additional performer or independent limb.','Opening standing-to-seated change, singer medium-to-supported-mic close-up, four-plea reframings and C33/C34 hand reset are deliberate editorial elisions, not continuous single-camera action matches.','Full pass has2presentation drops/6667 and no stalls/errors/corruption; subjective listening/exact fingering/beat/phoneme synchronization remain unproven.'],
 'blocking_issues':[],
 'decision':'No additional generation, repeated frames, retiming, masking or source-range changes are required by this independent review of the exact master. Parent/root must separately adopt this review, director review and delivery checks.'}
output=P/'review/complete-film-independent-r2-review-v1.json';assert not output.exists();output.write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');print(json.dumps(ref(output)));print('world_frames',world)
