#!/usr/bin/env python3
"""Generate one anonymous LTX-2.5 demo clip, or resume its saved event.

No credentials, sign-in, billing, identity rotation or automatic retries. A job
directory is a submission boundary: once submitted, subsequent calls resume the
same event. A failed/quota-limited event remains failed; it is not resubmitted.
"""
import argparse
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import uuid

HOST = "https://lightricks-ltx-2-5.hf.space"


def request_json(path, data, content_type="application/json"):
    request = urllib.request.Request(HOST + path, data=data,
                                     headers={"Content-Type": content_type})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def generate(image, prompt, output, width=896, height=512, duration=5.0, seed=49):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    submission = output / "submission.json"
    result = output / "result.json"
    destination = output / "output.mp4"
    if result.exists() and destination.exists():
        print(destination)
        return
    if not submission.exists():
        if width % 64 or height % 64 or not 1 <= duration <= 5:
            raise ValueError("Dimensions must be divisible by 64; duration must be 1–5s")
        image = Path(image)
        boundary = "----JML" + uuid.uuid4().hex
        mime = "image/png" if image.suffix.lower() == ".png" else "image/jpeg"
        body = (f'--{boundary}\r\nContent-Disposition: form-data; name="files"; '
                f'filename="reference{image.suffix}"\r\nContent-Type: {mime}\r\n\r\n').encode()
        body += image.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        uploaded = request_json("/gradio_api/upload", body,
                                "multipart/form-data; boundary=" + boundary)
        arguments = {
            "prompt": prompt,
            "image_path": {"path": uploaded[0], "meta": {"_type": "gradio.FileData"}},
            "height": height, "width": width, "duration_s": duration,
            "seed": seed, "decoder": "conv", "auto_len": False,
            "randomize_seed": False, "do_enhance": False,
        }
        (output / "request.json").write_text(json.dumps(arguments, indent=2))
        # Persist the response before polling. Never blindly retry a timed-out submit.
        pending = output / "submit_started.txt"
        if pending.exists():
            raise RuntimeError("An earlier submission outcome is unknown; inspect it before retrying")
        pending.write_text("A single submission started; no automatic retries.\n")
        job = request_json("/gradio_api/call/v2/run", json.dumps(arguments).encode())
        submission.write_text(json.dumps(job, indent=2))
    else:
        job = json.loads(submission.read_text())
    event_url = HOST + "/gradio_api/call/run/" + job["event_id"]
    print("Awaiting saved event", job["event_id"], flush=True)
    event_type = ""
    completed = None
    with urllib.request.urlopen(event_url, timeout=55) as stream:
        with (output / "events.txt").open("a") as log:
            for raw in stream:
                line = raw.decode()
                log.write(line)
                log.flush()
                if line.startswith("event:"):
                    event_type = line[6:].strip()
                elif line.startswith("data:") and event_type == "error":
                    raise RuntimeError("Generation stopped: " + line[5:].strip())
                elif line.startswith("data:") and event_type == "complete":
                    completed = json.loads(line[5:].strip())
                    break
    if not completed:
        raise RuntimeError("No completion received; resume this same directory/event later")
    result.write_text(json.dumps(completed, indent=2))
    url = completed[0]["url"]
    if urllib.parse.urlsplit(url).netloc != urllib.parse.urlsplit(HOST).netloc:
        raise RuntimeError("Unexpected output host; inspect result before download")
    with urllib.request.urlopen(url, timeout=45) as response:
        destination.write_bytes(response.read())
    print(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--width", type=int, default=896)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--seed", type=int, default=49)
    args = parser.parse_args()
    generate(args.image, Path(args.prompt_file).read_text(), args.output,
             args.width, args.height, args.duration, args.seed)
