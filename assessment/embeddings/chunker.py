"""Markdown-aware chunker for DIT framework content."""
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import tiktoken

@dataclass
class Chunk:
    chunk_id: int
    source_file: str
    section_title: str
    heading_hierarchy: list
    text: str
    token_count: int
    sae_level: Optional[int] = None
    epias_stage: Optional[str] = None
    chunk_type: str = "prose"

class MarkdownChunker:
    MAX_TOKENS = 400
    MIN_TOKENS = 30

    def __init__(self):
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def chunk_all(self, source_dir: Path) -> list:
        """Chunk all markdown files in source directory."""
        chunks = []
        files = sorted(source_dir.glob("*.md"))
        chunk_id = 0
        for filepath in files:
            file_chunks = self._chunk_file(filepath, chunk_id)
            chunks.extend(file_chunks)
            chunk_id += len(file_chunks)
        return chunks

    def _chunk_file(self, filepath: Path, start_id: int) -> list:
        """Chunk a single markdown file."""
        text = filepath.read_text(encoding="utf-8")
        sections = self._split_by_headings(text)

        chunks = []
        for hierarchy, content in sections:
            if not content.strip():
                continue

            section_title = hierarchy[-1] if hierarchy else filepath.stem
            sae_level = self._extract_sae_level(" ".join(hierarchy))
            epias_stage = self._extract_epias_stage(" ".join(hierarchy))
            chunk_type = "table" if "|" in content and content.count("|") > 4 else "prose"

            # Split large sections into sub-chunks
            sub_texts = self._split_to_size(content)
            for sub_text in sub_texts:
                token_count = self._count_tokens(sub_text)
                if token_count < self.MIN_TOKENS:
                    continue
                chunks.append(Chunk(
                    chunk_id=start_id + len(chunks),
                    source_file=filepath.name,
                    section_title=section_title,
                    heading_hierarchy=hierarchy,
                    text=sub_text.strip(),
                    token_count=token_count,
                    sae_level=sae_level,
                    epias_stage=epias_stage,
                    chunk_type=chunk_type,
                ))
        return chunks

    def _split_by_headings(self, text: str) -> list:
        """Split markdown into (heading_hierarchy, content) tuples."""
        lines = text.split("\n")
        sections = []
        current_hierarchy = []
        current_content = []

        for line in lines:
            heading_match = re.match(r'^(#{1,3})\s+(.*)', line)
            if heading_match:
                # Save previous section
                if current_content:
                    content = "\n".join(current_content)
                    sections.append((list(current_hierarchy), content))
                    current_content = []

                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                # Update hierarchy
                while len(current_hierarchy) >= level:
                    current_hierarchy.pop()
                current_hierarchy.append(title)
            else:
                current_content.append(line)

        # Don't forget the last section
        if current_content:
            content = "\n".join(current_content)
            sections.append((list(current_hierarchy), content))

        return sections

    def _split_to_size(self, text: str) -> list:
        """Split text into chunks of MAX_TOKENS. Keep tables atomic."""
        tokens = self._count_tokens(text)
        if tokens <= self.MAX_TOKENS:
            return [text]

        # Try splitting by double newlines (paragraphs)
        paragraphs = re.split(r'\n\n+', text)
        chunks = []
        current = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self._count_tokens(para)
            if current_tokens + para_tokens > self.MAX_TOKENS and current:
                chunks.append("\n\n".join(current))
                current = [para]
                current_tokens = para_tokens
            else:
                current.append(para)
                current_tokens += para_tokens

        if current:
            chunks.append("\n\n".join(current))

        return chunks if chunks else [text]

    def _extract_sae_level(self, text: str) -> Optional[int]:
        """Extract SAE level from text. 'SAE L2' or 'L3' -> 2 or 3."""
        match = re.search(r'(?:SAE\s+)?L(\d)', text)
        return int(match.group(1)) if match else None

    def _extract_epias_stage(self, text: str) -> Optional[str]:
        """Extract EPIAS stage. 'Explorer' -> 'E', 'Practitioner -> Integrator' -> 'P'."""
        stage_map = {
            'explorer': 'E', 'practitioner': 'P', 'integrator': 'I',
            'architect': 'A', 'steward': 'S'
        }
        text_lower = text.lower()
        # If there's an arrow, use the first (source) stage
        if '->' in text_lower or '→' in text_lower:
            parts = re.split(r'->|→', text_lower)
            for word, code in stage_map.items():
                if word in parts[0]:
                    return code
        # Otherwise, find any stage mention
        for word, code in stage_map.items():
            if word in text_lower:
                return code
        return None

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
