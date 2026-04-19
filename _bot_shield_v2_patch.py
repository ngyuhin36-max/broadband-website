"""Bot shield V2 — upgrades V1 shield and installs on fresh files.

V2 adds 4 checks (each in try-catch, fail-open to avoid false positives):
1. iPhone/iPad UA but maxTouchPoints === 0 (stealth bot spoofing mobile UA)
2. Chrome UA on desktop but window.chrome missing
3. Desktop with outerWidth/outerHeight === 0 (headless default)
4. WebGL renderer is SwiftShader / llvmpipe / Mesa Offscreen (headless GPU)

Handles both V1 upgrade and fresh installs. Idempotent: marker 'with bot shield v2'
is used to skip re-patching.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent

SHIELD_CORE_V2 = (
    "(function(){var n=navigator,w=window;function b(){"
    # V1 checks (unchanged, proven)
    "if(n.webdriver===true)return 1;"
    "if(/HeadlessChrome|PhantomJS|Electron|puppeteer|playwright|slimerjs/i.test(n.userAgent))return 1;"
    "if(w.callPhantom||w._phantom||w.__selenium_unwrapped||w.__webdriver_evaluate||w.__driver_evaluate||w.__fxdriver_evaluate||w.domAutomation||w.domAutomationController)return 1;"
    "if(!n.languages||n.languages.length===0)return 1;"
    "var ua=n.userAgent,isMobile=/Mobi|Android|iPhone|iPad/i.test(ua);"
    "if(n.plugins&&n.plugins.length===0&&!isMobile)return 1;"
    # V2 checks (fail-open on error)
    "try{if(/iPhone|iPad/i.test(ua)&&n.maxTouchPoints===0)return 1;}catch(e){}"
    "try{if(!isMobile&&/Chrome/.test(ua)&&!w.chrome)return 1;}catch(e){}"
    "try{if(!isMobile&&(w.outerHeight===0||w.outerWidth===0))return 1;}catch(e){}"
    "try{if(!isMobile){var c=document.createElement('canvas'),gl=c.getContext('webgl')||c.getContext('experimental-webgl');"
    "if(gl){var ext=gl.getExtension('WEBGL_debug_renderer_info');"
    "if(ext){var r=gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)||'';"
    "if(/SwiftShader|llvmpipe|Mesa OffScreen/i.test(r))return 1;}}}}catch(e){}"
    "return 0}"
    "w.dataLayer=w.dataLayer||[];function gtag(){dataLayer.push(arguments)}w.gtag=gtag;"
    "if(!b()){"
    "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-23EZE5P385';document.head.appendChild(s);"
    "gtag('js',new Date());gtag('config','G-23EZE5P385');"
)

REPLACEMENT_FULL_V2 = (
    '<!-- Google Analytics 4 + Google Ads (with bot shield v2) -->\n'
    '<script>\n'
    + SHIELD_CORE_V2
    + "gtag('config','AW-959473638');"
    + "}})();\n"
    + '</script>'
)

REPLACEMENT_GA_ONLY_V2 = (
    '<!-- Google Analytics 4 (with bot shield v2) -->\n'
    '<script>\n'
    + SHIELD_CORE_V2
    + "}})();\n"
    + '</script>'
)

SHIELD_CORE_ADS_ONLY_V2 = (
    "(function(){var n=navigator,w=window;function b(){"
    "if(n.webdriver===true)return 1;"
    "if(/HeadlessChrome|PhantomJS|Electron|puppeteer|playwright|slimerjs/i.test(n.userAgent))return 1;"
    "if(w.callPhantom||w._phantom||w.__selenium_unwrapped||w.__webdriver_evaluate||w.__driver_evaluate||w.__fxdriver_evaluate||w.domAutomation||w.domAutomationController)return 1;"
    "if(!n.languages||n.languages.length===0)return 1;"
    "var ua=n.userAgent,isMobile=/Mobi|Android|iPhone|iPad/i.test(ua);"
    "if(n.plugins&&n.plugins.length===0&&!isMobile)return 1;"
    "try{if(/iPhone|iPad/i.test(ua)&&n.maxTouchPoints===0)return 1;}catch(e){}"
    "try{if(!isMobile&&/Chrome/.test(ua)&&!w.chrome)return 1;}catch(e){}"
    "try{if(!isMobile&&(w.outerHeight===0||w.outerWidth===0))return 1;}catch(e){}"
    "try{if(!isMobile){var c=document.createElement('canvas'),gl=c.getContext('webgl')||c.getContext('experimental-webgl');"
    "if(gl){var ext=gl.getExtension('WEBGL_debug_renderer_info');"
    "if(ext){var r=gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)||'';"
    "if(/SwiftShader|llvmpipe|Mesa OffScreen/i.test(r))return 1;}}}}catch(e){}"
    "return 0}"
    "w.dataLayer=w.dataLayer||[];function gtag(){dataLayer.push(arguments)}w.gtag=gtag;"
    "if(!b()){"
    "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=AW-959473638';document.head.appendChild(s);"
    "gtag('js',new Date());gtag('config','AW-959473638');"
    "}})();"
)

REPLACEMENT_ADS_ONLY_V2 = (
    '<!-- Google Ads (with bot shield v2) -->\n'
    '<script>\n'
    + SHIELD_CORE_ADS_ONLY_V2
    + "\n</script>"
)

# --- V1 -> V2 upgrade patterns (match existing V1 shield blocks) ---
V1_FULL = re.compile(
    r'<!-- Google Analytics 4 \+ Google Ads \(with bot shield\) -->\s*'
    r'<script>\s*\(function\(\)\{var n=navigator[\s\S]*?AW-959473638[\s\S]*?\}\)\(\);\s*</script>',
    re.MULTILINE,
)
V1_GA_ONLY = re.compile(
    r'<!-- Google Analytics 4 \(with bot shield\) -->\s*'
    r'<script>\s*\(function\(\)\{var n=navigator[\s\S]*?\}\)\(\);\s*</script>',
    re.MULTILINE,
)
V1_ADS_ONLY = re.compile(
    r'<!-- Google Ads \(with bot shield\) -->\s*'
    r'<script>\s*\(function\(\)\{var n=navigator[\s\S]*?\}\)\(\);\s*</script>',
    re.MULTILINE,
)

# --- Fresh install patterns (original unshielded GA4 snippets) ---
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


def main():
    upgraded = 0
    fresh = 0
    already_v2 = 0
    skipped = 0
    scanned = 0

    for html in ROOT.rglob('*.html'):
        scanned += 1
        try:
            text = html.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue

        if 'with bot shield v2' in text:
            already_v2 += 1
            continue

        new_text = text
        n_total = 0

        # Try V1 -> V2 upgrades first
        new_text, n = V1_FULL.subn(REPLACEMENT_FULL_V2, new_text, count=1)
        n_total += n
        if n == 0:
            new_text, n = V1_GA_ONLY.subn(REPLACEMENT_GA_ONLY_V2, new_text, count=1)
            n_total += n
        if n == 0:
            new_text, n = V1_ADS_ONLY.subn(REPLACEMENT_ADS_ONLY_V2, new_text, count=1)
            n_total += n

        if n_total > 0:
            html.write_text(new_text, encoding='utf-8')
            upgraded += 1
            continue

        # Fresh install (no shield yet)
        new_text, n = PATTERN_FULL.subn(REPLACEMENT_FULL_V2, text, count=1)
        if n == 0:
            new_text, n = PATTERN_GA_ONLY.subn(REPLACEMENT_GA_ONLY_V2, text, count=1)
        if n == 0:
            new_text, n = PATTERN_ADS_ONLY.subn(REPLACEMENT_ADS_ONLY_V2, text, count=1)
        if n == 0:
            skipped += 1
            continue

        html.write_text(new_text, encoding='utf-8')
        fresh += 1

    print(f'Scanned:         {scanned}')
    print(f'Upgraded V1->V2: {upgraded}')
    print(f'Fresh install:   {fresh}')
    print(f'Already V2:      {already_v2}')
    print(f'No match:        {skipped}')


if __name__ == '__main__':
    main()
