from __future__ import annotations

from pathlib import Path

from loci.services.ingestion_pipeline import IngestionPipeline
from loci.services.storage_service import StorageService


def test_markdown_ingestion_preserves_original_and_creates_artifacts(tmp_path: Path) -> None:
    storage = StorageService(data_dir=tmp_path / "data")
    pipeline = IngestionPipeline(storage)
    source = "# Intro\nOriginal alpha beta.\n\n## Details\nEquation-ish: E = mc^2\n"

    result = pipeline.ingest_text("Paper", source, source_type="markdown")

    assert result.document.source_type == "markdown"
    assert Path(result.document.source_path or "").read_text(encoding="utf-8") == source
    assert [section.title for section in result.sections] == ["Intro", "Details"]
    assert result.sections[0].verbatim_content == "Original alpha beta.\n\n"
    assert result.sections[1].parent_id == result.sections[0].id
    assert {artifact.artifact_type for artifact in result.artifacts} == {
        "summary",
        "faq",
        "critique",
        "takeaways",
    }
    assert all(artifact.model == "fallback-local" for artifact in result.artifacts)


def test_txt_ingestion_without_headings_creates_single_verbatim_section(tmp_path: Path) -> None:
    storage = StorageService(data_dir=tmp_path / "data")
    pipeline = IngestionPipeline(storage)
    text = "A source paragraph with Bayesian inference.\nSecond paragraph is preserved."

    result = pipeline.ingest_text("Notes", text, source_type="pasted")

    assert len(result.sections) == 1
    assert result.sections[0].verbatim_content == text
    assert result.sections[0].title == "Notes"
