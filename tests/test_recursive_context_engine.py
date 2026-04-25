from loci.models.schemas import Scope, Section, new_id
from loci.services.recursive_context_engine import RecursiveContextEngine
from loci.services.storage_service import StorageService


def test_recursive_context_engine_answers_with_citations(tmp_path):
    storage = StorageService(data_dir=tmp_path / "data", db_path=tmp_path / "loci.sqlite")
    doc = storage.create_document("RCE", "pasted", None, "hash")
    storage.create_section(
        Section(
            id=new_id("sec"),
            document_id=doc.id,
            title="Recursive retrieval",
            verbatim_content="Recursive retrieval searches smaller sections instead of stuffing the entire corpus into a prompt.",
            ai_summary="Explains recursive retrieval for scoped context.",
        )
    )

    engine = RecursiveContextEngine(storage=storage, max_tool_calls=8)
    answer = engine.answer_query("How does recursive retrieval avoid huge prompts?", Scope(document_id=doc.id))

    assert "Recursive retrieval" in answer.answer
    assert answer.citations
    assert answer.trace
    stored_traces = storage.list_traces(answer.trace[0].inputs["run_id"])
    assert stored_traces


def test_recursive_context_engine_enforces_tool_limit(tmp_path):
    storage = StorageService(data_dir=tmp_path / "data", db_path=tmp_path / "loci.sqlite")
    doc = storage.create_document("Limit", "pasted", None, "hash")
    storage.create_section(
        Section(
            id=new_id("sec"),
            document_id=doc.id,
            title="Tool budget",
            verbatim_content="Tool budget enforcement prevents unbounded recursive context inspection.",
            ai_summary="Budget enforcement.",
        )
    )

    engine = RecursiveContextEngine(storage=storage, max_tool_calls=1)
    try:
        engine.answer_query("What prevents unbounded inspection?", Scope(document_id=doc.id))
    except RuntimeError as exc:
        assert "tool limit" in str(exc)
    else:
        raise AssertionError("Expected tool limit to raise RuntimeError")
