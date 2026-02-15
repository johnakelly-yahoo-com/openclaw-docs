"""MkDocs hook for veiseule.ai — rewrite absolute paths to relative ones and
replace the homepage with a clean, professional version.

The OpenClaw docs use absolute paths like /assets/foo.png, /images/foo.png,
and internal links like /plugins/manifest, /tools/web, etc.
These don't resolve correctly in MkDocs when served under a subdirectory.
This hook rewrites them all to relative paths at build time without
modifying the source files.

Additionally, the Mintlify docs use "slug-only" links (e.g., /showcase
instead of /start/showcase). This hook expands those to full paths before
converting to relative links.

It also replaces the homepage (index.md) with the veiseule.ai branded
version that removes Mintlify components and novelty graphics.

Path calculation:
  MkDocs with use_directory_urls=true serves foo/bar.md at URL /foo/bar/
  (as /foo/bar/index.html). This means the browser's base path is one
  level deeper than the file path. We must account for this when
  calculating how many ../ are needed to reach the language root.

  For English pages:
    index.md          -> URL /              -> prefix ./
    foo.md            -> URL /foo/          -> prefix ../
    foo/bar.md        -> URL /foo/bar/      -> prefix ../../
    foo/index.md      -> URL /foo/          -> prefix ../

  For language-prefixed pages (e.g., ja/):
    ja/index.md       -> URL /ja/           -> prefix ./
    ja/foo.md         -> URL /ja/foo/       -> prefix ../
    ja/foo/bar.md     -> URL /ja/foo/bar/   -> prefix ../../
"""

import re
import os


# Known language codes from our i18n configuration
LANGUAGE_CODES = {
    "ja", "ko", "zh-TW", "zh-CN", "es", "fr", "de", "pt-BR",
    "vi", "sv", "fil", "tl", "nl", "ur", "ar", "hi", "da", "pl",
    "th", "tr", "my", "ru", "uz",
    # Also match the folder names as they appear on disk
    "ja-JP",
}


# ── Slug-to-full-path mapping ──────────────────────────────────────
# Mintlify uses flat slugs (e.g., /showcase resolves to start/showcase).
# This map covers every .md file whose slug differs from its full path.
# Conflicts (same slug, multiple files) are resolved by picking the most
# likely target based on the navigation structure.
SLUG_MAP = {
    "AGENTS": "reference/templates/AGENTS",
    "AGENTS.default": "reference/AGENTS.default",
    "BOOT": "reference/templates/BOOT",
    "BOOTSTRAP": "reference/templates/BOOTSTRAP",
    "HEARTBEAT": "reference/templates/HEARTBEAT",
    "IDENTITY": "reference/templates/IDENTITY",
    "RELEASING": "reference/RELEASING",
    "SOUL": "reference/templates/SOUL",
    "TOOLS": "reference/templates/TOOLS",
    "USER": "reference/templates/USER",
    "acp": "cli/acp",
    "agent": "concepts/agent",
    "agent-loop": "concepts/agent-loop",
    "agent-send": "tools/agent-send",
    "agent-tools": "plugins/agent-tools",
    "agent-workspace": "concepts/agent-workspace",
    "agents": "cli/agents",
    "android": "platforms/android",
    "ansible": "install/ansible",
    "anthropic": "providers/anthropic",
    "api-usage-costs": "reference/api-usage-costs",
    "apply-patch": "tools/apply-patch",
    "approvals": "cli/approvals",
    "architecture": "concepts/architecture",
    "audio": "nodes/audio",
    "auth-monitoring": "automation/auth-monitoring",
    "authentication": "gateway/authentication",
    "background-process": "gateway/background-process",
    "bedrock": "providers/bedrock",
    "bluebubbles": "channels/bluebubbles",
    "bonjour": "gateway/bonjour",
    "bootstrapping": "start/bootstrapping",
    "bridge-protocol": "gateway/bridge-protocol",
    "broadcast-groups": "channels/broadcast-groups",
    "browser": "tools/browser",
    "browser-linux-troubleshooting": "tools/browser-linux-troubleshooting",
    "browser-login": "tools/browser-login",
    "bun": "install/bun",
    "bundled-gateway": "platforms/mac/bundled-gateway",
    "camera": "nodes/camera",
    "canvas": "platforms/mac/canvas",
    "channel-routing": "channels/channel-routing",
    "channels": "cli/channels",
    "child-process": "platforms/mac/child-process",
    "chrome-extension": "tools/chrome-extension",
    "claude-max-api-proxy": "providers/claude-max-api-proxy",
    "clawhub": "tools/clawhub",
    "clawnet": "refactor/clawnet",
    "cli-backends": "gateway/cli-backends",
    "cloudflare-ai-gateway": "providers/cloudflare-ai-gateway",
    "compaction": "concepts/compaction",
    "config": "cli/config",
    "configuration": "gateway/configuration",
    "configuration-examples": "gateway/configuration-examples",
    "configure": "cli/configure",
    "context": "concepts/context",
    "control-ui": "web/control-ui",
    "creating-skills": "tools/creating-skills",
    "credits": "reference/credits",
    "cron": "cli/cron",
    "cron-add-hardening": "experiments/plans/cron-add-hardening",
    "cron-jobs": "automation/cron-jobs",
    "cron-vs-heartbeat": "automation/cron-vs-heartbeat",
    "dashboard": "web/dashboard",
    "debugging": "help/debugging",
    "deepgram": "providers/deepgram",
    "dev-setup": "platforms/mac/dev-setup",
    "development-channels": "install/development-channels",
    "device-models": "reference/device-models",
    "devices": "cli/devices",
    "digitalocean": "platforms/digitalocean",
    "directory": "cli/directory",
    "discord": "channels/discord",
    "discovery": "gateway/discovery",
    "dns": "cli/dns",
    "docker": "install/docker",
    "docs": "cli/docs",
    "docs-directory": "start/docs-directory",
    "doctor": "gateway/doctor",
    "elevated": "tools/elevated",
    "environment": "help/environment",
    "exe-dev": "install/exe-dev",
    "exec": "tools/exec",
    "exec-approvals": "tools/exec-approvals",
    "exec-host": "refactor/exec-host",
    "faq": "help/faq",
    "features": "concepts/features",
    "feishu": "channels/feishu",
    "firecrawl": "tools/firecrawl",
    "flags": "diagnostics/flags",
    "fly": "install/fly",
    "formal-verification": "security/formal-verification",
    "gateway": "cli/gateway",
    "gateway-lock": "gateway/gateway-lock",
    "gcp": "install/gcp",
    "getting-started": "start/getting-started",
    "github-copilot": "providers/github-copilot",
    "glm": "providers/glm",
    "gmail-pubsub": "automation/gmail-pubsub",
    "googlechat": "channels/googlechat",
    "grammy": "channels/grammy",
    "group-messages": "channels/group-messages",
    "group-policy-hardening": "experiments/plans/group-policy-hardening",
    "groups": "channels/groups",
    "health": "gateway/health",
    "heartbeat": "gateway/heartbeat",
    "hetzner": "install/hetzner",
    "hooks": "automation/hooks",
    "hubs": "start/hubs",
    "icon": "platforms/mac/icon",
    "images": "nodes/images",
    "imessage": "channels/imessage",
    "installer": "install/installer",
    "ios": "platforms/ios",
    "line": "channels/line",
    "linux": "platforms/linux",
    "llm-task": "tools/llm-task",
    "lobster": "tools/lobster",
    "local-models": "gateway/local-models",
    "location": "channels/location",
    "location-command": "nodes/location-command",
    "logging": "gateway/logging",
    "logs": "cli/logs",
    "lore": "start/lore",
    "macos": "platforms/macos",
    "macos-vm": "install/macos-vm",
    "manifest": "plugins/manifest",
    "markdown-formatting": "concepts/markdown-formatting",
    "matrix": "channels/matrix",
    "mattermost": "channels/mattermost",
    "media-understanding": "nodes/media-understanding",
    "memory": "concepts/memory",
    "menu-bar": "platforms/mac/menu-bar",
    "message": "cli/message",
    "messages": "concepts/messages",
    "migrating": "install/migrating",
    "minimax": "providers/minimax",
    "model-config": "experiments/proposals/model-config",
    "model-failover": "concepts/model-failover",
    "model-providers": "concepts/model-providers",
    "models": "providers/models",
    "moonshot": "providers/moonshot",
    "msteams": "channels/msteams",
    "multi-agent": "concepts/multi-agent",
    "multi-agent-sandbox-tools": "tools/multi-agent-sandbox-tools",
    "multiple-gateways": "gateway/multiple-gateways",
    "network-model": "gateway/network-model",
    "nextcloud-talk": "channels/nextcloud-talk",
    "nix": "install/nix",
    "node": "install/node",
    "node-issue": "debug/node-issue",
    "nodes": "cli/nodes",
    "nostr": "channels/nostr",
    "oauth": "concepts/oauth",
    "ollama": "providers/ollama",
    "onboard": "cli/onboard",
    "onboarding": "start/onboarding",
    "onboarding-config-protocol": "experiments/onboarding-config-protocol",
    "openai": "providers/openai",
    "openai-http-api": "gateway/openai-http-api",
    "openclaw": "start/openclaw",
    "opencode": "providers/opencode",
    "openresponses-gateway": "experiments/plans/openresponses-gateway",
    "openresponses-http-api": "gateway/openresponses-http-api",
    "openrouter": "providers/openrouter",
    "oracle": "platforms/oracle",
    "outbound-session-mirroring": "refactor/outbound-session-mirroring",
    "pairing": "channels/pairing",
    "peekaboo": "platforms/mac/peekaboo",
    "permissions": "platforms/mac/permissions",
    "plugin": "tools/plugin",
    "plugin-sdk": "refactor/plugin-sdk",
    "plugins": "cli/plugins",
    "poll": "automation/poll",
    "presence": "concepts/presence",
    "protocol": "gateway/protocol",
    "qianfan": "providers/qianfan",
    "queue": "concepts/queue",
    "quickstart": "start/quickstart",
    "qwen": "providers/qwen",
    "raspberry-pi": "platforms/raspberry-pi",
    "reactions": "tools/reactions",
    "release": "platforms/mac/release",
    "remote": "gateway/remote",
    "remote-gateway-readme": "gateway/remote-gateway-readme",
    "reset": "cli/reset",
    "retry": "concepts/retry",
    "rpc": "reference/rpc",
    "sandbox": "cli/sandbox",
    "sandbox-vs-tool-policy-vs-elevated": "gateway/sandbox-vs-tool-policy-vs-elevated",
    "sandboxing": "gateway/sandboxing",
    "scripts": "help/scripts",
    "security": "cli/security",
    "session": "concepts/session",
    "session-management-compaction": "reference/session-management-compaction",
    "session-pruning": "concepts/session-pruning",
    "session-tool": "concepts/session-tool",
    "sessions": "concepts/sessions",
    "setup": "start/setup",
    "showcase": "start/showcase",
    "signal": "channels/signal",
    "signing": "platforms/mac/signing",
    "skills": "tools/skills",
    "skills-config": "tools/skills-config",
    "slack": "channels/slack",
    "slash-commands": "tools/slash-commands",
    "soul-evil": "hooks/soul-evil",
    "status": "cli/status",
    "streaming": "concepts/streaming",
    "strict-config": "refactor/strict-config",
    "subagents": "tools/subagents",
    "submitting-a-pr": "help/submitting-a-pr",
    "submitting-an-issue": "help/submitting-an-issue",
    "synthetic": "providers/synthetic",
    "system": "cli/system",
    "system-prompt": "concepts/system-prompt",
    "tailscale": "gateway/tailscale",
    "talk": "nodes/talk",
    "telegram": "channels/telegram",
    "test": "reference/test",
    "testing": "help/testing",
    "thinking": "tools/thinking",
    "timezone": "concepts/timezone",
    "tlon": "channels/tlon",
    "token-use": "reference/token-use",
    "tools-invoke-http-api": "gateway/tools-invoke-http-api",
    "transcript-hygiene": "reference/transcript-hygiene",
    "troubleshooting": "help/troubleshooting",
    "tui": "web/tui",
    "twitch": "channels/twitch",
    "typebox": "concepts/typebox",
    "typing-indicators": "concepts/typing-indicators",
    "uninstall": "install/uninstall",
    "update": "cli/update",
    "updating": "install/updating",
    "usage-tracking": "concepts/usage-tracking",
    "venice": "providers/venice",
    "vercel-ai-gateway": "providers/vercel-ai-gateway",
    "voice-call": "plugins/voice-call",
    "voice-overlay": "platforms/mac/voice-overlay",
    "voicecall": "cli/voicecall",
    "voicewake": "nodes/voicewake",
    "web": "tools/web",
    "webchat": "web/webchat",
    "webhook": "automation/webhook",
    "webhooks": "cli/webhooks",
    "whatsapp": "channels/whatsapp",
    "windows": "platforms/windows",
    "wizard": "start/wizard",
    "wizard-cli-automation": "start/wizard-cli-automation",
    "wizard-cli-reference": "start/wizard-cli-reference",
    "xiaomi": "providers/xiaomi",
    "xpc": "platforms/mac/xpc",
    "zai": "providers/zai",
    "zalo": "channels/zalo",
    "zalouser": "channels/zalouser",
}



# No custom homepage -- use the original OpenClaw index.md as-is


def _calc_prefix(page_path):
    """Calculate the correct ../ prefix for a given page source path.

    Accounts for:
    - MkDocs use_directory_urls (each non-index page gets an extra dir level)
    - Language-prefixed paths (ja/foo/bar.md -> links resolve within /ja/)
    """
    parts = page_path.replace("\\", "/").split("/")

    # Detect and strip language prefix
    if len(parts) > 1 and parts[0] in LANGUAGE_CODES:
        content_parts = parts[1:]
    else:
        content_parts = parts

    # Split into directory components and filename
    filename = content_parts[-1]
    dirs = content_parts[:-1]

    # Calculate URL depth:
    # - index.md files are served at the directory level (no extra depth)
    # - other .md files get an extra directory level from use_directory_urls
    if filename == "index.md":
        url_depth = len(dirs)
    else:
        url_depth = len(dirs) + 1

    if url_depth == 0:
        return "./"
    return "../" * url_depth


def _is_homepage(page_path):
    """Check if this is a root index.md or a language root index.md."""
    parts = page_path.replace("\\", "/").split("/")

    # Root index.md
    if parts == ["index.md"]:
        return True

    # Language root: ja/index.md, es/index.md, etc.
    if len(parts) == 2 and parts[0] in LANGUAGE_CODES and parts[1] == "index.md":
        return True

    return False


def _expand_slug(path):
    """Expand a Mintlify slug to its full path if it's a bare slug.

    /showcase           -> /start/showcase  (slug-only, expand)
    /start/showcase     -> /start/showcase  (already has dir, keep)
    /assets/foo.png     -> /assets/foo.png  (asset, keep)
    /images/bar.jpg     -> /images/bar.jpg  (asset, keep)
    """
    # Strip leading slash for lookup
    stripped = path.lstrip("/")

    # Don't touch paths that already contain a directory separator
    # (they're already full paths, not bare slugs)
    if "/" in stripped:
        return path

    # Don't touch fragment-only or empty
    if not stripped or stripped.startswith("#"):
        return path

    # Look up in slug map
    if stripped in SLUG_MAP:
        return "/" + SLUG_MAP[stripped]

    # Not found — return as-is (could be a valid top-level file like
    # index.md, vps.md, etc.)
    return path


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Rewrite absolute paths to relative paths, and replace homepage."""

    page_path = page.file.src_path

    # Calculate the correct relative prefix for this page
    prefix = _calc_prefix(page_path)

    # ── Phase 1: Expand Mintlify slug-only links to full paths ──
    # Match [text](/slug) and [text](/slug#anchor) — only bare slugs (no /)
    def expand_md_link(m):
        path = m.group(1)
        rest = m.group(2) or ""
        expanded = _expand_slug("/" + path)
        return "]({}{}".format(expanded, rest)

    # Expand slug-only links: ](/slug) or ](/slug#anchor) or ](/slug "title")
    # This matches the path after ]( up to the first ), #, space, or "
    markdown = re.sub(
        r'\]\(/([a-zA-Z0-9._-]+)((?:#[^)]*)?(?:\s+"[^"]*")?)\)',
        lambda m: "]({}{})" .format(
            _expand_slug("/" + m.group(1)),
            m.group(2) or "",
        ),
        markdown,
    )

    # Expand href="/slug" — bare slugs in HTML attributes
    markdown = re.sub(
        r'href="/([a-zA-Z0-9._-]+)((?:#[^"]*)?)"',
        lambda m: 'href="{}{}\"'.format(
            _expand_slug("/" + m.group(1)),
            m.group(2) or "",
        ),
        markdown,
    )

    # ── Phase 2: Rewrite all absolute paths to relative ──

    # Rewrite src="/assets/..." and src="/images/..."
    markdown = re.sub(
        r'src="/assets/',
        'src="{}assets/'.format(prefix),
        markdown,
    )
    markdown = re.sub(
        r'src="/images/',
        'src="{}images/'.format(prefix),
        markdown,
    )

    # Rewrite markdown image syntax ![alt](/assets/...) and ![alt](/images/...)
    markdown = re.sub(
        r'\]\(/assets/',
        ']({prefix}assets/'.format(prefix=prefix),
        markdown,
    )
    markdown = re.sub(
        r'\]\(/images/',
        ']({prefix}images/'.format(prefix=prefix),
        markdown,
    )

    # Rewrite absolute internal doc links: [text](/some/path) -> [text](prefix/some/path)
    # Matches ](/path but NOT ](// or ](http or ](# or ](mailto:
    markdown = re.sub(
        r'\]\(/(?!/)(?!http)(?!#)(?!mailto:)',
        ']({}'.format(prefix),
        markdown,
    )

    # Rewrite href="/path" in HTML tags (same logic)
    markdown = re.sub(
        r'href="/(?!/)(?!http)(?!#)(?!mailto:)',
        'href="{}'.format(prefix),
        markdown,
    )

    return markdown
