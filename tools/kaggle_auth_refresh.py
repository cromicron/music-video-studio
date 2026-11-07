#!/usr/bin/env python3
"""Refresh existing Kaggle OAuth through its SDK without displaying credentials.

Run with the prepared Kaggle CLI Python before long unattended provider work.
The installed SDK's expiry predicate waits until 30 minutes after expiration;
this entrypoint refreshes five minutes early instead, using its public method.
"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from kagglesdk.kaggle_client import KaggleClient
from kagglesdk.kaggle_creds import KaggleCredentials


def main():
    path = Path(KaggleCredentials.DEFAULT_CREDENTIALS_FILE).expanduser()
    data = json.loads(path.read_text())
    raw_expiry = data.get("access_token_expiration")
    expiry = datetime.fromisoformat(raw_expiry) if raw_expiry else None
    if expiry is not None and expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    refresh = (not data.get("access_token") or expiry is None
               or expiry <= datetime.now(timezone.utc) + timedelta(minutes=5))
    del data
    if refresh:
        with KaggleClient() as client:
            credentials = KaggleCredentials.load(client)
            if credentials is None:
                raise RuntimeError("Existing OAuth credentials unavailable")
            credentials.refresh_access_token()
        expiry = datetime.fromisoformat(json.loads(path.read_text())["access_token_expiration"])
    print(json.dumps({"refreshed": refresh, "valid_until_utc": expiry.isoformat(),
                      "credential_values_displayed": False}))


if __name__ == "__main__":
    main()
