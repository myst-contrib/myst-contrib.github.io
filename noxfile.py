"""Nox sessions for the myst-contrib landing page."""

import json
import subprocess
from pathlib import Path
from urllib.request import urlretrieve

import nox

# Use uv for faster installs
nox.options.default_venv_backend = "uv|virtualenv"

# The site mirrors the org-wide README, fetched fresh before each build
README_URL = (
    "https://raw.githubusercontent.com/myst-contrib/.github/main/profile/README.md"
)

# Utility repositories that aren't community projects
EXCLUDED_REPOS = {".github", "myst-contrib.github.io"}


def fetch_pages():
    """Fetch / generate the site's pages: the org README and the repository list."""
    urlretrieve(README_URL, "docs/index.md")

    listing = subprocess.run(
        [
            "gh",
            "repo",
            "list",
            "myst-contrib",
            "--json",
            "name,description,url,homepageUrl,repositoryTopics,stargazerCount,updatedAt",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    repos = [r for r in json.loads(listing.stdout) if r["name"] not in EXCLUDED_REPOS]

    lines = [
        "# Repositories",
        "",
        "The repositories in the [myst-contrib organization](https://github.com/orgs/myst-contrib/repositories).",
        "",
        "| Repository | Description | Topics | ★ | Updated | Docs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for repo in sorted(repos, key=lambda r: r["name"].lower()):
        topics = ", ".join(t["name"] for t in repo["repositoryTopics"] or [])
        docs = f"[docs]({repo['homepageUrl']})" if repo["homepageUrl"] else ""
        lines.append(
            f"| [{repo['name']}]({repo['url']}) "
            f"| {repo['description'] or ''} "
            f"| {docs} "
            f"| {topics} "
            f"| {repo['stargazerCount']} "
            f"| {repo['updatedAt'][:10]} |"
        )
    Path("docs/repositories.md").write_text("\n".join(lines) + "\n")


@nox.session(name="docs")
def docs(session):
    """Build the documentation as static HTML."""
    fetch_pages()
    session.chdir("docs")
    session.install("mystmd")
    session.run("myst", "build", "--html")


@nox.session(name="docs-live")
def docs_live(session):
    """Start a live development server for the documentation."""
    fetch_pages()
    session.chdir("docs")
    session.install("mystmd")
    session.run("myst", "start")


@nox.session
def clean(session):
    """Clean the documentation build artifacts."""
    session.chdir("docs")
    session.install("mystmd")
    session.run("myst", "clean", "-y")
