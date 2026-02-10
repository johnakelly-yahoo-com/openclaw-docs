"""MkDocs hook to rewrite absolute image paths to relative ones.

The OpenClaw docs use absolute paths like /assets/foo.png and /images/foo.png
which don't resolve correctly in MkDocs. This hook rewrites them to relative
paths at build time without modifying the source files.
"""

import re
import os


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Rewrite absolute /assets/ and /images/ paths to relative paths."""

    # Calculate the relative path prefix based on page depth
    # e.g., a page at install/docker.md needs ../assets/
    # a page at channels/discord/setup.md needs ../../assets/
    page_path = page.file.src_path
    depth = page_path.count(os.sep)

    # For language-prefixed paths like ja/install/docker.md,
    # assets are at the root docs level, so we need to go up past the lang dir too
    prefix = "../" * depth if depth > 0 else "./"

    # Rewrite src="/assets/..." to src="<prefix>assets/..."
    markdown = re.sub(
        r'src="/assets/',
        f'src="{prefix}assets/',
        markdown,
    )

    # Rewrite src="/images/..." to src="<prefix>images/..."
    markdown = re.sub(
        r'src="/images/',
        f'src="{prefix}images/',
        markdown,
    )

    # Rewrite markdown image syntax ![alt](/assets/...) and ![alt](/images/...)
    markdown = re.sub(
        r'\]\(/assets/',
        f']({prefix}assets/',
        markdown,
    )
    markdown = re.sub(
        r'\]\(/images/',
        f']({prefix}images/',
        markdown,
    )

    return markdown
