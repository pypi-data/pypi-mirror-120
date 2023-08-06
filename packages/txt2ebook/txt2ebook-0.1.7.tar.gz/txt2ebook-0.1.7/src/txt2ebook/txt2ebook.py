# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path

import cchardet
import click
from bs4 import UnicodeDammit
from ebooklib import epub

from txt2ebook import __version__

logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--title",
    "-t",
    default=None,
    show_default=True,
    help="Set the title of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default="en",
    show_default=True,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    show_default=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--cover",
    "-c",
    type=click.Path(exists=True),
    default=None,
    show_default=True,
    help="Set the cover of the ebook.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value=logging.DEBUG,
    show_default=True,
    help="Enable debugging log.",
)
@click.option(
    "--no-backup",
    "-nb",
    is_flag=True,
    flag_value=True,
    show_default=True,
    help="Do not backup source txt file.",
)
@click.option(
    "--remove_wrapping",
    "-rw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--delete-regex",
    "-dr",
    multiple=True,
    help="Regex to delete word or phrase.",
)
@click.option(
    "--replace-regex",
    "-rr",
    nargs=2,
    multiple=True,
    help="Regex to replace word or phrase.",
)
@click.option(
    "--delete-line-regex",
    "-dlr",
    multiple=True,
    help="Regex to delete whole line.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
@click.pass_context
def main(ctx, **kwargs):
    """
    Console tool to convert txt file to different ebook format.
    """
    logging.basicConfig(
        level=kwargs["debug"] or logging.INFO,
        format="[%(levelname).1s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ctx.obj = kwargs

    try:
        filename = Path(kwargs["filename"])
        title = kwargs["title"]

        logger.info("Processing txt file: '%s'.", filename.resolve())

        with open(filename, "rb") as file:
            unicode = UnicodeDammit(file.read())
            logger.info("Encoding detected: '%s'.", unicode.original_encoding)
            content = unicode.unicode_markup

            if not content:
                raise RuntimeError(f"Empty file content in '{filename}'!")

            content = tidy_content(content)
            chapters = parse_content(content)

        ctx.obj["title"] = ctx.obj["title"] or find_book_title(content)
        output_filename = ctx.obj["title"] or Path(filename).stem

        if not ctx.obj["author"]:
            match = re.search(r"作者：(.*)", content)
            if match:
                author = match.group(1)
                ctx.obj["author"] = author

        build_txt(filename, content, kwargs["no_backup"])
        if chapters:
            build_epub(output_filename, chapters)

    except RuntimeError as error:
        click.echo(f"[E] {str(error)}!", err=True)


def find_book_title(content):
    """
    Extract book title from the content of the txt file.
    """
    regex = r"书名：(.*)|【(.*)】|《(.*)》"
    match = re.search(regex, content)
    if match:
        book_title = next(
            (title for title in match.groups() if title is not None)
        )
        logger.info("Found book title: '%s'.", book_title)
    else:
        book_title = False
        logger.info("No book title found from file!")
    return book_title


@click.pass_obj
def tidy_content(ctx, content):
    """
    Tidy content with incorrect wrapping which can affect chapters splitting
    and other opinionated changes.
    """
    # Remove words/phrases based on regex.
    for delete_regex in ctx["delete_regex"]:
        content = re.sub(
            re.compile(rf"{delete_regex}", re.MULTILINE), "", content
        )

    # Replace words/phrases based on regex.
    for search, replace in ctx["replace_regex"]:
        content = re.sub(
            re.compile(rf"{search}", re.MULTILINE), rf"{replace}", content
        )

    # Delete whole line based on regex.
    for delete_line_regex in ctx["delete_line_regex"]:
        content = re.sub(
            re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
            "",
            content,
        )

    # Stick to one form of quotation punctuation.
    content = content.replace("“", "「").replace("”", "」")

    # Remove incorrect closing quotation line wrapping.
    content = re.sub(r"\s+」", "」\n\n", content)

    # # Remove spaces or tabs at beginning of line.
    # content = re.sub(re.compile(r"^[ \t]+", re.MULTILINE), "", content)

    # # Replace double spaces as single space.
    # content = content.replace("  ", " ")

    # # Replace extra space in paragraph.
    # content = re.sub(re.compile(r"(?<![章卷])　", re.MULTILINE), "", content)

    # Append space to chapter name and chapter title.
    pattern = re.compile(
        r"^((第[0-9零一二三四五六七八九十百千两]*[章卷]|楔子)(?!\s)[：-]?)(.*)$", re.MULTILINE
    )
    chapters = re.findall(pattern, content)
    for chapter in chapters:
        space = " "
        content = content.replace(
            f"{chapter[0]}{chapter[2]}", f"{chapter[1]}{space}{chapter[2]}", 1
        )

    # Remove duplicate chapter title.
    pattern = re.compile(rf"({chapter_regexs()})([\r?\n]+\1)$", re.MULTILINE)
    duplicates = re.findall(pattern, content)
    for duplicate in duplicates:
        content = content.replace(duplicate[1], "", 1)

    # # Single spacing.
    # lines = content.split("\n")
    # content = "\n\n".join([line.strip() for line in lines if line])

    # Remove wrapping. Paragraph should be in one line.
    if ctx["remove_wrapping"]:
        unwrapped_content = ""
        for line in content.split("\n\n"):
            # if a line contains more opening quote(「) than closing quote(」),
            # we're still within the same paragraph.
            # e.g.:
            # 「...」「...
            # 「...
            if line.count("「") > line.count("」"):
                unwrapped_content = unwrapped_content + line.strip()
            elif (
                re.search(r"[…。？！]{1}」?$", line)
                or re.search(r"」$", line)
                or re.match(r"^[ \t]*……[ \t]*$", line)
                or re.match(r"^「」$", line)
                or re.match(r".*[》：＊\*]$", line)
                or re.match(r".*[a-zA-Z0-9]$", line)
            ):
                unwrapped_content = unwrapped_content + line.strip() + "\n\n"
            elif re.match(chapter_regexs(), line):
                # replace full-width space with half-wdith space.
                # looks nicer on the output.
                header = line.replace("\u3000\u3000", " ").replace(
                    "\u3000", " "
                )
                unwrapped_content = (
                    unwrapped_content + "\n\n" + header.strip() + "\n\n"
                )
            else:
                unwrapped_content = unwrapped_content + line.strip()
    else:
        unwrapped_content = content

    return unwrapped_content


def parse_content(content):
    """
    Parse the content into volumes (if exists) and chapters.
    """

    volume_regex = "^[ \t]*第[0-9一二三四五六七八九十]*[集卷册][^。~\n]*$"
    volume_pattern = re.compile(rf"{volume_regex}", re.MULTILINE)
    volume_headers = re.findall(volume_pattern, content)

    if not volume_headers:
        logger.info("Parsed 0 volumes.")
        parsed_content = parse_chapters(content)
        if parsed_content:
            logger.info("Parsed %s chapters.", len(parsed_content))
        else:
            logger.error("Parsed 0 chapters.")
    else:
        logger.info("Parsed %s volumes.", len(volume_headers))
        volume_bodies = re.split(volume_pattern, content)
        volumes = list(zip(volume_headers, volume_bodies[1:]))

        parsed_content = []
        for volume_header, body in volumes:
            parsed_body = parse_chapters(body)
            if parsed_body:
                parsed_content.append((volume_header, parsed_body))
            else:
                logger.error(
                    "Parsed 0 chapters for volume: '%s'.", volume_header
                )

    return parsed_content


def parse_chapters(content):
    """
    Split the content of txt file into chapters by chapter header.
    """
    chapter_regex = chapter_regexs()
    chapter_pattern = re.compile(rf"{chapter_regex}", re.MULTILINE)
    chapter_headers = re.findall(chapter_pattern, content)

    if not chapter_headers:
        return False
    else:
        bodies = re.split(chapter_pattern, content)
        chapters = list(zip(chapter_headers, bodies[1:]))

        return chapters


def chapter_regexs():
    """
    Regex rules for chapter headers.
    """
    regexs = (
        "^[ \t]*第[.0-9零一二三四五六七八九十百千两]*[章篇折][^。~\n]*$",
        "^[ \t]*[楔引]子.*$",
        "^[ \t]*序[章幕曲]?.*$",
        "^[ \t]*前言.*$",
        "^[ \t]*[内容]*简介.*$",
        "^[ \t]*[号番]外篇.*$",
        "^[ \t]*尾声$",
    )
    return "|".join(regexs)


def build_txt(filename, parsed_content, no_backup):
    """
    Generate txt from parsed content from original txt file.
    """
    txt_filename = Path(filename)

    if not no_backup:
        ymd_hms = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = Path(
            txt_filename.resolve().parent.joinpath(
                txt_filename.stem + "_" + ymd_hms + ".bak.txt"
            )
        )
        os.rename(txt_filename, backup_filename)
        logger.info("Backup txt file: '%s'.", backup_filename)

    with open(txt_filename, "w") as file:
        file.write(parsed_content)
        logger.info("Overwrite txt file: '%s'.", txt_filename.resolve())


@click.pass_obj
def build_epub(ctx, output_filename, parsed_content):
    """
    Generate epub from the parsed chapters from txt file.
    """

    book = epub.EpubBook()

    if ctx["title"]:
        book.set_title(ctx["title"])

    if ctx["language"]:
        book.set_language(ctx["language"])

    if ctx["author"]:
        book.add_author(ctx["author"])

    if ctx["cover"]:
        book.set_cover("cover.jpg", open(ctx["cover"], "rb").read())
        book.spine += ["cover"]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine += ["nav"]
    for header, body in parsed_content:
        if isinstance(body, list):
            logger.debug(header)
            html_chapters = []
            for chapter_title, chapter_body in body:
                html_chapter = build_html_chapter(
                    chapter_title, chapter_body, header
                )
                book.add_item(html_chapter)
                book.spine += [html_chapter]
                html_chapters.append(html_chapter)
            book.toc += [(epub.Section(header), html_chapters)]
        else:
            html_chapter = build_html_chapter(header, body)
            book.add_item(html_chapter)
            book.spine += [html_chapter]
            book.toc += [html_chapter]

    logger.info("Generating epub file: '%s'.", output_filename + ".epub")
    epub.write_epub(output_filename + ".epub", book, {})


def build_html_chapter(title, body, volume=None):
    """
    Generates the whole chapter to HTML.
    """
    if volume:
        filename = f"{volume}_{title}"
        logger.debug(f"  {title}")
    else:
        filename = title
        logger.debug(title)

    filename = filename.replace(" ", "_")

    html = f"<h2>{title}</h2>"
    for paragraph in body.split("\n\n"):
        paragraph = paragraph.replace(" ", "").replace("\n", "")
        html = html + f"<p>{paragraph}</p>"

    return epub.EpubHtml(
        title=title,
        content=html,
        file_name=filename + ".xhtml",
    )


if __name__ == "__main__":
    main()
