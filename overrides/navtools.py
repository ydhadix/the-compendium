"""Shared navigation helpers for the custom mega-menu and the left ToC.

This is the single place the nav "rules" live, so the templates stay dumb.

on_nav annotates every Section with:
    section.index_page      its own index page (its index.md), or None. The section
                            title links here, and this page is never listed as a
                            child entry.
    section.has_subsection  True if any child is itself a Section.

on_nav also tags separators. A nav entry whose target is the sentinel "sep:" (a
harmless external-link value that passes a --strict build, e.g.
`- "---": "sep:"`) is marked for the templates:
    item.is_separator       True for a sentinel entry
    item.separator_label    None for a divider whose title is only dashes (a plain
                            rule); otherwise the title text, for a labelled divider

on_page_context exposes, for the left ToC:
    localnav_host           the hub nav page whose out-of-nav leaves to list, or
                            None. On an out-of-nav leaf this is its owning nav
                            page (one dir up); on a hub's own index page it is
                            that hub itself.
    localnav_chain          [host, host.parent, ... top-level section], or []
                            (set only for out-of-nav leaves; nav pages get the
                            active path from mkdocs)
    localnav_siblings       the host's out-of-nav leaf pages, sorted by title,
                            or []
so the left ToC can list a hub's out-of-nav leaves one level below it. On a
leaf page the current leaf is highlighted alongside its siblings; on the hub's
own index page all of its leaves are listed (the hub link itself stays active).
"""


import os

SEPARATOR_URL = "sep:"      # nav sentinel target marking a divider (see mkdocs.yml)
_DASHES = set("-—–─")       # a title of only these is a plain rule, with no label

# Banner pool: the client picks one of these at random on load (see banner.js),
# falling back to BANNER_FALLBACK. Enumerated at build time so adding/removing a
# file in docs/images/banners/ needs no code change.
BANNER_SUBDIR = ("images", "banners")
BANNER_FALLBACK = "campaign/odyssey.png"
_BANNER_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def on_config(config):
    """List the banner images into config.extra so the template (which always
    has `config`) can embed them for the client; see banner.js."""
    path = os.path.join(config["docs_dir"], *BANNER_SUBDIR)
    try:
        names = sorted(
            f for f in os.listdir(path) if f.lower().endswith(_BANNER_EXTS)
        )
    except OSError:
        names = []
    config["extra"]["banners"] = names
    config["extra"]["banner_fallback"] = BANNER_FALLBACK
    return config


def _annotate(items):
    for item in items:
        if getattr(item, "is_section", False):
            item.index_page = next(
                (c for c in item.children
                 if getattr(c, "is_page", False) and c.is_index),
                None,
            )
            item.has_subsection = any(
                getattr(c, "is_section", False) for c in item.children
            )
            _annotate(item.children)


def _annotate_separators(items):
    """Tag every item with is_separator, and separator_label for the ones that are.
    A title of only dashes is a plain rule (label None); any other title is a
    labelled divider carrying that text."""
    for item in items:
        item.is_separator = (getattr(item, "is_link", False)
                             and getattr(item, "url", None) == SEPARATOR_URL)
        if item.is_separator:
            label = (item.title or "").strip()
            item.separator_label = None if label and set(label) <= _DASHES else label
        elif getattr(item, "is_section", False):
            _annotate_separators(item.children)


def _leaf_title(page, config):
    """Title for an out-of-nav page. Out-of-nav pages aren't read during nav
    building, so populate the title ourselves (MkDocs' own logic: front-matter
    `title:`, else the first H1, else a humanised filename). Cached on the page,
    so the later page build reuses it."""
    if page.title is None:
        try:
            page.read_source(config)
        except OSError:
            pass
    return page.title or page.file.name.replace("-", " ").title()


def _index_leaf_children(nav, config, files):
    """Map every hub url -> its out-of-nav leaf pages, sorted by title.

    A leaf page is any documentation page absent from the nav (see `not_in_nav`
    in mkdocs.yml); its hub is the nav page one directory up. Stored on config so
    on_page_context can hand the right slice to the template."""
    nav_urls = {p.url for p in nav.pages}
    hubs = {}
    for file in files.documentation_pages():
        page = file.page
        if page is None or page.url in nav_urls:
            continue
        hub_url = _parent_url(page.url)
        if hub_url:
            hubs.setdefault(hub_url, []).append(page)
    for pages in hubs.values():
        pages.sort(key=lambda p: _leaf_title(p, config).lower())
    config["_leaf_children"] = hubs


def on_nav(nav, config, files):
    _annotate(nav.items)
    _annotate_separators(nav.items)
    _index_leaf_children(nav, config, files)
    return nav


def _parent_url(url):
    trimmed = url.rstrip("/")
    if "/" not in trimmed:
        return None
    return trimmed.rsplit("/", 1)[0] + "/"


def on_page_context(context, page, config, nav):
    context["localnav_host"] = None
    context["localnav_chain"] = []
    context["localnav_siblings"] = []

    nav_pages = {p.url: p for p in nav.pages}
    leaf_children = config.get("_leaf_children", {})

    if page.url in nav_pages:
        # Already in the nav; mkdocs marks the active path. But if this page is
        # itself a hub for out-of-nav leaf pages, expose them so the left ToC
        # lists its children one level down — the same way a section's index
        # page shows its children. The hub link stays highlighted via mkdocs'
        # active flag, so no leaf here is the current page.
        children = leaf_children.get(page.url)
        if children:
            context["localnav_host"] = nav_pages[page.url]
            context["localnav_siblings"] = children
        return context

    parent_url = _parent_url(page.url)
    host = nav_pages.get(parent_url) if parent_url else None
    if host is None:
        return context

    chain = []
    node = host
    while node is not None:
        chain.append(node)
        node = node.parent

    context["localnav_host"] = host
    context["localnav_chain"] = chain
    context["localnav_siblings"] = leaf_children.get(parent_url, [])
    return context
