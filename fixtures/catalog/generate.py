#!/usr/bin/env python3
"""Generate silent .m4b fixture audiobooks for AudioBookShelf to scan.

Why silent and synthetic? We need realistic-looking catalog data (with
multi-axis tagging metadata, varied authors/titles, recognizable from our
Gherkin scenarios) but cannot ship real audio for license + repo-size reasons.
These fixtures are 30-second silent AAC streams with proper metadata.

Why Docker for ffmpeg? Avoids requiring a system ffmpeg install; matches the
project's cross-platform principle. Uses `mwader/static-ffmpeg` (~20MB,
static-linked).

Run: python fixtures/catalog/generate.py
     (or `just fixtures` once that recipe lands)

The resulting .m4b files are gitignored. Re-run after `git clean` or on a
fresh checkout.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent

# Tiny static-linked ffmpeg image. Pulled once per host.
FFMPEG_IMAGE = "mwader/static-ffmpeg:latest"
DURATION_SECONDS = 30
SAMPLE_RATE = 22050


@dataclass(frozen=True, slots=True)
class FixtureBook:
    title: str
    author: str
    narrator: str
    # Filesystem-safe path components (AudioBookShelf scans by directory).
    author_dir: str
    title_dir: str

    def path(self) -> Path:
        return FIXTURE_DIR / self.author_dir / self.title_dir / f"{self.title}.m4b"


BOOKS: list[FixtureBook] = [
    # Aligns with tests/features/kid_checks_out_book.feature.
    FixtureBook(
        title="The Wild Robot",
        author="Peter Brown",
        narrator="Kate Atwater",
        author_dir="Peter Brown",
        title_dir="The Wild Robot",
    ),
    FixtureBook(
        title="The Wild Robot Escapes",
        author="Peter Brown",
        narrator="Kate Atwater",
        author_dir="Peter Brown",
        title_dir="The Wild Robot Escapes",
    ),
    FixtureBook(
        title="Coraline",
        author="Neil Gaiman",
        narrator="Neil Gaiman",
        author_dir="Neil Gaiman",
        title_dir="Coraline",
    ),
    # A few more for variety.
    FixtureBook(
        title="Charlotte's Web",
        author="E.B. White",
        narrator="E.B. White",
        author_dir="E.B. White",
        title_dir="Charlotte's Web",
    ),
    FixtureBook(
        title="The Phantom Tollbooth",
        author="Norton Juster",
        narrator="David Hyde Pierce",
        author_dir="Norton Juster",
        title_dir="The Phantom Tollbooth",
    ),
    FixtureBook(
        title="Frog and Toad Are Friends",
        author="Arnold Lobel",
        narrator="Arnold Lobel",
        author_dir="Arnold Lobel",
        title_dir="Frog and Toad Are Friends",
    ),
]


def generate_one(book: FixtureBook) -> None:
    """Generate a single silent .m4b with metadata."""
    out_path = book.path()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists():
        print(f"  skip (exists): {out_path.relative_to(FIXTURE_DIR)}")
        return

    # ffmpeg writes inside the container; we mount the fixture dir to /work.
    container_path = f"/work/{out_path.relative_to(FIXTURE_DIR)}"
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{FIXTURE_DIR}:/work",
        FFMPEG_IMAGE,
        "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=channel_layout=mono:sample_rate={SAMPLE_RATE}",
        "-t", str(DURATION_SECONDS),
        "-c:a", "aac",
        "-b:a", "32k",
        "-metadata", f"title={book.title}",
        "-metadata", f"artist={book.author}",
        "-metadata", f"album={book.title}",
        "-metadata", f"composer={book.narrator}",
        "-metadata", f"album_artist={book.author}",
        container_path,
    ]
    print(f"  generating: {out_path.relative_to(FIXTURE_DIR)}")
    subprocess.run(cmd, check=True, capture_output=True)


def main() -> int:
    if not (FIXTURE_DIR / ".keep").exists():
        (FIXTURE_DIR / ".keep").touch()  # ensure dir survives `git clean`

    print(f"Generating {len(BOOKS)} fixture audiobooks via {FFMPEG_IMAGE}...")
    for book in BOOKS:
        generate_one(book)
    print("\nDone. Run `just dev` and AudioBookShelf will scan these on first boot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
