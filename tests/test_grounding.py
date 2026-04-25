from __future__ import annotations

from loci.models.schemas import Section
from loci.services.grounding_service import GroundingService


def test_grounding_flags_supported_and_unsupported_claims() -> None:
    section = Section(
        document_id="doc_1",
        title="Caches",
        verbatim_content="Caches reduce repeated database reads by storing hot query results near the app.",
        ai_summary="Caches reduce repeated reads.",
    )
    service = GroundingService()
    result = service.check_artifact_grounding(
        "Caches reduce repeated database reads. Quantum teleportation solves every cache miss.",
        [section],
    )

    assert result["references"]
    assert result["confidence"] < 1.0
    assert any("Low grounding" in warning for warning in result["warnings"])
