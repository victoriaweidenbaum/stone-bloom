# Stone Bloom

Static site for [stonebloom.studio](https://www.stonebloom.studio) — clay art and jewelry by Victoria Weidenbaum. Hosted on GitHub Pages (no build step on the server; the generated HTML is committed).

## Editing

Page content lives in `build.py`. After changing it, regenerate the pages:

```bash
python3 build.py
```

Preview locally:

```bash
python3 -m http.server 4173
```

- `css/style.css` — all styling. Layout uses a 24-column grid (8 on mobile); each block's position is set with `--m` (mobile) and `--d` (desktop) `grid-area` values.
- `images/` — every photo has an `-800.jpg` and `-1600.jpg` version. To add one, export both sizes and reference the base name in `build.py`.
- `fonts/` — self-hosted open-source fonts (Lustria, Encode Sans Expanded, Arimo).

## Forms

The contact form and newsletter signup post to [FormSubmit](https://formsubmit.co), which forwards each submission to the email set in `build.py` (`EMAIL`). The first submission triggers a one-time activation email from FormSubmit — click the link in it to start receiving messages.

## Fonts

The original Squarespace site used Adobe Fonts (Teimer, Grange Extended). The CSS font stacks still list them first, so adding an Adobe Fonts web-project `<link>` to the `<head>` in `build.py` restores them; otherwise the bundled free look-alikes are used.
