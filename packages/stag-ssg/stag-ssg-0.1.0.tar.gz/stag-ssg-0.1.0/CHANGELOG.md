# Changelog

All notable changes to this stag will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2021-09-16

This is the initial release of stag.

### Added
- stag build subcommand to generate static website
- stag serve subcommand to generate static website and then serve it locally
  with a light HTTP server
- handling configuration in TOML format
- plugin-based architecture which allows endless extensibility
- support for Jinja themes
- support for static files
- support for input in Markdown with TOML front-matter
- support for "macros" (shortcodes)
- auto-generating taxonomies
