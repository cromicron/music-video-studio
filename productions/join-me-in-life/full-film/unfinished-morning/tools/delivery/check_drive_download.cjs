#!/usr/bin/env node
'use strict';
/** Verify a private Drive download using an already authorized, isolated CDP session.
 * Provider session creation/cancellation is deliberately outside this script.
 * No cookie extraction, sign-in changes, file upload, or playback claims.
 */
const fs = require('node:fs');
const path = require('node:path');

const HELP = `Usage: node check_drive_download.cjs --cdp ws://127.0.0.1:8878 \\
  --file-id DRIVE_FILE_ID --expected-bytes INTEGER --output evidence.json
Options:
  --timeout-ms INTEGER   Download completion deadline (default 30000, max 60000).
  --playwright PATH      Optional installed Playwright module path.
  --help                 Show this help without connecting.

Requires an isolated, already signed-in reviewer session and the existing
proxy-preserving tinyfish_cdp_bridge.py. CDP must be a loopback ws endpoint.
Success requires a completed download with matching byte counts and no observed
header contradictions. Missing headers are explicitly unverified. Output must
not already exist and is written exclusively to preserve earlier evidence.
This is not a content hash or subjective playback review. Close/cancel the exact
provider setup session separately afterward; CDP disconnect is not cleanup.
`;

function argumentsFrom(argv) {
  if (argv.includes('--help')) return null;
  const permitted = new Set(['cdp', 'file-id', 'expected-bytes', 'output', 'timeout-ms', 'playwright']);
  const args = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i].replace(/^--/, '');
    if (!argv[i].startsWith('--') || !permitted.has(key) || !argv[i + 1] || args[key] !== undefined) {
      throw new Error('Unknown, duplicate, or incomplete argument. Use --help.');
    }
    args[key] = argv[i + 1];
  }
  let cdp;
  try { cdp = new URL(args.cdp); } catch { throw new Error('A loopback --cdp URL is required.'); }
  if (cdp.protocol !== 'ws:' || !['127.0.0.1', 'localhost', '[::1]'].includes(cdp.hostname)
      || cdp.username || cdp.password || cdp.search || cdp.hash || cdp.pathname !== '/') {
    throw new Error('--cdp must be a plain loopback ws endpoint without credentials, path, or query.');
  }
  if (!/^[A-Za-z0-9_-]{10,200}$/.test(args['file-id'] || '')) throw new Error('A valid stable Drive --file-id is required.');
  const bytes = Number(args['expected-bytes']);
  if (!Number.isSafeInteger(bytes) || bytes <= 0) throw new Error('--expected-bytes must be a positive safe integer.');
  const timeout = Number(args['timeout-ms'] || 30000);
  if (!Number.isSafeInteger(timeout) || timeout < 1000 || timeout > 60000) throw new Error('--timeout-ms must be 1000–60000.');
  if (!args.output || path.extname(args.output) !== '.json') throw new Error('--output must name a JSON file.');
  try {
    fs.lstatSync(args.output);
  } catch (error) {
    if (error.code === 'ENOENT') return { ...args, bytes, timeout };
    throw new Error('--output could not be checked; no browser connection attempted.');
  }
  throw new Error('--output already exists; choose a new evidence filename.');
}

function safeLocation(url) {
  try {
    const u = new URL(url);
    return ['drive.google.com', 'drive.usercontent.google.com'].includes(u.hostname)
      ? { host: u.hostname, path: u.pathname } : null;
  } catch { return null; }
}
function safeHeaders(headers) {
  return Object.fromEntries(Object.entries(headers || {}).filter(([name]) =>
    ['content-type', 'content-disposition', 'content-length'].includes(name.toLowerCase())));
}
function verifyHeaders(responses, expectedBytes) {
  // Redirects legitimately have different MIME/length. Judge only the download
  // endpoint's non-redirect responses; absence is not proof of correct headers.
  const finals = responses.filter(r => r.host === 'drive.usercontent.google.com'
    && r.path === '/download' && r.event !== 'redirect'
    && !(r.status >= 300 && r.status < 400));
  const values = name => finals.flatMap(r => Object.entries(r.headers || {})
    .filter(([key]) => key.toLowerCase() === name).map(([, value]) => String(value)));
  const check = (observed, predicate) => ({
    status: !observed.length ? 'unverified' : observed.every(predicate) ? 'pass' : 'fail',
    observed: [...new Set(observed)]
  });
  const checks = {
    http_200: check(finals.map(r => r.status), value => value === 200),
    video_mp4: check(values('content-type'), value => value.split(';')[0].trim().toLowerCase() === 'video/mp4'),
    content_length: check(values('content-length'), value => /^\d+$/.test(value.trim()) && Number(value) === expectedBytes),
    mp4_filename: check(values('content-disposition'), value => /filename\*?\s*=\s*(?:"[^"]*\.mp4"|[^;]*\.mp4)(?:\s*;|\s*$)/i.test(value))
  };
  const statuses = Object.values(checks).map(c => c.status);
  return { status: statuses.includes('fail') ? 'fail' : statuses.includes('unverified') ? 'unverified' : 'pass', checks };
}

function playwrightModule(explicit) {
  if (explicit) return require(path.resolve(explicit));
  try { return require('playwright'); }
  catch { return require('/workspace/.tools/browser/node_modules/playwright'); }
}

async function run(args) {
  const { chromium } = playwrightModule(args.playwright);
  const result = {
    schema: 'jml-private-drive-download/v1', observed_at: new Date().toISOString(),
    file_id: args['file-id'], expected_bytes: args.bytes,
    stable_url: `https://drive.google.com/uc?export=download&id=${args['file-id']}`,
    codecs: [], responses: [], downloads: [], verdict: 'incomplete',
    download_verification: 'incomplete', header_verification: { status: 'unverified' },
    limits: [
      'Download completion and expected byte count are not a content hash.',
      'Codec capability is not actual playback, listening, or creative acceptance.',
      'Results describe this reviewer browser, not the recipient browser.',
      'Provider session cleanup is separate and is not performed by this script.'
    ]
  };
  let browser, page, timer;
  try {
    browser = await chromium.connectOverCDP(args.cdp, { timeout: args.timeout });
    result.browser_version = browser.version();
    const context = browser.contexts()[0];
    if (!context) throw new Error('No existing browser context.');
    page = await context.newPage();
    result.codecs = await page.evaluate(() => [
      'video/mp4; codecs="avc1.640028"', 'video/mp4; codecs="avc1.42E01E"',
      'audio/mp4; codecs="mp4a.40.2"', 'video/webm; codecs="vp9"', 'audio/webm; codecs="opus"'
    ].map(mime => ({ mime, canPlayType: document.createElement('video').canPlayType(mime) })));
    const network = await context.newCDPSession(page);
    await network.send('Network.enable');
    const frameId = (await network.send('Page.getFrameTree')).frameTree.frame.id;
    const requests = new Map();
    network.on('Network.requestWillBeSent', event => {
      const location = safeLocation(event.request.url);
      if (location) requests.set(event.requestId, location);
      if (event.redirectResponse) {
        const from = safeLocation(event.redirectResponse.url);
        if (from) result.responses.push({ event: 'redirect', ...from,
          status: event.redirectResponse.status, headers: safeHeaders(event.redirectResponse.headers) });
      }
    });
    network.on('Network.responseReceived', event => {
      const location = safeLocation(event.response.url);
      if (location) result.responses.push({ event: 'response', ...location,
        status: event.response.status, mime_type: event.response.mimeType,
        headers: safeHeaders(event.response.headers) });
    });
    network.on('Network.responseReceivedExtraInfo', event => {
      const location = requests.get(event.requestId);
      if (location) result.responses.push({ event: 'extra_info', ...location,
        status: event.statusCode, headers: safeHeaders(event.headers) });
    });
    const browserCDP = await browser.newBrowserCDPSession();
    await browserCDP.send('Browser.setDownloadBehavior', {
      behavior: 'allow', downloadPath: `/tmp/jml-drive-review-${Date.now()}`, eventsEnabled: true
    });
    const guids = new Set();
    let finished;
    const completion = new Promise(resolve => { finished = resolve; });
    browserCDP.on('Browser.downloadWillBegin', event => {
      const location = safeLocation(event.url);
      if (!location || event.frameId !== frameId) return;
      guids.add(event.guid);
      result.downloads.push({ event: 'will_begin', guid: event.guid,
        suggested_filename: event.suggestedFilename, ...location });
    });
    browserCDP.on('Browser.downloadProgress', event => {
      if (!guids.has(event.guid)) return;
      result.downloads.push({ event: 'progress', guid: event.guid, state: event.state,
        received_bytes: event.receivedBytes, total_bytes: event.totalBytes });
      if (event.state === 'completed' || event.state === 'canceled') finished(event);
    });
    const timeout = new Promise(resolve => { timer = setTimeout(() => resolve(null), args.timeout); });
    try {
      await page.goto(result.stable_url, { waitUntil: 'domcontentloaded', timeout: args.timeout });
      result.navigation = 'document_loaded';
    } catch (error) {
      // Raw Playwright errors can include redirects or signed URLs. Never persist them.
      result.navigation = /Download is starting/.test(error.message)
        ? 'download_started' : 'navigation_did_not_complete';
    }
    const download = await Promise.race([completion, timeout]);
    if (!download) result.verdict = 'timeout';
    else if (download.state === 'canceled') result.verdict = 'canceled';
    else result.verdict = download.receivedBytes === args.bytes && download.totalBytes === args.bytes
      ? 'pass' : 'byte_count_mismatch';
  } catch (error) {
    result.verdict = 'error';
    result.error_type = error.name; // No arbitrary error message, endpoint, cookie, or token.
  } finally {
    clearTimeout(timer);
    if (page) await page.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
    result.download_verification = result.verdict;
    result.header_verification = verifyHeaders(result.responses, args.bytes);
    if (result.header_verification.status === 'fail' && result.verdict === 'pass') {
      result.verdict = 'header_mismatch';
    }
    fs.mkdirSync(path.dirname(path.resolve(args.output)), { recursive: true });
    // Exclusive creation protects prior evidence even if a file appeared after
    // argument validation while this browser check was running.
    fs.writeFileSync(args.output, `${JSON.stringify(result, null, 2)}\n`, { flag: 'wx' });
  }
  console.log(JSON.stringify({ verdict: result.verdict, download_verification: result.download_verification,
    header_verification: result.header_verification.status, expected_bytes: args.bytes, output: args.output }));
  return result.verdict === 'pass' ? 0 : 1;
}

if (require.main === module) {
  let args;
  try { args = argumentsFrom(process.argv.slice(2)); }
  catch (error) { console.error(error.message); process.exitCode = 2; }
  if (args === null) console.log(HELP);
  else if (args) run(args).then(code => { process.exitCode = code; }).catch(error => {
    console.error(`Verification could not finish (${error.name}); check setup without printing secrets.`);
    process.exitCode = 1;
  });
}
module.exports = { argumentsFrom, safeLocation, safeHeaders, verifyHeaders };
