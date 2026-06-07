from pathlib import Path
import shutil
import json
import yaml


ROOT = Path(__file__).resolve().parent.parent

MD_DIR = ROOT / "md"
ASSETS_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"


def extract_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)

    if len(parts) < 3:
        return {}

    return yaml.safe_load(parts[1]) or {}


def build_index():
    articles = []

    for md_file in sorted(MD_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")

        frontmatter = extract_frontmatter(content)

        articles.append(
            {
                "file": str(
                    md_file.relative_to(ROOT)
                ).replace("\\", "/"),
                "slug": md_file.stem,
                "title": frontmatter.get("title"),
                "summary": frontmatter.get("summary"),
                "date": frontmatter.get("date"),
            }
        )
        print(frontmatter.get("date"))
    articles.sort(key=lambda x: x['date'])

    return articles


def main():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    DIST_DIR.mkdir(parents=True)

    if MD_DIR.exists():
        shutil.copytree(MD_DIR, DIST_DIR / "md")

    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, DIST_DIR / "assets")

    articles = build_index()

    with open(
        DIST_DIR / "file_list.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            articles,
            f,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    print(f"Generated {len(articles)} articles")


if __name__ == "__main__":
    main()