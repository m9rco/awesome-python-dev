The certificate and private key in this directory are public, test-only fixtures.
They identify `github.com` solely inside the local proxy regression test: the
CONNECT proxy routes that hostname to an in-process HTTPS test server and the
spawned test child trusts this certificate via its private `NODE_EXTRA_CA_CERTS`
environment. No system trust store or real GitHub connection is changed.

The key does not authenticate any real service. These fixtures are excluded from
the published npm package by the package's explicit `files` allowlist.
