# myst-contrib.github.io

The landing page for the [myst-contrib organization](https://github.com/myst-contrib), served at <https://myst-contrib.github.io>.

## How it works

The site is a [MyST Markdown](https://mystmd.org) site in `docs/`.
At build time, `noxfile.py` writes two files:

- `docs/index.md`: the [org-wide README](https://github.com/myst-contrib/.github/blob/main/profile/README.md), with a list of projects added after its intro.
- `docs/repos.json`: the org's repositories, from the `gh` CLI. The [myst-listing](https://github.com/myst-contrib/myst-listing) plugin shows them on the landing page and on `docs/repositories.md`.

The [deploy workflow](.github/workflows/deploy.yml) rebuilds the site on every push to `main` and once a day, so changes to the org README and repositories show up within a day.

To change the landing page text, edit the org README in [`myst-contrib/.github`](https://github.com/myst-contrib/.github).
To change a project's entry, edit that repository's description, topics, or homepage on GitHub.

## Build locally

Use [nox](https://nox.thea.codes), which generates the pages and runs MyST for you.
You need the [`gh` CLI](https://cli.github.com) installed and logged in, because `noxfile.py` uses it to list the repositories.

```sh
nox -s docs       # build static HTML in docs/_build/html
nox -s docs-live  # start a live development server
```
