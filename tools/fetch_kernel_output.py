"""E5b output fetch: list via direct API call, download files through the local proxy.

The API host (api.kaggle.com) only answers on a direct connection here, while the
file host (www.kaggleusercontent.com) is only reachable through the Clash proxy at
127.0.0.1:7890 — so the two phases need opposite network settings.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

OUT = Path.home() / "Desktop" / "hermes-output" / "arc3-eng" / "runs" / "e5b" / "out"
OUT.mkdir(parents=True, exist_ok=True)
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
WANTED = re.compile(r"(metrics|score)\.json$")
OWNER_SLUG = "zgyyyl/arc3-e5b-behavior"

LIST_CODE = r"""
import json, sys
from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.kernels.types.kernels_api_service import ApiListKernelSessionOutputRequest
api = KaggleApi(); api.authenticate()
files, token = [], None
for _ in range(40):
    with api.build_kaggle_client() as k:
        req = ApiListKernelSessionOutputRequest()
        req.user_name = "zgyyyl"; req.kernel_slug = "arc3-e5b-behavior"; req.page_size = 100
        if token: req.page_token = token
        resp = k.kernels.kernels_api_client.list_kernel_session_output(req)
        files += [[f.file_name, f.url] for f in (resp.files or [])]
        token = getattr(resp, "next_page_token", None)
    if not token: break
print(json.dumps(files))
"""


def list_files():
    env = {**os.environ, "NO_PROXY": "*", "no_proxy": "*"}
    for attempt in range(1, 9):
        try:
            r = subprocess.run([sys.executable, "-c", LIST_CODE], capture_output=True,
                               text=True, timeout=240, env=env)
            if r.returncode == 0 and r.stdout.strip().startswith("["):
                return json.loads(r.stdout)
            err = (r.stderr or "").strip().splitlines()[-1:] or [""]
            print(f"list attempt {attempt}: {err[0][:140]}")
        except subprocess.TimeoutExpired:
            print(f"list attempt {attempt}: timeout")
        time.sleep(20)
    return []


def download(url: str, dest: Path) -> bool:
    session = requests.Session()
    session.trust_env = False          # ignore NO_PROXY et al; use PROXY explicitly
    session.proxies.update(PROXY)
    for attempt in range(1, 5):
        try:
            r = session.get(url, timeout=180)
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            print(f"OK   {dest.name} {len(r.content)}B")
            return True
        except Exception as exc:                       # noqa: BLE001
            print(f"try {attempt} {dest.name}: {type(exc).__name__}: {str(exc)[:100]}")
            time.sleep(8 * attempt)
    return False


def main() -> None:
    files = list_files()
    if not files:
        print("NO FILE LIST")
        sys.exit(1)
    (OUT.parent / "e5b_urls.json").write_text(json.dumps(files), encoding="utf-8")
    targets = [(n, u) for n, u in files if WANTED.search(n) and "/" in n]
    print(f"listed {len(files)}; want {len(targets)}")
    for name, url in targets:
        dest = OUT / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {name}")
            continue
        download(url, dest)
    print("ALLDONE")


if __name__ == "__main__":
    main()
