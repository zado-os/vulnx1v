# Contributors

## Project owner (sole maintainer)

| Name | GitHub | Role |
|------|--------|------|
| **Hussain Al-zadjali** | [@zado-os](https://github.com/zado-os) | Author, maintainer, ZADO-OS Roger OS |

## Not a contributor

**Cursor Agent** (`@cursoragent`) must **not** appear as a project contributor.  
If it shows on GitHub, that comes from the **Cursor IDE** adding a `Co-authored-by: Cursor Agent` trailer when commits are pushed from the editor — not from this repository’s git history (all commits here use `zado-os <hussainzado@gmail.com>`).

### Remove Cursor Agent from GitHub Contributors

1. In **Cursor**: Settings → Features → Git → disable **“Include co-author in commits”** (or similar).
2. On **GitHub**: only make commits from your machine with:
   ```bash
   git config user.name "zado-os"
   git config user.email "hussainzado@gmail.com"
   ```
3. Future pushes should be only from Kali/terminal or Cursor with co-author **off**.
4. GitHub’s contributor graph updates after new commits without the Cursor co-author trailer.

## Upstream credit

[Anouar Ben Saad — VulnX](https://github.com/anouarbensaad/vulnx) — original codebase.
