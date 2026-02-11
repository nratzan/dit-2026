"""Generate pre-computed embeddings for the DIT framework.

Run once with OPENAI_API_KEY set:
    cd assessment
    python scripts/generate_embeddings.py

Reads markdown from ../v-0.0.1/ (the repo's versioned content).
Outputs:
    data/embeddings/embeddings.npy   (N x 3072 float32)
    data/embeddings/manifest.json    (chunk metadata)
"""
import sys
from pathlib import Path
from dataclasses import asdict

# Add package root to path
pkg_root = Path(__file__).parent.parent
sys.path.insert(0, str(pkg_root))

from dotenv import load_dotenv
load_dotenv(pkg_root / ".env")

from embeddings.chunker import MarkdownChunker
from embeddings.generator import get_embeddings, save_embeddings
from config import settings


def main():
    print(f"Source dir: {settings.source_dir}")
    print(f"Output dir: {settings.embeddings_dir}")

    # 1. Chunk all source markdown files
    chunker = MarkdownChunker()
    chunks = chunker.chunk_all(settings.source_dir)
    print(f"Chunked into {len(chunks)} chunks")
    for c in chunks[:3]:
        title = c.section_title.encode('ascii', 'replace').decode('ascii')
        print(f"  [{c.chunk_id}] {c.source_file} / {title} ({c.token_count} tokens)")

    # 2. Prepare texts and manifest
    texts = [c.text for c in chunks]
    manifest = [asdict(c) for c in chunks]

    # 3. Generate embeddings
    print(f"\nGenerating embeddings for {len(texts)} chunks...")
    embeddings = get_embeddings(texts)

    # 4. Save
    save_embeddings(embeddings, manifest, settings.embeddings_dir)
    print(f"\nDone! Embeddings saved to {settings.embeddings_dir}")


if __name__ == "__main__":
    main()
