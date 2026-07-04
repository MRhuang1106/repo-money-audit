# Repo Money Audit

Repo Money Audit is a small CLI that checks whether a GitHub repository is ready to earn trust, users, sponsors, and consulting leads.

Most developers publish useful code and then lose potential users because the repository does not explain the problem, show a demo, provide install steps, or expose a support path. This tool gives a fast score and a practical checklist.

## Install

```bash
pipx install repo-money-audit
```

For local development:

```bash
git clone https://github.com/YOUR_NAME/repo-money-audit.git
cd repo-money-audit
python -m repo_money_audit .
```

## Usage

Audit the current repository:

```bash
repo-money-audit .
```

Audit another repository:

```bash
repo-money-audit ../my-project
```

Get JSON output for automation:

```bash
repo-money-audit . --json
```

Example output:

```text
Repo Money Audit: 72/100 (B)

Passed:
  + README exists
  + Install or setup instructions
  + License

Next fixes:
  - Funding link: Add .github/FUNDING.yml with GitHub Sponsors, Polar, Ko-fi, or custom support links.
  - Demo media or screenshots: Add a screenshot, GIF, hosted demo, or short terminal recording.
```

## What It Checks

- README quality
- Clear problem statement
- Install and usage instructions
- Demo media or screenshots
- License
- Funding links
- CI workflow or CI template
- Tests
- Issue templates
- Contribution guide
- Security policy
- Changelog
- Package keywords

## Monetization Use Cases

This project can be used as:

- A free open-source tool that attracts developers to your GitHub profile.
- A lead magnet for paid repository cleanup, README writing, GitHub Actions setup, or open-source launch consulting.
- A base for a paid "repository growth report" service.
- A GitHub Action or SaaS dashboard in a later version.

## Roadmap

- GitHub Action mode
- Markdown report export
- Profile README audit
- Sponsor copy generator
- Language-specific checks for Python, Node, Go, and Rust projects

## Support

If this tool saves you time, consider sponsoring the maintainer or requesting a paid repository review.
