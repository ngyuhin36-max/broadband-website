"""Wrap GA4/Google Ads loading with client-side bot detection.

Blocks headless browsers (Puppeteer, Selenium, PhantomJS, Playwright, etc.) from
triggering GA4 events — stops the Singapore bot flood from polluting analytics
and firing phantom Google Ads clicks.

Matches both multi-line and minified single-line GA4 snippets. Only files that
contain an exact match are rewritten. Run from repo root.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent

SHIELD_CORE = (
    "(function(){var n=navigator,w=window;function b(){"
    "if(n.webdriver===true)return 1;"
    "if(/HeadlessChrome|PhantomJS|Electron|puppeteer|playwright|slimerjs/i.test(n.userAgent))return 1;"
    "if(w.callPhantom||w._phantom||w.__selenium_unwrapped||w.__webdriver_evaluate||w.__driver_evaluate||w.__fxdriver_evaluate||w.domAutomation||w.domAutomationController)return 1;"
    "if(!n.languages||n.languages.length===0)return 1;"
    "if(n.plugins&&n.plugins.length===0&&!/Mobi|Android|iPhone|iPad/i.test(n.userAgent))return 1;"
    "return 0}"
    "w.dataLayer=w.dataLayer||[];function gtag(){dataLayer.push(arguments)}w.gtag=gtag;"
    "if(!b()){"
    "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385';document.head.appendChild(s);"
    "gtag('js',new Date());gtag('config','G-23EZE5P385');"
)

REPLACEMENT_FULL = (
    '<!-- Google Analytics 4 + Google Ads (with bot shield) -->\n'
    '<script>\n'
    + SHIELD_CORE
    + "gtag('config','AW-959473638');"
    + "}})();\n"
    + '</script>'
)

REPLACEMENT_GA_ONLY = (
    '<!-- Google Analytics 4 (with bot shield) -->\n'
    '<script>\n'
    + SHIELD_CORE
    + "}})();\n"
    + '</script>'
)

SHIELD_CORE_ADS_ONLY = (
    "(function(){var n=navigator,w=window;function b(){"
    "if(n.webdriver===true)return 1;"
    "if(/HeadlessChrome|PhantomJS|Electron|puppeteer|playwright|slimerjs/i.test(n.userAgent))return 1;"
    "if(w.callPhantom||w._phantom||w.__selenium_unwrapped||w.__webdriver_evaluate||w.__driver_evaluate||w.__fxdriver_evaluate||w.domAutomation||w.domAutomationController)return 1;"
    "if(!n.languages||n.languages.length===0)return 1;"
    "if(n.plugins&&n.plugins.length===0&&!/Mobi|Android|iPhone|iPad/i.test(n.userAgent))return 1;"
    "return 0}"
    "w.dataLayer=w.dataLayer||[];function gtag(){dataLayer.push(arguments)}w.gtag=gtag;"
    "if(!b()){"
    "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=AW-959473638';document.head.appendChild(s);"
    "gtag('js',new Date());gtag('config','AW-959473638');"
    "}})();"
)

REPLACEMENT_ADS_ONLY = (
    '<!-- Google Ads (with bot shield) -->\n'
    '<script>\n'
    + SHIELD_CORE_ADS_ONLY
    + "\n</script>"
)

PATTERN_FULL = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-23EZE5P385"></script>'
    r'\s*<script>[\s\S]*?AW-959473638[\s\S]*?</script>',
    re.MULTILINE,
)

PATTERN_GA_ONLY = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-23EZE5P385"></script>'
    r'\s*<script>(?:(?!AW-959473638)[\s\S])*?</script>',
    re.MULTILINE,
)

PATTERN_ADS_ONLY = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=AW-959473638"></script>'
    r'\s*<script>(?:(?!G-23EZE5P385)[\s\S])*?</script>',
    re.MULTILINE,
)


def is_target(path: Path) -> bool:
    return path.suffix == '.html'


def main():
    changed = 0
    skipped_nomatch = 0
    already_patched = 0
    scanned = 0

    for html in ROOT.rglob('*.html'):
        if not is_target(html):
            continue
        scanned += 1
        try:
            text = html.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue

        if 'with bot shield' in text:
            already_patched += 1
            continue

        new_text, n = PATTERN_FULL.subn(REPLACEMENT_FULL, text, count=1)
        if n == 0:
            new_text, n = PATTERN_GA_ONLY.subn(REPLACEMENT_GA_ONLY, text, count=1)
        if n == 0:
            new_text, n = PATTERN_ADS_ONLY.subn(REPLACEMENT_ADS_ONLY, text, count=1)
        if n == 0:
            skipped_nomatch += 1
            continue

        html.write_text(new_text, encoding='utf-8')
        changed += 1

    print(f'Scanned (non-pages HTML): {scanned}')
    print(f'Patched this run:         {changed}')
    print(f'Already patched:          {already_patched}')
    print(f'No GA4 match (skipped):   {skipped_nomatch}')


if __name__ == '__main__':
    main()
