"""Regression checks for published URLs and crawlable catalog content."""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://m9rco.github.io/awesome-python-dev"


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def builder():
    return load_script("build_site")


@pytest.fixture(scope="module")
def checker():
    return load_script("check_site")


@pytest.fixture
def site(tmp_path, builder):
    output = tmp_path / "site"
    builder.build_site(output, BASE_URL)
    return output


@pytest.mark.parametrize(
    "base_url",
    [BASE_URL, "https://example.org", "https://example.org/nested/toolkit/", "http://localhost:8000"],
)
def test_site_validates_for_project_and_custom_domains(tmp_path, builder, checker, base_url):
    output = tmp_path / "site"
    builder.build_site(output, base_url)
    assert checker.check_site(output, base_url) == []


def test_every_catalog_resource_and_profile_is_crawlable(site, checker):
    catalog = json.loads((ROOT / "src/awesome_python_dev/data/catalog.json").read_text(encoding="utf-8"))
    sitemap = ElementTree.parse(site / "sitemap.xml")
    urls = {node.text for node in sitemap.findall("{*}url/{*}loc")}
    for tool in catalog["tools"]:
        url = f"{BASE_URL}/tools/{tool['id']}/"
        assert url in urls
        source = (site / "tools" / tool["id"] / "index.html").read_text(encoding="utf-8")
        page = checker.Page(source)
        assert tool["name"] in "".join(page.text)
        assert page.canonicals == [url]
        if tool.get("install"):
            assert f"--tools {tool['id']}" in "".join(page.text)
        else:
            assert f"--tools {tool['id']}" not in "".join(page.text)
            assert "reference" in "".join(page.text).lower()
    for kind in {tool["kind"] for tool in catalog["tools"]}:
        assert f"{BASE_URL}/categories/{kind}/" in urls
    for profile in catalog["profiles"]:
        assert f"{BASE_URL}/profiles/{profile}/" in urls
        content = (site / "profiles" / profile / "index.html").read_text(encoding="utf-8")
        assert f"--profile {profile}" in "".join(checker.Page(content).text)


def test_language_alternates_and_404_indexing(site, checker):
    english = checker.Page((site / "index.html").read_text(encoding="utf-8"))
    chinese = checker.Page((site / "zh/index.html").read_text(encoding="utf-8"))
    assert english.lang == "en"
    assert chinese.lang == "zh-CN"
    assert english.alternates == chinese.alternates
    assert english.alternates["en"] == BASE_URL + "/"
    assert english.alternates["zh-CN"] == BASE_URL + "/zh/"
    assert english.alternates["x-default"] == BASE_URL + "/"
    error_page = checker.Page((site / "404.html").read_text(encoding="utf-8"))
    assert "noindex" in ",".join(error_page.meta["robots"])
    assert "404.html" not in (site / "sitemap.xml").read_text(encoding="utf-8")


def test_agent_discovery_routes_share_the_catalog_and_commands(site, checker):
    canonical = json.loads((ROOT / "src/awesome_python_dev/data/catalog.json").read_text(encoding="utf-8"))
    exported = json.loads((site / "catalog.json").read_text(encoding="utf-8"))
    assert exported["profiles"] == canonical["profiles"]
    assert [tool["id"] for tool in exported["tools"]] == [tool["id"] for tool in canonical["tools"]]
    assert exported["discovery"]["catalog_scope"] == "source-snapshot"
    assert exported["discovery"]["release_note"]
    assert (site / "agents/index.md").is_file()
    assert f"{BASE_URL}/agents/" in (site / "sitemap.xml").read_text(encoding="utf-8")
    for document in site.rglob("index.html"):
        page = checker.Page(document.read_text(encoding="utf-8"))
        markdown = document.with_suffix(".md")
        assert markdown.is_file()
        assert page.markdown_alternates == [f"{BASE_URL}/{markdown.relative_to(site).as_posix()}"]
        assert page.describedby == [f"{BASE_URL}/llms.txt"]
    for tool in canonical["tools"]:
        markdown = (site / "tools" / tool["id"] / "index.md").read_text(encoding="utf-8")
        if tool.get("install"):
            assert f"--tools {tool['id']}" in markdown
        else:
            assert f"--tools {tool['id']}" not in markdown
            assert "reference" in markdown.lower()


def test_checker_rejects_missing_or_misdirected_agent_documents(site, checker):
    document = site / "agents/index.md"
    original = document.read_text(encoding="utf-8")
    document.unlink()
    assert any("broken local link" in error for error in checker.check_site(site, BASE_URL))
    document.write_text(original, encoding="utf-8")
    llms = site / "llms.txt"
    llms.write_text(llms.read_text(encoding="utf-8") + "\n[Bad route](https://m9rco.github.io/elsewhere/index.md)\n", encoding="utf-8")
    assert any("discovery link escapes site base path" in error for error in checker.check_site(site, BASE_URL))


def test_checker_rejects_catalog_drift_and_reference_install_commands(site, checker):
    path = site / "catalog.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    reference = next(tool for tool in catalog["tools"] if not tool.get("install"))
    reference["installable"] = True
    reference["preview_command"] = f"uvx awesome-python-dev init --tools {reference['id']} --dry-run"
    catalog["profiles"]["invalid-profile"] = [reference["id"]]
    path.write_text(json.dumps(catalog), encoding="utf-8")
    errors = checker.check_site(site, BASE_URL)
    assert any("kind/installability differs" in error for error in errors)
    assert any("reference-only tool" in error for error in errors)
    assert any("profiles must match" in error for error in errors)
    assert any("checksum" in error for error in errors)


def test_checker_rejects_changed_recipe_even_with_recomputed_checksum(site, checker):
    path = site / "catalog.json"
    exported = json.loads(path.read_text(encoding="utf-8"))
    recipe = next(tool["install"] for tool in exported["tools"] if tool.get("install", {}).get("url"))
    recipe["url"] = "https://example.org/unreviewed-skill.tar.gz"
    original = {key: value for key, value in exported.items() if key != "discovery"}
    derived = {"installable", "url", "markdown_url", "preview_command"}
    original["tools"] = [
        {key: value for key, value in tool.items() if key not in derived}
        for tool in exported["tools"]
    ]
    payload = json.dumps(original, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    exported["discovery"]["catalog_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    path.write_text(json.dumps(exported), encoding="utf-8")

    errors = checker.check_site(site, BASE_URL)
    assert any("exactly match the CLI catalog" in error for error in errors)
    assert not any("checksum" in error for error in errors)


def test_checker_rejects_unknown_markdown_commands_and_filesystem_paths(site, checker):
    document = site / "agents/index.md"
    document.write_text(
        document.read_text(encoding="utf-8")
        + "\n`uvx awesome-python-dev init --tools missing-tool --profile missing-profile`\n"
        + "[Local source](file:///Users/example/project/catalog.json)\n",
        encoding="utf-8",
    )
    errors = checker.check_site(site, BASE_URL)
    assert any("invalid installable tool" in error for error in errors)
    assert any("unknown profile" in error for error in errors)
    assert any("absolute filesystem path" in error for error in errors)


def test_checker_rejects_broken_link_and_missing_fragment(site, checker):
    index = site / "index.html"
    original = index.read_text(encoding="utf-8")
    index.write_text(
        original.replace("</main>", '<a href="missing/">Missing</a></main>'), encoding="utf-8"
    )
    assert any("broken local link" in error for error in checker.check_site(site, BASE_URL))
    index.write_text(
        original.replace("</main>", '<a href="#nonexistent">Missing</a></main>'), encoding="utf-8"
    )
    assert any("missing fragment" in error for error in checker.check_site(site, BASE_URL))


def test_checker_rejects_stale_canonical_and_duplicate_sitemap(site, checker):
    index = site / "index.html"
    source = index.read_text(encoding="utf-8")
    index.write_text(
        source.replace(f'href="{BASE_URL}/"', 'href="https://old.example/"', 1), encoding="utf-8"
    )
    assert any("canonical" in error for error in checker.check_site(site, BASE_URL))
    index.write_text(source, encoding="utf-8")
    sitemap_path = site / "sitemap.xml"
    tree = ElementTree.parse(sitemap_path)
    root = tree.getroot()
    root.append(root[0])
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    assert any("duplicate URLs" in error for error in checker.check_site(site, BASE_URL))


def test_checker_rejects_missing_structured_data(site, checker):
    index = site / "index.html"
    source = index.read_text(encoding="utf-8").replace('type="application/ld+json"', 'type="application/json"')
    index.write_text(source, encoding="utf-8")
    assert any("missing JSON-LD" in error for error in checker.check_site(site, BASE_URL))


def test_catalog_description_cannot_inject_html_or_close_json_ld(
    tmp_path, builder, checker, monkeypatch
):
    catalog = deepcopy(builder.load_catalog())
    payload = '安全 " onclick="alert(2)" & </script><script>alert(1)</script>'
    tool = catalog["tools"][0]
    tool["description"] = payload
    monkeypatch.setattr(builder, "load_catalog", lambda: catalog)
    monkeypatch.setattr(checker, "load_catalog", lambda: catalog)
    output = tmp_path / "site"
    builder.build_site(output, BASE_URL)

    for document in output.rglob("*.html"):
        assert "</script><script>alert(1)</script>" not in document.read_text(encoding="utf-8")
    source = (output / "tools" / tool["id"] / "index.html").read_text(encoding="utf-8")
    assert html.escape(payload, quote=True) in source
    page = checker.Page(source)
    assert len(page.meta["description"]) == 1
    assert page.meta["description"][0].startswith(payload)
    graph = json.loads(page.json_ld[0])["@graph"]
    webpage = next(node for node in graph if node["@type"] == "WebPage")
    assert webpage["description"].startswith(payload)
    assert checker.check_site(output, BASE_URL) == []


def test_build_refuses_nonempty_output_without_removing_user_files(tmp_path, builder):
    output = tmp_path / "documents"
    output.mkdir()
    sentinel = output / "important.txt"
    sentinel.write_text("保留我的文件", encoding="utf-8")

    with pytest.raises(ValueError, match="nonempty"):
        builder.build_site(output, BASE_URL)

    assert sentinel.read_text(encoding="utf-8") == "保留我的文件"
    assert list(output.iterdir()) == [sentinel]


def test_build_refuses_symlink_output_even_for_existing_generated_site(tmp_path, builder):
    target = tmp_path / "target"
    target.mkdir()
    (target / ".apd-generated-site").write_text("Existing build", encoding="utf-8")
    sentinel = target / "important.txt"
    sentinel.write_text("原始内容", encoding="utf-8")
    output = tmp_path / "linked-output"
    try:
        output.symlink_to(target, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"This platform does not permit directory symlinks: {exc}")

    with pytest.raises(ValueError, match="symlink"):
        builder.build_site(output, BASE_URL)

    assert output.is_symlink()
    assert sentinel.read_text(encoding="utf-8") == "原始内容"
