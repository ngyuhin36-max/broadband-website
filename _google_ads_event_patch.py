"""Google Ads event snippet patch — installs standalone AW tag + page-view
conversion event on every HTML, outside the bot shield.

Why this exists:
  - Bot shield v2 hides gtag.js from headless Chrome (Google Ads validator).
  - Validator couldn't detect AW-959473638 conversion action across the site.
  - Index.html was patched manually; this script propagates the same change
    to all other HTML files so deep-link landing pages also count conversions
    and pass validator checks.

What it does on each file:
  1. Finds the existing bot-shield-v2 block.
  2. Inserts a NEW standalone Google Ads block (outside the shield) BEFORE it.
  3. Removes `gtag('config','AW-959473638');` from inside the shield (now
     redundant — standalone block handles AW; shield only handles GA4).

Idempotent: re-run safe. Skips files that already contain 'FjZMCOqYza0cEObPwckD'.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent

CONVERSION_ID = "AW-959473638/FjZMCOqYza0cEObPwckD"
MARKER = "FjZMCOqYza0cEObPwckD"

# Standalone Google Ads block (outside bot shield — validator can see it)
STANDALONE_BLOCK = (
    '    <!-- Google Ads standalone tag (for Ads validator detection, bypasses bot shield) -->\n'
    '    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-959473638"></script>\n'
    '    <script>\n'
    '      window.dataLayer = window.dataLayer || [];\n'
    '      function gtag(){dataLayer.push(arguments);}\n'
    "      gtag('js', new Date());\n"
    "      gtag('config', 'AW-959473638');\n"
    "      gtag('event', 'conversion', {'send_to': '" + CONVERSION_ID + "'});\n"
    '    </script>\n'
    '\n'
)

# Match the existing bot shield V2 comment + script block.
# Replace it with: standalone block + renamed comment + shield (AW config stripped).
SHIELD_COMMENT_OLD = "<!-- Google Analytics 4 + Google Ads (with bot shield v2) -->"
SHIELD_COMMENT_NEW = "<!-- Google Analytics 4 (with bot shield v2) -->"

# Pattern: capture indentation before the comment so we preserve it.
SHIELD_BLOCK_RE = re.compile(
    r"([ \t]*)" + re.escape(SHIELD_COMMENT_OLD) + r"\s*\n([ \t]*)<script>\n(.*?)</script>",
    re.DOTALL,
)

# Strip the redundant AW config call from inside the shield body.
AW_CONFIG_RE = re.compile(r"gtag\('config','AW-959473638'\);")


# For files WITHOUT bot shield: locate the vanilla GA4 gtag.js script tag
# so we can insert the AW standalone block right before it.
VANILLA_GA4_RE = re.compile(
    r'([ \t]*)<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-23EZE5P385"></script>'
)

# Fallback: insert before </head>.
HEAD_CLOSE_RE = re.compile(r'([ \t]*)</head>', re.IGNORECASE)


def patch_file(path: Path) -> str:
    """Return one of: 'patched-shield', 'patched-vanilla', 'patched-head',
    'skip-marker', 'skip-no-head', 'skip-error'."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "skip-error"

    if MARKER in text:
        return "skip-marker"

    # Path 1: existing bot shield V2 block — replace with new structure.
    m = SHIELD_BLOCK_RE.search(text)
    if m:
        comment_indent = m.group(1)
        script_indent = m.group(2)
        shield_body = m.group(3)
        new_shield_body = AW_CONFIG_RE.sub("", shield_body)
        standalone = STANDALONE_BLOCK.replace("    ", comment_indent)
        new_block = (
            standalone
            + comment_indent + SHIELD_COMMENT_NEW + "\n"
            + script_indent + "<script>\n"
            + new_shield_body
            + "</script>"
        )
        path.write_text(text[: m.start()] + new_block + text[m.end():], encoding="utf-8")
        return "patched-shield"

    # Path 2: vanilla GA4 install (no bot shield) — insert AW block right before it.
    m = VANILLA_GA4_RE.search(text)
    if m:
        indent = m.group(1)
        standalone = STANDALONE_BLOCK.replace("    ", indent).rstrip() + "\n\n" + indent
        path.write_text(text[: m.start()] + standalone + text[m.start():], encoding="utf-8")
        return "patched-vanilla"

    # Path 3: no analytics at all — insert AW block right before </head>.
    m = HEAD_CLOSE_RE.search(text)
    if m:
        indent = m.group(1) + "    "
        standalone = STANDALONE_BLOCK.replace("    ", indent)
        path.write_text(text[: m.start()] + standalone + text[m.start():], encoding="utf-8")
        return "patched-head"

    return "skip-no-head"


def main():
    counts = {"patched-shield": 0, "patched-vanilla": 0, "patched-head": 0,
              "skip-marker": 0, "skip-no-head": 0, "skip-error": 0}
    html_files = list(ROOT.rglob("*.html"))
    print(f"Scanning {len(html_files)} HTML files...")

    for path in html_files:
        result = patch_file(path)
        counts[result] += 1

    print("\nResults:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"\nTotal: {sum(counts.values())}")


if __name__ == "__main__":
    main()
