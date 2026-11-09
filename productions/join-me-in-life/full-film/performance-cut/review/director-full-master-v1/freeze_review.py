from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
root=next(p for p in D.parents if (p/'studio.json').exists())
P=root/'productions/join-me-in-life/full-film/performance-cut'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'file':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size}
index=json.loads((D/'evidence-index-v1.json').read_text());draft=json.loads((D/'findings-draft-v1.json').read_text())
playfile=D/'continuous-pass-v2/playback.json';play=json.loads(playfile.read_text());t=play['telemetry']
assert t['ended'] and t['rate']==1 and not t['muted'] and t['volume']==1 and t['error'] is None
assert t['quality']['corrupted']==0 and t['quality']['total']==6667
assert not [e for e in t['events'] if e['event'] in ['stalled','error']]
presentation_limited=bool(t['quality']['dropped']>6 or [e for e in t['events'] if e['event']=='waiting'])
assert play['browser_and_server_closed'] and play['compressed_input_fully_preloaded'] and play['loaded_blob_bytes']==196409309
assert play['actual_launch_mute_flag_present'] is False
master=root/'build/performance-cut-final-v1/Join_Me_in_Life_Movie_and_Band.mp4'
editfile=P/'edit/edit-v009.json'
assert sha(master)==play['source_sha256']=='fabe33c576aaa0473e82c6ed755e884e3b6bc9103f392551138f6527099f2fdb'
assert sha(editfile)==play['edit_sha256']=='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
edit=json.loads(editfile.read_text());technical=P/'research/editor-full-master-v1-technical-verification.json';tech=json.loads(technical.read_text())
assert tech['state']=='TECHNICAL_FULL_PASS_CREATIVE_REVIEW_SEPARATE'
assert tech['master']['sha256']==sha(master) and tech['edit']['sha256']==sha(editfile)
assert tech['frames']==6667 and tech['shots']==46 and tech['full_decode'] and tech['all_ordered_chunk_pictures_identical']
assert tech['source_padding_frames']==tech['reused_source_interval_frames']==0
assert tech['decoded_adjacent_equal_picture_frames']==[] and tech['decoded_picture_hash_frequency_max']==1
assert len(draft['join_reviews'])==45
expected=[(a['id'],b['id'],b['start_frame']) for a,b in zip(edit['shots'],edit['shots'][1:])]
assert expected==[(j['left'],j['right'],j['master_frame']) for j in draft['join_reviews']]
for group in ['joins','shots','native_targets']:
 for evidence in index[group]:assert sha(D/evidence['file'])==evidence['sha256']
refs={};bindings=[]
for s in edit['shots']:
 src=edit['sources'][s['source']['id']];r=src['review'];rp=P.parent/r['path']
 assert s['end_frame_exclusive']-s['start_frame']==s['source']['out_frame_exclusive']-s['source']['in_frame']
 assert any(a<=s['source']['in_frame']<s['source']['out_frame_exclusive']<=b for a,b in r['accepted_ranges'])
 assert sha(rp)==r['sha256']
 refs[r['path']]=ref(rp)
 bindings.append({'shot':s['id'],'global_range':[s['start_frame'],s['end_frame_exclusive']],'source_id':s['source']['id'],'source_file':src['path'],'source_sha256':src['sha256'],'source_range':[s['source']['in_frame'],s['source']['out_frame_exclusive']],'native_motion_gate':{'file':r['path'],'sha256':r['sha256']},'accepted_ranges':r['accepted_ranges']})
for name in ['story-context-review-v1.json','second-chorus-story-trial-review-v1.json']:
 p=P/'review'/name;refs[name]=ref(p)
all_evidence=[]
for glob in ['join-panel-*.jpg','overview-*.jpg','native-*.jpg']:
 all_evidence.extend(ref(p) for p in sorted(D.glob(glob)))
all_evidence.extend(ref(D/'continuous-pass-v2'/c['image']) for c in play['captures'])
review={
 'schema':'jml-performance-full-master-director-review/v1','review_id':'performance-cut-full-master-director-v1','reviewer':'independent recut_story_review_r2 director/story critic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':('PASS_CREATIVE_DIRECTOR_SCOPE_WITH_PLAYBACK_LIMITATION' if presentation_limited else 'PASS_FULL_MASTER_DIRECTOR_SCOPE'),'scope':'Actual assembled 46-shot, 6,667-frame master: all 45 joins, complete 1× original-song playback execution, chronological film/story/playing progression,13 targeted output-native frames and retained hash-bound native-motion/context source gates. Root acceptance and external delivery remain separate.',
 'master':ref(master),'source_edit':ref(editfile),'provider_plan':ref(P/'story/shot-plan-v1.json'),'editorial_plan':ref(P/'story/editorial-plan-v3.json'),
 'complete_original_song_playback':ref(playfile),'actual_unmuted_launch':ref(D/'continuous-pass-v2/launch-args.json'),'complete_playback_telemetry':t,'local_browser_smooth_playback_certified':not presentation_limited,
 'environment_interrupted_attempt_retained':ref(D/'attempt-01-environment-interrupted/interruption.json'),
 'playback_evidence_limits':'First attempt lost its controller during an environment update and is explicitly incomplete. Only the completed detached replay supplies the final ended/drops/stalls telemetry. Actual unmuted execution and encoded-audio verification are not subjective human hearing.',
 'technical_master_verification':ref(technical),'technical_result_referenced':{'all_6667_ordered_pictures':tech['all_ordered_chunk_pictures_identical'],'frames':tech['frames'],'natural_fps':tech['fps'],'padding_frames':tech['source_padding_frames'],'reused_source_interval_frames':tech['reused_source_interval_frames'],'identical_adjacent_frames':tech['decoded_adjacent_equal_picture_frames'],'unique_frame_hash_max':tech['decoded_picture_hash_frequency_max'],'full_decode':tech['full_decode'],'original_audio_waveform':tech['audio']['waveform']},
 'actual_evidence_index':ref(D/'evidence-index-v1.json'),'actually_viewed_compact_panels_overviews_native_and_playback_captures':all_evidence,
 'source_motion_gate_references_hash_verified':list(refs.values()),'exact_shot_bindings':bindings,
 'actual_playback_captures_visual_findings':{'30s':'Bearded keyboardist, sole clear cross, hands on keys.','125s':'Shared-earbud private summer joy, not a stage duet.','214s':'Second forceful private plea, open strained mouth and tears.','276s':'The actual capture around276.19s catches the previously reviewed brief blink at about O04 raw157. Head remains turned toward him; this is not a downcast return. Output-native final master frame6666, inspected separately, ends with eyes reopened toward him and tears still visible.'},'all45actual_cut_reviews':draft['join_reviews'],'global_directorial_findings':draft['global_directorial_findings'],'nonblocking_limits':draft['nonblocking_limits'],
 'blocking_findings':[],
 'recommendation':'Accept this exact master in the creative director/story scope; local presentation behavior remains disclosed and root must separately consider the independent complete playback result. Preserve its46 shot order, only one summer recollection, private recognition/allfour pleas, corrected playing sources and ambiguous tearful ending. No new render or provider generation requested by this review.',
 'presentation_gate':'LIMITED_NOT_CERTIFIED_SMOOTH' if presentation_limited else 'PASS','full_film_scope_reviewed':True,'full_film_director_gate_passed':True,'root_final_acceptance_separate':True,'external_delivery_approved_by_this_review':False
}
if t['quality']['dropped']:
 review['nonblocking_limits'].append(f"Complete replay recorded {t['quality']['dropped']} browser presentation drop(s) out of 6,667; {len([e for e in t['events'] if e['event']=='waiting'])} waiting event(s), zero stalled/error/corruption events. This is reported as presentation behavior, not hidden or confused with the independently verified encoded6667unique ordered frames.")
reviewfile=D/'full-master-director-review-v1.json';reviewfile.write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
text=['# Actual full-master director review','',f"PASS in creative director/story scope, with the local presentation limitation separately disclosed, for `{review['master']['sha256']}` and edit-v009 `{review['source_edit']['sha256']}`.",'',f"The detached complete original-song 1× replay ended after {t['wallSeconds']:.3f} s: 6,667 frames, {t['quality']['dropped']} browser presentation drops, zero corruption, stalls or errors and {len([e for e in t['events'] if e['event']=='waiting'])} waiting event(s). This local run is not certified smooth; root must separately assess the independent low-drop complete playback. Actual launch lacked the mute flag; video was unmuted at volume 1. The earlier environment-interrupted run is retained as incomplete. No subjective human-hearing or perfect lip-sync claim.",'']
for g in review['global_directorial_findings']:text.append(f"**{g['area']}.** {g['finding']}\n")
text+=['All 45 cuts were inspected as 9 compact actual-master boundary panels,46 shot midpoints in 4 chronological overviews, and13 targeted output-native frames. Every cut has a scoped finding in the JSON gate. Existing exact-hash native source gates and the separate all 6,667-frame encoded-master verification supply complementary movement/integrity evidence.','', '**Material limits.** B06 uses a tighter crop with clipped upper hair/headstock edge; B09 has peripheral curtain/reflection softness. Several kitchen and performance joins are visible angle/time ellipses, including standing-to-seated, handheld-to-stand microphone and the final unshown lap-to-cup lift. Fine source detail is generally upscaled. These do not block this exact edit.','', 'Root retains final acceptance, preservation and Drive delivery. This review requests no new generation or re-edit.','']
(D/'full-master-director-review-v1.md').write_text('\n'.join(text))
print(json.dumps({'review':str(reviewfile),'sha256':sha(reviewfile),'master_sha256':sha(master),'edit_sha256':sha(editfile),'joins':45,'status':review['status'],'telemetry':t},indent=2))
