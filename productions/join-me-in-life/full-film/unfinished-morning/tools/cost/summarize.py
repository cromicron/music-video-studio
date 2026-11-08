#!/usr/bin/env python3
"""Read local C completion evidence and bindings; emit JSON or Markdown, never write inputs."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys


class EvidenceError(ValueError):
    """An incomplete, ambiguous or inconsistent record cannot support a total."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def positive(value, label):
    require(type(value) in (int, float) and math.isfinite(value) and value > 0,
            f'{label}: expected finite positive number')
    return value


def digest(value, label):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value),
            f'{label}: invalid SHA-256')
    return value


def summarize(root):
    root = Path(root).resolve()
    inputs = {}

    def read(path):
        path = path.resolve()
        raw = path.read_bytes()
        inputs[str(path.relative_to(root))] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw, object_pairs_hook=no_duplicate_keys)

    plan = read(root / 'story/shot-plan-v1.json')
    bindings = read(root / 'tools/editor/motion-bindings.json')
    require(plan['fps'] == 24 and bindings['schema'] == 'jml-c-motion-bindings/v1',
            'unsupported story/binding format')
    shots = {s['id']: s for s in plan['shots']}
    require(len(shots) == len(plan['shots']) == plan['shot_count'], 'duplicate/missing planned shots')
    require(sum(s['planned_generation']['editorial_frames'] for s in shots.values()) == plan['total_frames'],
            'planned picture total differs')
    pointer = read(root / 'tools/editor/current-edit.json')
    require(pointer['schema'] == 'jml-c-current-edit/v1', 'unsupported current-edit pointer')
    edit_path = Path(pointer['edit'])
    if not edit_path.is_absolute():
        edit_path = root.parents[3] / edit_path  # Stored paths are relative to the studio repository.
    require(sha(edit_path) == digest(pointer['sha256'], 'current edit'), 'current edit bytes changed')
    edit = read(edit_path)
    require(edit['fps'] == plan['fps'] and edit['total_frames'] == plan['total_frames'],
            'current edit changes the film frame grid or duration')
    require([s['id'] for s in edit['shots']] == list(shots), 'current edit changes shot identity/order')
    editorial = {}
    cursor = 0
    for shot in edit['shots']:
        first, last = shot['start_frame'], shot['end_frame_exclusive']
        require(type(first) is int and type(last) is int and first == cursor < last,
                f"{shot['id']}: noncontiguous or invalid current editorial timing")
        editorial[shot['id']] = shot
        cursor = last
    require(cursor == plan['total_frames'], 'current edit is not a complete picture timeline')
    require(set(pointer['bound_shots']) == set(bindings['shot_sources']),
            'current edit pointer and binding ledger disagree; wait for coherent adoption')
    deployments = [read(p) for p in sorted((root / 'research').glob('*-deployment.json'))]
    package_locks = {d.get('package_lock_sha256') for d in deployments}
    jobs_by_hash = defaultdict(list)
    for path in sorted((root / 'assets/motion').glob('*/job.json')):
        jobs_by_hash[sha(path)].append(path)
    records = sorted((root / 'research').glob('*-output-verification.json'))
    require(records, 'no completed output-verification records')
    seen_jobs, seen_pairs = set(), set()
    batches, generated = [], []
    for path in records:
        report = read(path)
        require(report['schema'] in ('jml-v2-downloaded-batch-verification/v1',
                                    'jml-v2-a2v-downloaded-verification/v1'), f'{path.name}: unsupported schema')
        kind = 'performance' if 'a2v' in report['schema'] else 'narrative'
        lock = digest(report['package_lock_sha256'], path.name)
        job_hash = digest(report['job_record_sha256'], path.name)
        pair = (lock, job_hash)
        require(pair not in seen_pairs and job_hash not in seen_jobs,
                f'{path.name}: duplicate completion record for actual package/job; remove report alias, not the job')
        seen_pairs.add(pair)
        seen_jobs.add(job_hash)
        require(lock in package_locks, f'{path.name}: package lock lacks local deployment evidence')
        matches = jobs_by_hash[job_hash]
        require(len(matches) == 1, f'{path.name}: actual job bytes missing or ambiguous')
        job_path = matches[0]
        job = read(job_path)
        status = report.get('provider_job_status', report.get('job_status'))
        require(status == job['status'] == 'bounded_job_complete', f'{path.name}: job is not complete')
        seconds = positive(report['whole_job_seconds'], path.name)
        require(math.isclose(seconds, positive(job['elapsed_seconds'], 'job elapsed'), abs_tol=1e-6),
                f'{path.name}: elapsed time differs from actual job')
        require(report['all_takes_technically_verified'] is True and report['takes'],
                f'{path.name}: not all takes technically verified')
        ids = [t.get('take_id', t.get('shot_id')) for t in report['takes']]
        require(len(set(ids)) == len(ids) and ids == [s['shot_id'] for s in job['shots']],
                f'{path.name}: duplicate, missing or reordered takes')
        require(all(s['status'] == 'child_complete_unreviewed' and s['attempts'] == 1 for s in job['shots']),
                f'{path.name}: unaccounted child attempts or incomplete child')
        frames = 0
        for sid, take in zip(ids, report['takes']):
            require(sid in shots, f'{path.name}: unknown shot {sid}')
            expected_method = 'original_song_A2V' if kind == 'performance' else 'reviewed_endpoints_I2V'
            require(shots[sid]['planned_generation']['method'] == expected_method, f'{sid}: method mismatch')
            n = take['frames']
            require(type(n) is int and n > 0 and take['fps'] == 24, f'{sid}: invalid frame count/fps')
            require(take['technical_verification'] == 'pass' and take['full_decode_passed'] is True,
                    f'{sid}: missing technical pass')
            render_path = job_path.parent / sid / 'render.json'
            video_path = job_path.parent / sid / 'video-silent.mp4'
            render = read(render_path)
            require(sha(render_path) == digest(take['render_sha256'], sid), f'{sid}: render bytes changed')
            require(render['manifest']['frames'] == n and render['manifest']['fps'] == 24,
                    f'{sid}: reported frames differ from actual render manifest')
            video_hash = digest(take['video_sha256'], sid)
            require(sha(video_path) == video_hash, f'{sid}: video bytes changed')
            require(render['status'] == 'complete' and render['technical_valid'] is True, f'{sid}: render incomplete')
            generation = positive(take['generation_seconds'], sid + ' generation')
            child = positive(take['child_seconds'], sid + ' child')
            require(generation <= child <= seconds, f'{sid}: inconsistent runtime hierarchy')
            require(math.isclose(generation, render['generation_seconds'], abs_tol=1e-6)
                    and math.isclose(child, render['elapsed_seconds'], abs_tol=1e-6), f'{sid}: render timing mismatch')
            generated.append({'shot': sid, 'kind': kind, 'video_sha256': video_hash,
                              'frames': n, 'batch': path.name, 'job_record_sha256': job_hash})
            frames += n
        batches.append({'record': str(path.relative_to(root)), 'package_lock_sha256': lock,
                        'job_record_sha256': job_hash, 'kind': kind, 'takes': len(ids),
                        'raw_frames': frames, 'whole_job_seconds': seconds})

    accepted, source_ids = [], set()
    generated_by_hash = defaultdict(list)
    for take in generated:
        generated_by_hash[take['video_sha256']].append(take)
    for sid, binding in sorted(bindings['shot_sources'].items()):
        require(sid in shots, f'bound unknown shot: {sid}')
        source_id = binding['id']
        source = bindings['sources'][source_id]
        review = source['review']
        require(source['kind'] == 'video' and review['status'] == 'accepted', f'{sid}: bound source is not accepted')
        # Source/review paths are relative to full-film, including the preserved ../current source.
        source_path = root.parent / source['path']
        review_path = root.parent / review['path']
        require(sha(source_path) == digest(source['sha256'], sid), f'{sid}: bound source bytes changed')
        require(sha(review_path) == digest(review['sha256'], sid), f'{sid}: review bytes changed')
        first, last = binding['in_frame'], binding['out_frame_exclusive']
        require(type(first) is int and type(last) is int and 0 <= first < last,
                f'{sid}: malformed bound range')
        current = editorial[sid]
        require(current.get('source') == binding, f'{sid}: current edit has not adopted this binding')
        require(last - first == current['end_frame_exclusive'] - current['start_frame'],
                f'{sid}: bound duration differs from adopted current edit')
        require(any(a <= first < last <= b for a, b in review['accepted_ranges']), f'{sid}: range not reviewed')
        existing = shots[sid]['planned_generation']['method'] == 'existing_reviewed_motion_candidate'
        matches = generated_by_hash[source['sha256']]
        if not existing:
            require(matches and all(t['shot'] == sid and last <= t['frames'] for t in matches),
                    f'{sid}: accepted new source lacks exact completed take evidence')
        source_ids.add(source_id)
        accepted.append({'shot': sid, 'source_id': source_id, 'existing': existing,
                         'retained_frames': last - first, 'video_sha256': source['sha256']})

    by_kind = {}
    forecast_initial_seconds = 0
    for kind, method in [('narrative', 'reviewed_endpoints_I2V'), ('performance', 'original_song_A2V')]:
        group = [b for b in batches if b['kind'] == kind]
        seconds = sum(b['whole_job_seconds'] for b in group)
        frames = sum(b['raw_frames'] for b in group)
        planned = sum(s['planned_generation']['model_frames_8n_plus_1'] for s in shots.values()
                      if s['planned_generation']['method'] == method)
        require(frames > 0, f'no measured {kind} work; cannot forecast that method')
        forecast_initial_seconds += planned * seconds / frames
        by_kind[kind] = {'completed_jobs': len(group), 'generated_takes': sum(b['takes'] for b in group),
                         'raw_frames': frames, 'raw_seconds': frames / 24,
                         'whole_job_seconds': seconds, 'wall_seconds_per_generated_second': seconds / (frames / 24),
                         'planned_initial_raw_frames': planned}
    completed_seconds = sum(b['whole_job_seconds'] for b in batches)
    accepted_new = {a['video_sha256'] for a in accepted if not a['existing']}
    unbound = sorted(set(shots) - {a['shot'] for a in accepted})
    account_observation = None
    capacity_path = root / 'research/post-all-planned-jobs-capacity-v1.json'
    if capacity_path.exists():
        capacity = read(capacity_path)
        account_observation = {
            'evidence': str(capacity_path.relative_to(root)), 'observed_utc': capacity['observed_utc'],
            'gpu_remaining_hours': capacity['quota_gate']['gpu_remaining_hours'],
            'listed_active_jobs': len(capacity['active']),
            'scope': 'Separate official account-capacity snapshot, not the GPU hours charged to these jobs. Unreadable notebook statuses are not assumed active or inactive.',
        }
    scenarios = [
        {'name': name, 'takes_per_shot_multiplier': factor,
         'forecast_notebook_wall_hours': forecast_initial_seconds / 3600 * 10 * factor,
         'notional_30h_blocks_if_wall_hours_equal_quota_hours': math.ceil(forecast_initial_seconds / 3600 * 10 * factor / 30)}
        for name, factor in [('one_initial_take', 1), ('three_total_takes_plus_10_percent_pool', 3.3)]]
    if not unbound:
        scenarios.insert(0, {
            'name': 'repeat_this_observed_complete_source_process_ten_times',
            'forecast_notebook_wall_hours': completed_seconds / 3600 * 10,
            'notional_30h_blocks_if_wall_hours_equal_quota_hours': math.ceil(completed_seconds / 3600 * 10 / 30),
            'scope': 'Includes this film\'s actual generated rejected/unused takes. Repetition is a scenario, not a guaranteed future keeper rate, throughput or final-film approval.',
        })
    for relative, expected in inputs.items():
        require(sha(root / relative) == expected, f'input changed during read: {relative}; rerun')
    return {
        'schema': 'jml-c-measured-cost/v1', 'observed_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'INCOMPLETE_SOURCE_COVERAGE' if unbound else 'ALL_SOURCES_BOUND_FINAL_FILM_NOT_VERIFIED_HERE',
        'scope': 'Only exact locally verified completed C jobs. Running jobs, failed/pre-verification sessions, earlier concept tests, image/browser work, editing and review time are outside this measured subtotal.',
        'completed_jobs': len(batches), 'generated_takes': len(generated),
        'completed_notebook_wall_seconds_sum': completed_seconds,
        'completed_notebook_wall_hours_sum': completed_seconds / 3600,
        'provider_billed_gpu_hours': None, 'project_attributable_quota_debit_hours': None,
        'account_capacity_observation': account_observation,
        'not_elapsed_calendar_time': 'Concurrent notebooks overlap. Whole-job timers include setup/download/CPU overhead and are not provider billing or account quota measurements.',
        'bindings': {'planned_shots': len(shots), 'accepted_bound_shots': len(accepted),
                     'accepted_distinct_source_ids': len(source_ids), 'accepted_distinct_new_video_sources': len(accepted_new),
                     'observed_adopted_new_sources_per_generated_take': len(accepted_new) / len(generated),
                     'selection_ratio_scope': 'Current chosen sources divided by generated takes, including rejected/unused attempts; not a future or cross-model keeper probability.',
                     'accepted_existing_shots': sum(a['existing'] for a in accepted),
                     'accepted_retained_frames': sum(a['retained_frames'] for a in accepted),
                     'accepted_performance_shots': sum(shots[a['shot']]['planned_generation']['method'] == 'original_song_A2V' for a in accepted),
                     'planned_performance_shots': sum(s['planned_generation']['method'] == 'original_song_A2V' for s in shots.values()),
                     'unbound_shots': unbound, 'whole_film_acceptance_established_by_this_tool': False},
        'editorial_accounting': {
            'current_edit': str(edit_path.relative_to(root)), 'current_edit_sha256': pointer['sha256'],
            'raw_workload_basis': 'Frozen story/shot-plan-v1.json, unchanged by editorial range/timing selection.',
            'accepted_duration_basis': 'Hash-verified current edit with exact binding agreement and contiguous complete timeline.',
            'changed_editorial_durations': {
                sid: {'generation_plan_keeper_frames': shots[sid]['planned_generation']['editorial_frames'],
                      'adopted_edit_frames': editorial[sid]['end_frame_exclusive'] - editorial[sid]['start_frame']}
                for sid in shots if shots[sid]['planned_generation']['editorial_frames'] !=
                editorial[sid]['end_frame_exclusive'] - editorial[sid]['start_frame']},
            'additional_generation_inferred_from_edit_changes': False},
        'batches': batches, 'by_method': by_kind, 'accepted_bindings': accepted,
        'ten_film_scenarios': scenarios,
        'forecast_method': 'Scale each planned narrative/A2V raw frame by that method\'s measured completed-job wall-seconds per generated frame, then multiply by ten films and explicit attempt scenario. Fixed batch overhead is averaged over current batch sizes; no keeper-rate extrapolation.',
        'forecast_limits': 'Sensitivity only: no quota admission, future throughput, acceptance yield or calendar guarantee. The 30h blocks are not actual quota debit or weeks. Each future film needs its own accepted five-second existing source or extra free generation. No still/loop fallback.',
        'cost': {'paid_video_option_ten_complete_films_actual_checkout_cap_eur': 20,
                 'new_paid_video_provider_purchase_eur_recorded': 0,
                 'purchased_Runway_credits_consumed_for_selected_C': 0,
                 'purchase_fact_date': '2026-11-08',
                 'purchase_fact_source': 'Dated root report, not refreshed by this runtime tool; account billing is not audited.',
                 'existing_included_resources_incremental_cost_eur': 0,
                 'included_resource_rule': 'User explicitly counts already-paid subscriptions, included credits, machines and cloud accounts as zero additional cost. Existing included browser usage follows that rule; its underlying price is not audited.',
                 'separately_purchased_chat_credit_replenishment_cost_eur': None,
                 'chat_replenishment_in_paid_video_budget': False,
                 'total_personal_spending_eur': None,
                 'personal_spending_scope': 'Unpriced separate chat replenishment is disclosed outside the paid-video-tools budget; this tool makes no claim about total personal spending.',
                 'paid_option_purchase_or_quality_demonstrated': False,
                 'creative_tools': ['ChatGPT images', 'owned LTX', 'FFmpeg'],
                 'paid_price_report': 'research/paid-budget-c.md (preserved dated research, no new provider pricing calls)'},
        'input_sha256': inputs,
    }


def markdown(data):
    b = data['bindings']
    lines = ['# Unfinished Morning — measured runtime and cost supplement', '',
             f"Snapshot: {data['observed_utc']}. **{data['status']}**.", '',
             f"{data['completed_jobs']} verified completed notebooks generated {data['generated_takes']} takes in "
             f"**{data['completed_notebook_wall_hours_sum']:.6f} summed notebook wall-hours**. "
             f"The binding ledger accepts {b['accepted_bound_shots']}/{b['planned_shots']} shots: "
             f"{b['accepted_distinct_new_video_sources']} distinct new sources and {b['accepted_existing_shots']} existing source(s). "
             'This is scoped source acceptance, not final-film approval.', '', data['scope'], '',
             f"Current selection is {b['accepted_distinct_new_video_sources']}/{data['generated_takes']} generated takes "
             f"({100*b['observed_adopted_new_sources_per_generated_take']:.2f}%). " + b['selection_ratio_scope'], '',
             f"Current bindings include {b['accepted_performance_shots']}/{b['planned_performance_shots']} planned performance shots. "
             'Earlier failed takes remain charged to runtime even when repaired sources are now accepted; the earlier paid report is a dated snapshot.', '',
             'Raw workload comes from the frozen generation plan. Accepted keeper lengths come from the hash-verified adopted current edit; '
             'a reviewed redistribution of existing frames does not create another generated take or GPU charge.', '',
             data['not_elapsed_calendar_time'] + ' Billed GPU hours and project-specific quota debit are unknown.', '',
             '| Completed record | Takes | Raw frames | Notebook wall-hours |', '|---|---:|---:|---:|']
    for row in data['batches']:
        lines.append(f"| {Path(row['record']).name} | {row['takes']} | {row['raw_frames']} | {row['whole_job_seconds']/3600:.6f} |")
    if data['account_capacity_observation']:
        capacity = data['account_capacity_observation']
        lines += ['', f"Separate account snapshot at {capacity['observed_utc']}: {capacity['gpu_remaining_hours']:.2f} free GPU hours remaining, "
                  f"{capacity['listed_active_jobs']} listed active jobs. " + capacity['scope']]
    lines += ['', '**Ten-film sensitivity from these completed records only:**', '', data['forecast_method'], '',
              '| Scenario | Forecast notebook wall-hours | Notional 30-hour blocks* |', '|---|---:|---:|']
    for row in data['ten_film_scenarios']:
        lines.append(f"| {row['name']} | {row['forecast_notebook_wall_hours']:.3f} | {row['notional_30h_blocks_if_wall_hours_equal_quota_hours']} |")
    lines += ['', '*Only if notebook wall-hours equalled provider quota hours, which this evidence does not establish. ' + data['forecast_limits'], '',
              '**The paid-video option has a hard actual checkout cap of €20 total across ten complete films.** '
              f"The dated root report of {data['cost']['purchase_fact_date']} records no new paid video-provider purchase and no purchased Runway credits consumed for selected C; this tool does not refresh account billing. "
              '**Already-paid subscriptions, included credits, machines and cloud accounts count as zero additional cost under the user’s rule.** '
              'Existing included TinyFish browser usage follows that rule; its underlying price is not audited. '
              'Separately purchased chat-credit replenishment is unpriced and excluded from the paid-video-tools budget. '
              'It prevents a claim about total personal spending, without changing the scope of the €20 paid-video cap. '
              'The three creative tools remain ChatGPT images, owned LTX and FFmpeg, plus the retained original summer source.', '',
              'The dated [paid recommendation](paid-budget-c.md) remains unchanged. Its prices and conditional upgrade are research, not purchases or demonstrated improvement.', '',
              'Rerun from the repository root after all outputs and bindings are verified; choose a fresh version for saved snapshots:', '',
              '```sh',
              'python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format json',
              'python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format markdown',
              '```', '',
              'Both commands only read local evidence and print to stdout. Duplicate actual package/job identities, malformed completion data, '
              'changed hashes or accepted sources without exact completion evidence cause a nonzero exit rather than a plausible total. '
              'Running or queued jobs never count as completed. Distinct executions of the same package count separately.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = parser.parse_args()
    try:
        data = summarize(args.root)
    except (EvidenceError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f'Evidence rejected: {error}', file=sys.stderr)
        return 2
    print(json.dumps(data, indent=2, allow_nan=False) if args.format == 'json' else markdown(data), end='\n' if args.format == 'json' else '')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
