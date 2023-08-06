# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v0.1.7 - 2021-09-19
Added
- Detect the original encoding of txt file, convert, and save to utf-8
- Add `--cover` option to add cover image to ebook

Changed
- Revise logging message format
- Do not raise exception when no chapter header found
- Show indentation for chapter title in debugging message
- Match different chapter headers and line separator
- Replace full-width space with half-width space in chapter headers
- Generate HTML manually instead through Markdown
- Keep original txt file formatting except chapter header
- Refactor and use more ways to extract book title from txt file
- Relax chapter header regex rules

Fixed
- Fix paragraph wrapping of imbalance opening and closing quote
- Fix group match not working with replacing regex

## v0.1.6 - 2021-09-11
Changed
- Backup original txt file and overwrite with parsed content
- Include and refactor more chapter header regex

Added
- Add `--no-backup` option to skip backup the original txt file

## v0.1.5 - 2021-09-02
Added
- Add `--delete-regex` option to remove selected words or phrases from the file
  content
- Add `--replace-regex` option to replace selected words or phrases from the
  file content
- Add `--delete-line-regex` option to remove whole line from the file content
- Detect author name from file content
- Parse volumes and chapters correctly and generate nested toc

Fixed
- Fix incorrect chapter filename
- Fix missing title in Epub file
- Fix issues raised by Flake8 and PyLint
- Replace missing space between chapter header and chapter title

Changed
- Parse more different chapter headers
- Save HTML filename in Epub as chapter header and title
- Dump parsed txt file during debug mode
- Use only single quotation punctuation

## v0.1.4 - 2021-08-04
Added
- Add `--remove_wrapping` option to remove text wrapping in the body content of
  a chapter
- Capture the book title from the file if found and not explicitly set through
  `--title` option

Fixed
- Fix no paragraph separation for txt file without single-line spacing for
  markdown
- Fix issues raised by PyLint

Changed
- Parse more different chapter headers
- Refactor argument parsing

## v0.1.3 - 2021-07-24
Fixed
- Fix no parsing and split by introduction chapter
- Fix issues raised by PyLint

Changed
- Switch license to AGPL-3

## v0.1.2 - 2021-07-20
Added
- Add option to set metadata for ebook
- Add missing requirements.txt
- Show full help message when missing required argument

Changed
- Use better way to check for input file
- Print message using click.ecto
- Code formatting

## v0.1.1 - 2021-07-13

Added
- Enable logging for debugging and showing status
- Set log level through `LOG` environment variable

Fixed
- Check for missing filename, empty file content, and missing chapters

## v0.1.0 - 2021-07-08

Added
- Initial public release
- Support converting txt file in Chinese language into epub format
