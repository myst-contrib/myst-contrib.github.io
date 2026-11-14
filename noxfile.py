"""Nox sessions for the myst-contrib landing page."""

import json
import subprocess
from pathlib import Path
from urllib.request import urlopen

import nox

# Use uv for faster installs
nox.options.default_venv_backend = "uv|virtualenv"

# The site mirrors the org-wide README, fetched fresh before each build
README_URL = (
    "https://raw.githubusercontent.com/myst-contrib/.github/main/profile/README.md"
)

# Utility repositories that aren't community projects
EXCLUDED_REPOS = {".github", "myst-contrib.github.io"}

# Inserted into the README after its intro
PROJECTS_SECTION = """## Projects

:::{listing}
:source: json
:path: repos.json
:display: list
:sort: updated-desc
:limit: 0
:::

See [all repositories](repositories.md) for more details.
"""


def fetch_pages():
    """Write docs/index.md from the org README and docs/repos.json from the org's repositories."""
    readme = urlopen(README_URL).read().decode()

    listing = subprocess.run(
        [
            "gh",
            "repo",
            "list",
            "myst-contrib",
            "--json",
            "name,description,url,homepageUrl,repositoryTopics,stargazerCount,pushedAt",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    # Items for the myst-listing plugin, used by index.md and repositories.md
    items = [
        {
            "title": r["name"],
            # Many homepages are set as http://, which skips internal_domains matching
            "url": (r["homepageUrl"] or r["url"]).replace("http://", "https://", 1),
            "description": r["description"],
            "tags": [t["name"] for t in r["repositoryTopics"] or []],
            "stars": r["stargazerCount"],
            "updated": r["pushedAt"][:10],
        }
        for r in json.loads(listing.stdout)
        if r["name"] not in EXCLUDED_REPOS
    ]
    Path("docs/repos.json").write_text(json.dumps(items, indent=2))

    # Landing page: the README intro, then the project list, then the rest of the README
    intro, sep, rest = readme.partition("\n## ")
    Path("docs/index.md").write_text(intro + "\n" + PROJECTS_SECTION + sep + rest)


@nox.session(name="docs")
def docs(session):
    """Build the documentation as static HTML."""
    fetch_pages()
    session.chdir("docs")
    session.install("mystmd")
    session.run("myst", "build", "--html")


@nox.session(name="docs-live")
@nox.session(name="docs:live")
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
