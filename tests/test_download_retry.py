import http.client
import io
import ssl

import pytest

from awesome_python_dev import downloads


@pytest.mark.parametrize("error", [http.client.IncompleteRead(b"partial"), ssl.SSLEOFError("network EOF")])
def test_transient_archive_read_failure_retries_with_checksum(tmp_path, monkeypatch, error):
    content = b"complete verified archive bytes"
    install = {"url": "https://codeload.github.com/owner/repo/tar.gz/commit", "sha256": downloads.digest(content)}
    calls = []

    class Response(io.BytesIO):
        url = install["url"]

        def read(self, size=-1):
            if len(calls) == 1:
                raise error
            return super().read(size)

    def open_response(*args, **kwargs):
        calls.append(True)
        return Response(content)

    monkeypatch.setattr(downloads.urllib.request, "urlopen", open_response)
    monkeypatch.setattr(downloads.time, "sleep", lambda _: None)
    assert downloads.download(install, tmp_path) == content
    assert len(calls) == 2
    assert (tmp_path / (install["sha256"] + ".tar.gz")).read_bytes() == content
