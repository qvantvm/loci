from loci.models.schemas import AIArtifact, DiscussionMessage, Section, new_id
from loci.services.storage_service import StorageService


def test_storage_crud_round_trips_json_and_threads(tmp_path):
    storage = StorageService(data_dir=tmp_path / "data")
    source_path, digest = storage.save_pasted_source("Original text", ".txt")
    document = storage.create_document("Doc", "pasted", source_path, digest, {"kind": "test"})
    section = storage.create_section(
        Section(
            id=new_id("sec"),
            document_id=document.id,
            title="Intro",
            level=1,
            order_index=0,
            verbatim_content="Original text",
            ai_summary="AI summary",
            source_char_start=0,
            source_char_end=13,
            metadata={"warning": False},
        )
    )
    artifact = storage.create_artifact(
        AIArtifact(
            id=new_id("art"),
            document_id=document.id,
            section_id=section.id,
            artifact_type="summary",
            content="AI summary",
            grounding=[{"section_id": section.id, "quote": "Original text"}],
            model="fallback-local",
            prompt_version="test",
        )
    )
    thread = storage.get_or_create_root_thread(document.id, section.id)
    message = storage.create_message(
        DiscussionMessage(
            id=new_id("msg"),
            thread_id=thread.id,
            actor="user",
            content="Question?",
            grounding=[],
        )
    )

    loaded_document = storage.get_document(document.id)
    loaded_section = storage.get_section(section.id)
    assert loaded_document is not None and loaded_document.metadata["kind"] == "test"
    assert loaded_section is not None and loaded_section.verbatim_content == "Original text"
    assert storage.list_artifacts(document.id)[0].grounding == artifact.grounding
    assert storage.list_messages(thread.id)[0].content == message.content
    assert storage.get_or_create_root_thread(document.id, section.id).id == thread.id
