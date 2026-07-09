# MASO Exam 1 note generation

Use this to traverse the material links in `maso/maso_exam1.html` and generate Markdown study files in the same shape as the 0709 notes.

Naming rule:

- The first number is the top-level theme number in `maso_exam1.html`, excluding `Introduction / Self-evaluation`.
- The second number is the material order inside that theme.
- Example: `Repair and punishment` is under the third top-level theme, `Lost security`, so its file is `03-1_repair_punishment.md`.

```bash
python3 -B maso/tools/generate_maso_notes.py maso --output-dir maso/0709 --fetch-remote --insecure
```

Behavior:

- Reads course material links and hierarchy from `maso/maso_exam1.html`.
- Skips `Self-evaluation` by default.
- Creates material files like `01-3_not_only_breaking_ciphers.md` and `03-1_repair_punishment.md`.
- Keeps `# 笔记区`, `# MCQ区`, `## 答案`, and `# 贡献区` in the same study-note shape as the 0709 files.
- Does not overwrite existing notes by default.
- Uses any locally saved complete `maso_html` pages to fill MCQ questions automatically.
- With `--fetch-remote`, fetches missing MCQ question pages from the MASO course site.
- With `--insecure`, disables Python TLS verification when the course site's certificate chain is not trusted locally.
- Preserves non-empty existing MCQ sections unless `--replace-existing-mcq` is used.
- Leaves `## 答案` blank by default, so the generated file can be used before answering.
- Writes `maso/exam1_material_links.md` as the link manifest.
- Uses `<br>` inside the reasoning template to preserve Markdown hard line breaks without trailing spaces.

Useful options:

```bash
python3 -B maso/tools/generate_maso_notes.py maso --output-dir maso/0709 --fetch-remote --insecure --dry-run
python3 -B maso/tools/generate_maso_notes.py maso --output-dir maso/0709 --fetch-remote --insecure --include-answers
```

Important limitation: `maso/maso_exam1.html` contains links and titles, but not the MCQ text. Use `--fetch-remote` or save complete material HTML locally to fill MCQ sections.
