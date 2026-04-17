# 🏛️ XCGradient Infrastructure OS

This document serves as the "Source of Truth" for XC Gradient's standardized infrastructure.

## 🧱 Architectural Principles

XC Gradient's infrastructure is built on three core pillars:
1. **Single Source of Truth for Brand:** Branding assets must live in the `brand-assets` repository and be linked as submodules to builders to prevent drift.
2. **Standardized Execution (Docker):** Every internal tool must have a `Dockerfile`. If it can't run in a container, it isn't ready for production.
3. **Automated Reliability (CI/CD):** No code is merged to `main` without passing automated tests and linting.

## 📦 Repositories

| Repository | Purpose | Language | CI/CD |
|------------|---------|----------|-------|
| `brand-assets` | Logos, Colors, Fonts | - | - |
| `latex-builder`| Corporate Docs | TeX / Node | Docker (TexLive) |
| `pwp-builder` | Pitch Decks | Node | Docker (Alpine) |
| `xcg-bot` | Discord AI Ops | Python | Docker (Slim) |
| `hw-management`| Hardware Health | Python | Docker (Monitoring Tools) |

## 🐳 Container Registry (GHCR)

We use the [GitHub Container Registry](https://github.com/orgs/xcgradient-org/packages) to host our production images.

### Pulling Images

To run the latest version of any service without cloning the code:

```bash
docker pull ghcr.io/xcgradient-org/xcg-bot:latest
docker pull ghcr.io/xcgradient-org/pwp-builder:latest
```

### Authentication

If pulling from a private registry, authenticate your local Docker:

```bash
export CR_PAT=YOUR_GITHUB_TOKEN
echo $CR_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

## 🔗 Working with Git Submodules

Submodules are used for branding assets. When updating brand assets:

1. Update files in the `brand-assets/` folder.
2. Commit and push in the `brand-assets/` directory first.
3. Update the pointer in the builder repository:
   ```bash
   git submodule update --remote --merge
   git add brand-assets
   git commit -m "chore: update branding assets"
   ```

## ⚖️ Legal & Licensing

All infrastructure code is proprietary to XC Gradient. No unauthorized distribution is permitted.
