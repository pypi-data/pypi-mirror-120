# stag

Deadly simple, extensible static site generator.

# Features

- Markdown support
- Jinja2 templates support
- Everything is a plugin
  - easy extensibility with plugins; all built-in plugins can be enabled,
    disabled, reordered or mixed with custom user plugins
  - plugins are either readers, generators or writers and are called in that
    order
- generate nice urls:
  - _foo/index.md_ → _foo/index.html_
  - _bar.md_ → _bar/index.html_
