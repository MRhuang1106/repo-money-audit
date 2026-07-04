from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    points: int
    passed: bool
    fix: str


def read_text(root: Path, *parts: str) -> str:
    file = root.joinpath(*parts)
    if not file.exists() or not file.is_file():
        return ""
    return file.read_text(encoding="utf-8", errors="replace")


def exists(root: Path, *parts: str) -> bool:
    return root.joinpath(*parts).exists()


def list_files(root: Path, *parts: str) -> list[Path]:
    directory = root.joinpath(*parts)
    if not directory.exists() or not directory.is_dir():
        return []
    return [item for item in directory.iterdir() if item.is_file()]


def has_any_file(root: Path, names: list[str]) -> bool:
    return any(exists(root, name) for name in names)


def includes_any(text: str, words: list[str]) -> bool:
    lower = text.lower()
    return any(word.lower() in lower for word in words)


def word_count(text: str) -> int:
    return len([word for word in text.strip().split() if word])


def audit(root: Path) -> dict:
    readme_names = ["README.md", "readme.md", "Readme.md"]
    readme_name = next((name for name in readme_names if exists(root, name)), None)
    readme = read_text(root, readme_name) if readme_name else ""
    pyproject = read_text(root, "pyproject.toml")
    package_json = read_text(root, "package.json")

    license_exists = has_any_file(root, ["LICENSE", "LICENSE.md", "COPYING"])
    funding_exists = exists(root, ".github", "FUNDING.yml") or exists(root, ".github", "FUNDING.yaml")
    workflows = len(list_files(root, ".github", "workflows"))
    issue_templates = len(list_files(root, ".github", "ISSUE_TEMPLATE"))
    tests_exist = has_any_file(root, ["test", "tests", "__tests__"]) or includes_any(package_json, ['"test"'])

    checks = [
        Check(
            "README exists",
            12,
            bool(readme_name),
            "Add a README with the problem, install steps, usage examples, and support links.",
        ),
        Check(
            "README is substantial",
            8,
            word_count(readme) >= 180,
            "Expand the README to at least 180 words with real examples and expected output.",
        ),
        Check(
            "Clear problem statement",
            8,
            includes_any(readme, ["why", "problem", "use case", "for developers", "helps"]),
            "Explain who the project helps and what pain it removes.",
        ),
        Check(
            "Install or setup instructions",
            10,
            includes_any(readme, ["install", "pip", "python", "docker", "setup", "quick start"]),
            "Add a copy-paste install or quick start section.",
        ),
        Check(
            "Usage examples",
            10,
            includes_any(readme, ["usage", "example", "command", "api"]),
            "Show at least one command or code example with sample output.",
        ),
        Check(
            "Demo media or screenshots",
            8,
            includes_any(readme, ["demo", "screenshot", "gif", "video", "try it"]),
            "Add a screenshot, GIF, hosted demo, or short terminal recording.",
        ),
        Check(
            "License",
            8,
            license_exists,
            "Add a license file so companies know how they can use the project.",
        ),
        Check(
            "Funding link",
            8,
            funding_exists,
            "Add .github/FUNDING.yml with GitHub Sponsors, Polar, Ko-fi, or custom support links.",
        ),
        Check(
            "CI workflow",
            7,
            workflows > 0,
            "Add a GitHub Actions workflow that runs tests or lint checks.",
        ),
        Check(
            "Tests",
            7,
            tests_exist,
            "Add a minimal test script or examples that can run in CI.",
        ),
        Check(
            "Issue templates",
            5,
            issue_templates > 0,
            "Add issue templates for bug reports and paid support requests.",
        ),
        Check(
            "Contribution guide",
            4,
            has_any_file(root, ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"]),
            "Add CONTRIBUTING.md to make collaboration easier.",
        ),
        Check(
            "Security policy",
            3,
            has_any_file(root, ["SECURITY.md", ".github/SECURITY.md"]),
            "Add SECURITY.md if users may run this in production or with private data.",
        ),
        Check(
            "Changelog",
            1,
            has_any_file(root, ["CHANGELOG.md", "CHANGES.md"]),
            "Add CHANGELOG.md so users can track improvements.",
        ),
        Check(
            "Package keywords or classifiers",
            1,
            includes_any(pyproject + package_json, ["keywords", "classifiers"]),
            "Add package keywords or Python classifiers for discoverability.",
        ),
    ]

    score = sum(check.points for check in checks if check.passed)
    max_score = sum(check.points for check in checks)
    if score >= 85:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    elif score >= 40:
        grade = "D"
    else:
        grade = "F"

    return {
        "repository": str(root),
        "score": score,
        "maxScore": max_score,
        "grade": grade,
        "passed": [check.name for check in checks if check.passed],
        "missing": [
            {"name": check.name, "fix": check.fix}
            for check in checks
            if not check.passed
        ],
    }


def print_text(result: dict) -> None:
    print(f"Repo Money Audit: {result['score']}/{result['maxScore']} ({result['grade']})")
    print()
    print("Passed:")
    for name in result["passed"]:
        print(f"  + {name}")
    print()
    print("Next fixes:")
    for item in result["missing"][:7]:
        print(f"  - {item['name']}: {item['fix']}")
    if len(result["missing"]) > 7:
        print(f"  - {len(result['missing']) - 7} more fixes hidden. Run with --json for full output.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a GitHub repository for monetization readiness.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    result = audit(root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
