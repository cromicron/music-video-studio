from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent;P=D.parents[1];R=Path('/workspace/music-video-studio')
def sha(p):return hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest()
def ref(p):
 p=Path(p);p=p if p.is_absolute() else R/p
 return {'file':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}
cfg=json.loads((D/'viewing-input-v1.json').read_text());pb=json.loads((D/'playback-v1.json').read_text());t=pb['telemetry'];technical=json.loads((R/cfg['technical_verification']['file']).read_text());native_path=P/'research/editor-final-viewing-v1-native-quality.json';native=json.loads(native_path.read_text());browser=P/'research/editor-final-viewing-v1-browser.json';master_review=R/cfg['master_review']['file']
expected='bf539e626629d1602eaf6fa03e546b448b56735519165f07a767668a537a700b';S=R/cfg['source']['file']
assert sha(S)==expected==pb['sha256']==cfg['source']['sha256'] and S.stat().st_size==89168823
assert pb['source_role']=='accepted_viewing_copy' and pb['configuration_sha256']==sha(D/'viewing-input-v1.json')
assert pb['preloaded_bytes']==89168823 and t['ended'] and t['rate']==1 and not t['muted'] and t['volume']==1 and t['error'] is None
assert t['quality']=={'total':6667,'dropped':0,'corrupted':0} and [e['event'] for e in t['events']]==['ended']
assert (t['width'],t['height'])==(1920,1080) and abs(t['currentTime']-6667/24)<.0001 and abs(t['wallSeconds']-6667/24)<1
assert '--mute-audio' not in pb['actual_browser_command_line']['arguments']
assert technical['cadence_and_zero_origins'] and technical['frames']==6667 and technical['fps']==24 and technical['audio_packets_and_timestamps_identical'] and technical['full_decode'] and technical['faststart_verified']
assert technical['viewing_copy']['sha256']==expected and technical['master']['sha256']==cfg['master']['sha256']
for key in ['edit','master_review','technical_verification']:
 item=cfg[key];assert ref(item['file'])['sha256']==item['sha256']
for item in cfg['additional_provenance']:assert ref(item['file'])['sha256']==item['sha256']
assert len(pb['captures'])==48 and len(native['pairs'])==14
for c in pb['captures']:assert sha(c['file'])==c['sha256']
for pair in native['pairs']:assert sha(R/pair['file'])==pair['sha256']
# MANUAL OBSERVATION completed before freeze: all12 actual48-capture overviews and all14 native paired images were actually viewed.
viewed=[ref(D/f'actual-playback-overview-{i:02}.jpg') for i in range(1,13)]
native_proofs=[{'label':x['label'],'master_frame':x['master_frame'],'native_crop_xywh':x['native_crop_xywh'],'proof':ref(x['file'])} for x in native['pairs']]
record={'schema':'jml-independent-viewing-copy-review/v1','reviewer':'recut_vocal_review_r2','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_COMPLETE_ACTUAL_VIEWING_COPY_WITH_DISCLOSED_SOURCE_LIMITATIONS','source_role':'accepted_viewing_copy',
 'scope':'Exact final compressed viewing MP4 complete original-song1x presentation and visual preservation. This is the delivery encoding, not another master pass. Master creative/source/all45cut acceptance is inherited from the separately frozen exact-master reviews/root acceptance; no source generation, reframing, retiming or new edit occurs here.',
 'viewing_copy':ref(S),'accepted_master':cfg['master'],'edit':cfg['edit'],'prior_independent_master_review':ref(master_review),'root_master_acceptance':ref(P/'review/final-acceptance-v1.json'),
 'encode_record':ref(P/'research/editor-final-viewing-v1-encode.json'),'derivative_technical':ref(R/cfg['technical_verification']['file']),'editor_native_quality':ref(native_path),'editor_nine_browser_samples':ref(browser),
 'derivative_provenance':{'pictures':6667,'fps':24,'width':1920,'height':1080,'duration_seconds':6667/24,'lossy_picture_encode':'H264 medium CRF22 capped video bitrate, faststart MP4; accepted master to viewing copy with no frame-count/cadence/origin change.','ssim_all':technical['ssim_all'],'audio_packets_and_timestamps_identical_to_master':True,'audio_packet_count':technical['audio_packet_count'],'full_decode_verified_by_editor':True,'all45_cuts_and_source_gate_chains':'Inherited only from exact accepted edit/master/derivative provenance; not freshly reapproved by screenshot sampling.'},
 'playback':{'record':ref(D/'playback-v1.json'),'configuration':ref(D/'viewing-input-v1.json'),'launch':ref(D/'launch-v1.json'),'presented_callbacks':ref(D/'presented-frame-callbacks-v1.json'),'telemetry':t,'actual_launch_mute_audio_absent':True,'full_file_preloaded_bytes':89168823,'capture_count':48,'capture_montages':ref(D/'montage-v1.json'),'assessment':'Complete uninterrupted277.791667s at1x/278.19wallseconds,6667total presentation frames,0dropped/0corrupted. Only ended event; no waiting/stall/error/seek/rate-change. The earlier director-master buffering result is preserved rather than rewritten; this separate run clears presentation of this exact delivered encoding under the tested local browser conditions.','callback_scope':'6663requestVideoFrameCallback records with max observed83.334ms media gap; browser presentation quality reports all6667frames with0drops. Callback cadence alone is not a promise of independently observing every displayed frame.'},
 'actual_visual_findings':[
 'All48 actual browser captures were inspected in12 retained overview sheets after the uninterrupted run. Story/band alternation, opening lowering/squaring and counter-supported cup action, only private summer memory, closed-present callback, all four pleas and the final look retain the accepted progression.',
 'All14 existing native master-left/viewing-right comparison sheets were independently inspected, including the corrected bass-plucking ROI: record hands, cloth/cup support, keyboard cross/contact, guitar pick/fret, bass pluck, drum/snare, lead mouth/mic, summer joy, recognition, plea tears and final face/hand/cup.',
 'Compression mildly smooths hair, lace/cloth, fine finger lines and dark stage texture. It preserves connected hand silhouettes, instrument/cup contact, clear sole keyboardist cross, supported microphone, mouth/teeth boundaries and intended eye direction. No new blocking block edge, ghost actor/limb, prop drift or frozen presentation was found.',
 'Summer remains visibly joyful and intimate; the return to blue present still hurts. The failed B08A performance is absent; the disjoint C05 callback and accepted active B08B remain in the correct roles.',
 'Recognition and all four pleas retain readable frightened eyes, tear tracks and changing performance emphasis. Final native frame6666 and actual final-tail capture retain her tears and tentative look toward him without a smile or recovery promise. Compression does not erase the emotional endpoint.',
 'Known native-source softness, C16 style variation, B06 tighter crop/headstock-edge exit and B09 tassel/fabric texture remain the accepted source limitations. This derivative review does not relabel them as flawless native detail or repair their source pixels.'
 ],
 'viewed_actual_browser_montages':viewed,'viewed_native_pairs':native_proofs,
 'retained_tools':[ref(D/n) for n in ['playback.py','run-playback-detached.py','montage.py']],
 'blocking_findings':[],
 'limits':['This local preloaded Chromium result is specific to the exact89,168,823-byte encoding and tested conditions; hosted Drive retrieval/download checks are separate root-owned evidence.','Instrumented unmuted playback and visual evidence do not establish subjective human hearing, physical speaker output, exact note/fingering/beat or phoneme synchronization.','Source-level softness/style/crop/fabric/elision limitations remain as frozen in the master review. No every-pixel anatomy perfection or viewing every native frame is claimed.'],
 'decision':'No additional encode, generation, loop, hold, retiming or source change is required by this independent final-viewing review. Root delivery adoption/checkpoint remains separate.'}
out=P/'review/final-viewing-independent-r2-review-v1.json';assert not out.exists();out.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n');print(json.dumps(ref(out)));print('evidence_bytes',sum(p.stat().st_size for p in D.rglob('*') if p.is_file()))
