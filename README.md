# myst-contrib.github.io

The landing page for the [myst-contrib organization](https://github.com/myst-contrib), served at <https://myst-contrib.github.io>.

## How it works

The site is a minimal [MyST Markdown](https://mystmd.org) site in `docs/` whose pages are generated at build time by `noxfile.py`:

- `docs/index.md` mirrors the [org-wide README](https://github.com/myst-contrib/.github/blob/main/profile/README.md).
- `docs/repositories.md` lists the org's repositories, via the `gh` CLI.

The [deploy workflow](.github/workflows/deploy.yml) rebuilds on push and daily, so updates to the org README and repositories flow through automatically.

To update the content of the site, edit the org README in [`myst-contrib/.github`](https://github.com/myst-contrib/.github).

## Build locally

Use [nox](https://nox.thea.codes), which fetches the org README into `docs/index.md` and runs MyST for you:

```sh
nox -s docs       # build static HTML in docs/_build/html
nox -s docs-live  # start a live development server
```
