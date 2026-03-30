"""Generate SAN mirror documents from the canonical JSON manifests."""

from __future__ import annotations

import argparse

try:
    from scripts.san_shared import REPO_ROOT, generate_mirrors, load_bundle, write_text
except ImportError:  # pragma: no cover - script execution path
    from san_shared import REPO_ROOT, generate_mirrors, load_bundle, write_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any generated mirror is out of sync.")
    args = parser.parse_args()

    bundle = load_bundle()
    mirrors = generate_mirrors(bundle)
    drift: list[str] = []
    for path, expected in mirrors.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if args.check:
            if current != expected.rstrip() + "\n":
                drift.append(path.relative_to(REPO_ROOT).as_posix())
        else:
            write_text(path, expected)

    if args.check and drift:
        for item in drift:
            print(f"OUT_OF_SYNC {item}")
        return 1
    if args.check:
        print("SAN_MIRRORS_IN_SYNC")
    else:
        print(f"SAN_MIRRORS_UPDATED {len(mirrors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
