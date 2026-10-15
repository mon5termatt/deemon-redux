import json
import logging
import time
from typing import Dict, Iterable, Optional, Set

import requests

logger = logging.getLogger(__name__)

AUTH_URL = "https://auth.deezer.com/login/arl"
PIPE_URL = "https://pipe.deezer.com/api"
# Refresh JWT slightly before the typical ~6 minute TTL
JWT_REFRESH_MARGIN_SECONDS = 60


class AiContentChecker:
    """Check Deezer Pipe GraphQL for album.hasIdentifiedAIContent."""

    def __init__(self, arl: str):
        self.arl = (arl or "").strip()
        self._jwt: Optional[str] = None
        self._jwt_expires_at: float = 0
        self._cache: Dict[str, bool] = {}
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "deemon"})

    def is_ready(self) -> bool:
        return len(self.arl) > 0

    def is_ai_album(self, album_id) -> Optional[bool]:
        """
        Return True if album is AI-tagged, False if not, None if unknown/error.
        """
        album_id = str(album_id)
        if album_id in self._cache:
            return self._cache[album_id]

        results = self.check_albums([album_id])
        if album_id not in results:
            return None
        return results[album_id]

    def check_albums(self, album_ids: Iterable) -> Dict[str, bool]:
        """
        Batch-check album IDs. Returns {album_id: hasIdentifiedAIContent}.
        IDs that fail to resolve are omitted.
        """
        ids = []
        pending = []
        for raw in album_ids:
            album_id = str(raw)
            if album_id in self._cache:
                continue
            if album_id not in ids:
                ids.append(album_id)
                pending.append(album_id)

        if pending:
            try:
                fetched = self._query_albums(pending)
                self._cache.update(fetched)
            except Exception as e:
                logger.error(f"Failed to check AI content flags: {e}")

        return {str(i): self._cache[str(i)] for i in album_ids if str(i) in self._cache}

    def ai_album_ids(self, album_ids: Iterable) -> Set[str]:
        checked = self.check_albums(album_ids)
        return {album_id for album_id, is_ai in checked.items() if is_ai}

    def _ensure_jwt(self):
        now = time.time()
        if self._jwt and now < (self._jwt_expires_at - JWT_REFRESH_MARGIN_SECONDS):
            return

        if not self.is_ready():
            raise RuntimeError("No ARL configured; cannot query AI content flags")

        self._session.cookies.set("arl", self.arl, domain="auth.deezer.com", path="/")
        response = self._session.post(
            AUTH_URL,
            params={"jo": "p", "rto": "c", "i": "c"},
            timeout=30,
        )
        response.raise_for_status()
        payload = json.loads(response.text)
        jwt = payload.get("jwt")
        if not jwt:
            raise RuntimeError("auth.deezer.com did not return a JWT")

        # Decode exp from JWT payload (middle segment); fall back to 5 minutes
        expires_at = now + 300
        try:
            import base64

            segment = jwt.split(".")[1]
            segment += "=" * (-len(segment) % 4)
            claims = json.loads(base64.urlsafe_b64decode(segment.encode("utf-8")))
            if isinstance(claims.get("exp"), (int, float)):
                expires_at = float(claims["exp"])
        except Exception:
            logger.debug("Unable to parse JWT expiry; using 5 minute fallback")

        self._jwt = jwt
        self._jwt_expires_at = expires_at
        logger.debug("Acquired Deezer Pipe JWT for AI content checks")

    def _query_albums(self, album_ids: list) -> Dict[str, bool]:
        self._ensure_jwt()

        # GraphQL aliases keep this to one request per batch
        selections = []
        variables = {}
        var_defs = []
        for index, album_id in enumerate(album_ids):
            var_name = f"id{index}"
            var_defs.append(f"${var_name}: String!")
            variables[var_name] = album_id
            selections.append(
                f"a{index}: album(albumId: ${var_name}) {{ id hasIdentifiedAIContent }}"
            )

        query = (
            "query AlbumAI("
            + ", ".join(var_defs)
            + ") {\n  "
            + "\n  ".join(selections)
            + "\n}"
        )

        response = self._session.post(
            PIPE_URL,
            headers={
                "content-type": "application/json",
                "accept": "application/json",
                "authorization": f"Bearer {self._jwt}",
            },
            json={"query": query, "variables": variables},
            timeout=30,
        )
        response.raise_for_status()
        body = response.json()

        if body.get("errors"):
            # Soft-fail individual albums when possible; hard-fail if nothing usable
            logger.debug(f"Pipe GraphQL errors while checking AI flags: {body['errors']}")

        data = body.get("data") or {}
        results = {}
        for index, album_id in enumerate(album_ids):
            node = data.get(f"a{index}")
            if not node:
                continue
            results[album_id] = bool(node.get("hasIdentifiedAIContent"))
        return results
