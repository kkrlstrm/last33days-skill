"""Tests for the short-TTL on-disk fetch cache in lib.http.

The cache exists so the `--emit=html` shareable-brief flow's second pipeline
pass reuses the first pass's GET responses instead of re-fetching every source.
It is DISABLED unless LAST30DAYS_FETCH_CACHE_TTL is a positive integer, so these
tests set it explicitly; the default (unset) path is covered by asserting a
disabled cache never intercepts a request.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from lib import http


def _mock_response(body: str = '{"ok": true}', status: int = 200):
    resp = MagicMock()
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    resp.read = MagicMock(return_value=body.encode("utf-8"))
    resp.status = status
    return resp


class FetchCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._env = patch.dict(
            os.environ,
            {
                "LAST30DAYS_FETCH_CACHE_TTL": "900",
                "LAST30DAYS_FETCH_CACHE_DIR": self._tmp.name,
            },
            clear=False,
        )
        self._env.start()

    def tearDown(self) -> None:
        self._env.stop()
        self._tmp.cleanup()

    @patch("lib.http.urllib.request.urlopen")
    def test_get_is_cached_second_call_skips_network(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response('{"v": 1}')
        first = http.get("https://api.example.com/data")
        second = http.get("https://api.example.com/data")
        self.assertEqual({"v": 1}, first)
        self.assertEqual({"v": 1}, second)
        # Only the first call hit the network; the second was served from cache.
        self.assertEqual(1, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_distinct_urls_do_not_share_cache(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response()
        http.get("https://api.example.com/a")
        http.get("https://api.example.com/b")
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_raw_and_parsed_do_not_collide(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response('{"v": 2}')
        parsed = http.get("https://api.example.com/data")
        raw = http.request("GET", "https://api.example.com/data", raw=True)
        self.assertEqual({"v": 2}, parsed)
        self.assertEqual('{"v": 2}', raw)
        # Different return shapes are keyed separately, so both hit the network.
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_post_is_never_cached(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response()
        http.post("https://api.example.com/data", json_data={"q": "x"})
        http.post("https://api.example.com/data", json_data={"q": "x"})
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_disabled_when_ttl_unset(self, mock_urlopen):
        mock_urlopen.side_effect = [_mock_response('{"v": 1}'), _mock_response('{"v": 2}')]
        with patch.dict(os.environ, {}, clear=False):
            del os.environ["LAST30DAYS_FETCH_CACHE_TTL"]
            http.get("https://api.example.com/data")
            http.get("https://api.example.com/data")
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_kill_switch_disables_cache(self, mock_urlopen):
        mock_urlopen.side_effect = [_mock_response('{"v": 1}'), _mock_response('{"v": 2}')]
        with patch.dict(os.environ, {"LAST30DAYS_FETCH_CACHE": "0"}, clear=False):
            http.get("https://api.example.com/data")
            http.get("https://api.example.com/data")
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_expired_entry_refetches(self, mock_urlopen):
        mock_urlopen.side_effect = [_mock_response('{"v": 1}'), _mock_response('{"v": 2}')]
        with patch.dict(os.environ, {"LAST30DAYS_FETCH_CACHE_TTL": "1"}, clear=False):
            http.get("https://api.example.com/data")
            # Age the cache file well beyond the 1s TTL.
            with patch("lib.http.time.time", return_value=http.time.time() + 10):
                result = http.get("https://api.example.com/data")
        self.assertEqual({"v": 2}, result)
        self.assertEqual(2, mock_urlopen.call_count)

    @patch("lib.http.urllib.request.urlopen")
    def test_error_responses_are_not_cached(self, mock_urlopen):
        import urllib.error

        err = urllib.error.HTTPError("https://api.example.com/data", 500, "err", {}, None)
        ok = _mock_response('{"v": 9}')
        # First call errors out; a later call must re-hit the network and succeed.
        mock_urlopen.side_effect = [err, err, err, err, err, ok]
        with patch("lib.http.time.sleep"):
            with self.assertRaises(http.HTTPError):
                http.get("https://api.example.com/data", retries=5)
            result = http.get("https://api.example.com/data")
        self.assertEqual({"v": 9}, result)

    def test_cache_key_excludes_auth_headers(self):
        # The key is a function of method+url+raw only, so rotating auth tokens
        # neither fragment the cache nor leak into the on-disk key.
        k1 = http._fetch_cache_key("GET", "https://api.example.com/data", False)
        k2 = http._fetch_cache_key("GET", "https://api.example.com/data", False)
        self.assertEqual(k1, k2)
        self.assertNotEqual(
            k1, http._fetch_cache_key("GET", "https://api.example.com/other", False)
        )

    @patch("lib.http.urllib.request.urlopen")
    def test_url_query_credentials_do_not_fragment_cache(self, mock_urlopen):
        # A rotating api_key in the query string must not cause a cache miss:
        # the key is derived from the credential-masked safe_url, so the second
        # request (different key, same logical URL) is served from cache.
        mock_urlopen.return_value = _mock_response('{"v": 1}')
        http.get("https://api.example.com/s?q=x&api_key=AAA")
        result = http.get("https://api.example.com/s?q=x&api_key=BBB")
        self.assertEqual({"v": 1}, result)
        self.assertEqual(1, mock_urlopen.call_count)

    def test_default_cache_dir_is_user_specific(self):
        # The default temp dir carries the uid/username so it can't collide with
        # another user's dir on a shared host.
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("LAST30DAYS_FETCH_CACHE_DIR", None)
            name = http._fetch_cache_dir().name
        self.assertTrue(name.startswith("last30days-fetch-cache-"))
        self.assertNotEqual(name, "last30days-fetch-cache-")


if __name__ == "__main__":
    unittest.main()
