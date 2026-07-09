#!/usr/bin/env python3
"""Generate MASO study-note files from a saved MASO exam index."""

from __future__ import annotations

import argparse
import html
import re
import ssl
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urlencode, urlparse, urlunparse


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "but",
    "for",
    "in",
    "it",
    "not",
    "of",
    "only",
    "or",
    "some",
    "the",
    "to",
}

CRUMB_ALIASES = {
    "Information and...": "Information and threats",
    "Personal aspect...": "Personal aspects of threats",
    "General": "general",
}

REASONING_TEMPLATE = [
    "我选了____<br>",
    "理由如下<br>",
    "排除：<br>",
    "1 错在____。<br>",
    "2 错在____。<br>",
    "3 错在____。<br>",
    "4 错在____。",
    "",
    "不确定：<br>",
    "我不确定____和____的区别。",
]


@dataclass
class Question:
    prompt: str
    options: list[str]
    answer_title: str = ""

    @property
    def answer_number(self) -> str:
        match = re.match(r"\s*(\d+)\.", self.answer_title)
        return match.group(1) if match else ""


@dataclass
class Material:
    html_path: Path | None
    material_id: int
    title: str
    breadcrumb: str
    questions: list[Question]


@dataclass
class IndexEntry:
    order: int
    theme_number: int | None
    item_number: int | None
    material_id: int
    title: str
    href: str
    theme: str
    subtopic: str

    @property
    def prefix(self) -> str | None:
        if self.theme_number is None or self.item_number is None:
            return None
        return f"{self.theme_number:02d}-{self.item_number}"

    @property
    def breadcrumb(self) -> str:
        if self.theme and self.subtopic:
            return f"{self.theme} > {self.subtopic} >> {self.title}"
        if self.theme:
            return f"{self.theme} >> {self.title}"
        return f"MASO Exam 1 >> {self.title}"


@dataclass
class TreeNode:
    text_chunks: list[str]
    href: str = ""
    link_chunks: list[str] | None = None
    children: list["TreeNode"] | None = None

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = []

    @property
    def label(self) -> str:
        if self.link_chunks is not None:
            return normalize_space("".join(self.link_chunks))
        return normalize_space("".join(self.text_chunks))


class IndexTreeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = TreeNode([])
        self.stack: list[TreeNode] = [self.root]
        self.in_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "li" and "puurivi" in attr.get("class", ""):
            node = TreeNode([])
            self.stack[-1].children.append(node)
            self.stack.append(node)
            return

        if tag == "a" and self.stack:
            href = attr.get("href", "")
            if "materiaali.php?id=" in href:
                self.stack[-1].href = href
                self.stack[-1].link_chunks = []
                self.in_link = True

    def handle_data(self, data: str) -> None:
        if not self.stack:
            return
        if self.in_link and self.stack[-1].link_chunks is not None:
            self.stack[-1].link_chunks.append(data)
        else:
            self.stack[-1].text_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self.in_link = False
        elif tag == "li" and len(self.stack) > 1:
            self.stack.pop()


class QuestionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.questions: list[Question] = []
        self.current: dict[str, object] | None = None
        self.in_strong = False
        self.strong_chunks: list[str] = []
        self.ol_depth = 0
        self.in_option = False
        self.option_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "li" and "tehtavarivi" in attr.get("class", ""):
            self.current = {
                "prompt": "",
                "options": [],
                "answer_title": attr.get("title", ""),
            }
            return

        if self.current is None:
            return

        if tag == "strong":
            self.in_strong = True
            self.strong_chunks = []
        elif tag == "ol":
            self.ol_depth += 1
        elif tag == "li" and self.ol_depth:
            self.in_option = True
            self.option_chunks = []

    def handle_data(self, data: str) -> None:
        if self.current is None:
            return
        if self.in_strong:
            self.strong_chunks.append(data)
        elif self.in_option:
            self.option_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return

        if tag == "strong" and self.in_strong:
            self.current["prompt"] = normalize_space("".join(self.strong_chunks))
            self.in_strong = False
            return

        if tag == "li" and self.in_option:
            options = self.current["options"]
            assert isinstance(options, list)
            options.append(normalize_space("".join(self.option_chunks)))
            self.in_option = False
            return

        if tag == "ol" and self.ol_depth:
            self.ol_depth -= 1
            return

        if tag == "li" and not self.ol_depth:
            prompt = str(self.current["prompt"])
            options = list(self.current["options"])
            answer_title = str(self.current["answer_title"])
            if prompt and options:
                self.questions.append(Question(prompt, options, answer_title))
            self.current = None


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def strip_tags(value: str) -> str:
    return normalize_space(re.sub(r"<[^>]+>", " ", value))


def slugify(value: str) -> str:
    words = re.findall(r"[a-z0-9]+", value.lower())
    return "_".join(word for word in words if word not in {"a", "an", "and", "the", "of"})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def material_id_from_href(href: str) -> int:
    query = parse_qs(urlparse(href).query)
    if "id" not in query:
        raise ValueError(f"Missing material id in href: {href}")
    return int(query["id"][0])


def question_url_from_material_url(href: str) -> str:
    parsed = urlparse(href)
    query = parse_qs(parsed.query)
    material_id = query.get("id", [""])[0]
    if not material_id:
        raise ValueError(f"Missing material id in href: {href}")
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            "/maso/oheismateriaali.php",
            "",
            urlencode({"id": material_id, "tyyppi": "tehtava"}),
            "",
        )
    )


def parse_questions_html(text: str) -> list[Question]:
    parser = QuestionParser()
    parser.feed(text)
    return parser.questions


def fetch_questions(entry: IndexEntry, timeout: int, insecure: bool) -> list[Question]:
    question_url = question_url_from_material_url(entry.href)
    request = urllib.request.Request(question_url, headers={"User-Agent": "maso-note-generator/1.0"})
    context = ssl._create_unverified_context() if insecure else None
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        text = response.read().decode(charset, errors="replace")
    return parse_questions_html(text)


def resolve_frame_path(main_html: Path, frame_name: str) -> Path:
    text = read_text(main_html)
    pattern = rf'<frame[^>]+name="{re.escape(frame_name)}"[^>]+src="([^"]+)"'
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Missing frame {frame_name!r} in {main_html}")
    src = unquote(html.unescape(match.group(1))).lstrip("./")
    return main_html.parent / src


def parse_material_id(text: str, path: Path) -> int:
    match = re.search(r"materiaali\.php\?id=(\d+)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"id=(\d+)", text)
    if match:
        return int(match.group(1))
    raise ValueError(f"Could not parse material id from {path}")


def parse_title(text: str, path: Path) -> str:
    match = re.search(r"<title>\s*MASO\s*\|\s*[0-9]+\s+(.+?)\s*</title>", text, flags=re.I | re.S)
    if match:
        return normalize_space(match.group(1))
    raise ValueError(f"Could not parse MASO title from {path}")


def parse_breadcrumb(text_html: str, fallback_title: str) -> str:
    match = re.search(r"<h3[^>]*>(.*?)</h3>", text_html, flags=re.I | re.S)
    if not match:
        return fallback_title

    h3_inner = match.group(1)
    small_match = re.search(r"<small[^>]*>(.*?)</small>", h3_inner, flags=re.I | re.S)
    title_part = re.sub(r"<small[^>]*>.*?</small>", "", h3_inner, flags=re.I | re.S)
    page_title = strip_tags(title_part) or fallback_title

    if not small_match:
        return page_title

    small_text = strip_tags(small_match.group(1)).strip("[] ")
    crumbs = [normalize_space(part) for part in small_text.split("<")]
    crumbs = [CRUMB_ALIASES.get(part, part) for part in crumbs if part]
    crumbs.reverse()

    if not crumbs:
        return page_title
    if len(crumbs) == 1:
        return f"{crumbs[0]} >> {page_title}"
    return f"{' > '.join(crumbs)} >> {page_title}"


def parse_saved_material(path: Path) -> Material:
    main_html = read_text(path)
    material_id = parse_material_id(main_html, path)
    title = parse_title(main_html, path)
    text_frame = resolve_frame_path(path, "fTeksti")
    question_frame = resolve_frame_path(path, "fOheismateriaali")
    breadcrumb = parse_breadcrumb(read_text(text_frame), title)
    questions = parse_questions_html(read_text(question_frame))
    return Material(path, material_id, title, breadcrumb, questions)


def find_material_pages(paths: Iterable[Path]) -> list[Path]:
    pages: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".html" and "MASO _" in path.name:
            pages.append(path)
            continue
        if path.is_dir():
            if path.name != "maso_html":
                pages.extend(
                    candidate
                    for html_dir in path.rglob("maso_html")
                    for candidate in html_dir.glob("MASO _*.html")
                )
            else:
                pages.extend(path.glob("MASO _*.html"))
    return sorted(set(pages))


def collect_material_nodes(node: TreeNode) -> list[TreeNode]:
    collected: list[TreeNode] = []
    if node.href:
        collected.append(node)
    for child in node.children or []:
        collected.extend(collect_material_nodes(child))
    return collected


def parse_index_file(index_file: Path, include_self_evaluation: bool) -> list[IndexEntry]:
    parser = IndexTreeParser()
    parser.feed(read_text(index_file))

    entries: list[IndexEntry] = []
    order = 0
    theme_number = 0
    for top_node in parser.root.children or []:
        material_nodes = collect_material_nodes(top_node)
        material_nodes = [
            node
            for node in material_nodes
            if include_self_evaluation
            or not (material_id_from_href(node.href) == 700 or node.label.lower() == "self-evaluation")
        ]
        if not material_nodes:
            continue

        theme_number += 1
        item_number = 0
        for subtopic_node in top_node.children or []:
            for material_node in collect_material_nodes(subtopic_node):
                material_id = material_id_from_href(material_node.href)
                is_self_evaluation = material_id == 700 or material_node.label.lower() == "self-evaluation"
                if is_self_evaluation and not include_self_evaluation:
                    continue

                order += 1
                item_number += 1
                entries.append(
                    IndexEntry(
                        order=order,
                        theme_number=theme_number,
                        item_number=item_number,
                        material_id=material_id,
                        title=material_node.label,
                        href=material_node.href,
                        theme=top_node.label,
                        subtopic=subtopic_node.label,
                    )
                )
    return entries


def existing_note_for(output_dir: Path, prefix: str) -> Path | None:
    prefixed = sorted(output_dir.glob(f"{prefix}_*.md"))
    if len(prefixed) == 1:
        return prefixed[0]
    return None


def render_mcq(questions: list[Question], include_answers: bool) -> list[str]:
    lines: list[str] = ["# MCQ区"]
    if not questions:
        lines.append("TBC")
        return lines

    for number, question in enumerate(questions, start=1):
        lines.extend(["## Q" + str(number), question.prompt])
        for option in question.options:
            lines.append(f"1. {option}")
        lines.extend(["### 思路和正确答案", *REASONING_TEMPLATE, ""])

    answer_key = "".join(question.answer_number for question in questions)
    lines.extend(["", "## 答案", answer_key if include_answers else ""])
    return lines


def render_note(entry: IndexEntry, questions: list[Question], include_answers: bool) -> str:
    lines = [
        entry.breadcrumb,
        f"<!-- material_id: {entry.material_id} -->",
        f"<!-- source_url: {entry.href} -->",
        "# 笔记区",
        "TBC",
        "",
        "",
    ]
    lines.extend(render_mcq(questions, include_answers))
    lines.extend(["", "", "# 贡献区"])
    return "\n".join(lines).rstrip() + "\n"


def split_sections(content: str) -> tuple[str, str, str]:
    mcq_match = re.search(r"(?m)^# MCQ区\s*$", content)
    contribution_match = re.search(r"(?m)^# 贡献区\s*$", content)
    if not mcq_match or not contribution_match or mcq_match.start() > contribution_match.start():
        return content.rstrip(), "", ""
    before = content[: mcq_match.start()].rstrip()
    mcq = content[mcq_match.start() : contribution_match.start()].rstrip()
    after = content[contribution_match.start() :].rstrip()
    return before, mcq, after


def is_empty_mcq(mcq_section: str) -> bool:
    body = re.sub(r"(?m)^# MCQ区\s*", "", mcq_section).strip()
    body = re.sub(r"(?ms)^## 答案\s*.*$", "", body).strip()
    return body in {"", "TBC"}


def merge_existing_note(existing_content: str, questions: list[Question], include_answers: bool, replace_existing_mcq: bool) -> tuple[str, bool]:
    before, mcq, after = split_sections(existing_content)
    if not mcq:
        return existing_content, False
    if not replace_existing_mcq and not is_empty_mcq(mcq):
        return existing_content, False

    new_mcq = "\n".join(render_mcq(questions, include_answers)).rstrip()
    merged = "\n\n".join(part for part in [before, new_mcq, after] if part).rstrip() + "\n"
    return merged, merged != existing_content


def output_name(prefix: str, title: str) -> str:
    return f"{prefix}_{slugify(title)}.md"


def relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def write_manifest(index_file: Path, entries: list[IndexEntry], note_paths: dict[int, Path], materials: dict[int, Material], fetched_ids: set[int], manifest_path: Path, dry_run: bool) -> None:
    lines = [
        "# MASO Exam 1 Material Links",
        "",
        f"Source index: `{relative_path(index_file)}`",
        "",
        "| Theme | Item | ID | Theme title | Subtopic | Material | Note file | MCQ source | Link |",
        "|---:|---:|---:|---|---|---|---|---|---|",
    ]
    for entry in entries:
        note = note_paths.get(entry.material_id)
        note_text = f"`{relative_path(note)}`" if note else ""
        if entry.material_id in materials:
            mcq_source = "local"
        elif entry.material_id in fetched_ids:
            mcq_source = "remote"
        else:
            mcq_source = "missing"
        values = [
            str(entry.theme_number or "-"),
            str(entry.item_number or "-"),
            str(entry.material_id),
            entry.theme,
            entry.subtopic,
            entry.title,
            note_text,
            mcq_source,
            entry.href,
        ]
        escaped = [value.replace("|", "\\|") for value in values]
        lines.append("| " + " | ".join(escaped) + " |")

    content = "\n".join(lines).rstrip() + "\n"
    if dry_run:
        print(f"manifest: {manifest_path}")
    else:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(content, encoding="utf-8")
        print(f"manifest: {manifest_path}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate MASO Markdown notes from a saved MASO exam index.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[Path("maso")],
        type=Path,
        help="Index file or MASO root. Default uses maso/maso_exam1.html.",
    )
    parser.add_argument(
        "--index-file",
        type=Path,
        help="Saved MASO exam index file, for example maso/maso_exam1.html.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for generated Markdown notes. Default is maso/exam1_materials.",
    )
    parser.add_argument(
        "--saved-html-root",
        type=Path,
        help="Root containing any saved maso_html directories used to enrich notes with MCQs.",
    )
    parser.add_argument(
        "--fetch-remote",
        action="store_true",
        help="Fetch MCQ pages from the course site when local saved HTML is missing.",
    )
    parser.add_argument(
        "--fetch-timeout",
        type=int,
        default=20,
        help="Remote fetch timeout in seconds.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for remote fetches.",
    )
    parser.add_argument(
        "--include-self-evaluation",
        action="store_true",
        help="Also generate a note skeleton for material id 700 Self-evaluation.",
    )
    parser.add_argument(
        "--no-manifest",
        action="store_true",
        help="Do not write the material-link manifest.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Manifest path. Default is maso/exam1_material_links.md.",
    )
    parser.add_argument(
        "--include-answers",
        action="store_true",
        help="Fill the 答案 section with the hover/title answer key. Default keeps it blank.",
    )
    parser.add_argument(
        "--replace-existing-mcq",
        action="store_true",
        help="Replace non-empty MCQ sections in existing files. Default preserves them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files.",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    paths = [path.resolve() for path in args.paths]

    if args.index_file:
        index_file = args.index_file.resolve()
    else:
        first_path = paths[0] if paths else (Path.cwd() / "maso")
        index_file = first_path if first_path.is_file() else first_path / "maso_exam1.html"
    if not index_file.exists():
        print(f"No saved MASO exam index found: {index_file}")
        return 0

    maso_root = index_file.parent
    output_dir = args.output_dir.resolve() if args.output_dir else maso_root / "exam1_materials"
    saved_html_root = args.saved_html_root.resolve() if args.saved_html_root else maso_root
    manifest_path = args.manifest.resolve() if args.manifest else maso_root / "exam1_material_links.md"

    entries = parse_index_file(index_file, args.include_self_evaluation)
    material_pages = find_material_pages([saved_html_root])
    local_materials = {material.material_id: material for material in (parse_saved_material(path) for path in material_pages)}

    created = updated = preserved = failed = 0
    fetched_ids: set[int] = set()
    note_paths: dict[int, Path] = {}
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        prefix = entry.prefix
        if prefix is None:
            continue

        existing = existing_note_for(output_dir, prefix)
        output_path = existing or output_dir / output_name(prefix, entry.title)
        note_paths[entry.material_id] = output_path

        local_material = local_materials.get(entry.material_id)
        questions = local_material.questions if local_material else []
        if not questions and args.fetch_remote:
            try:
                questions = fetch_questions(entry, args.fetch_timeout, args.insecure)
                fetched_ids.add(entry.material_id)
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"fetch failed: {entry.material_id} {entry.title}: {exc}")

        if existing:
            existing_content = read_text(existing)
            new_content, changed = merge_existing_note(
                existing_content,
                questions,
                args.include_answers,
                args.replace_existing_mcq,
            )
            if not changed:
                print(f"preserve existing: {existing}")
                preserved += 1
                continue
            if args.dry_run:
                print(f"update MCQ: {existing}")
            else:
                existing.write_text(new_content, encoding="utf-8")
                print(f"update MCQ: {existing}")
            updated += 1
            continue

        content = render_note(entry, questions, args.include_answers)
        if args.dry_run:
            print(f"create: {output_path}")
        else:
            output_path.write_text(content, encoding="utf-8")
            print(f"create: {output_path}")
        created += 1

    if not args.no_manifest:
        write_manifest(index_file, entries, note_paths, local_materials, fetched_ids, manifest_path, args.dry_run)
    action_label = "planned" if args.dry_run else "done"
    print(
        f"Done ({action_label}). Materials: {len(entries)}; created: {created}; "
        f"updated: {updated}; preserved: {preserved}; fetch failed: {failed}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
