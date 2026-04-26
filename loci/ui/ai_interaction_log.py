"""Window for reviewing Loci's AI prompts, replies, and tool traces."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import Any

from PySide6.QtWidgets import QDialog, QLabel, QScrollArea, QTextBrowser, QVBoxLayout, QWidget

from loci.models.schemas import AIArtifact, DiscussionMessage, DiscussionThread, Document, Section, ToolTrace
from loci.services.storage_service import StorageService
from loci.ui.widgets import Card, LabelPill


@dataclass(frozen=True)
class InteractionEvent:
    """Display-ready AI interaction event."""

    created_at: datetime
    title: str
    prompt: str
    reply: str
    model: str
    prompt_version: str
    source: str
    metadata: dict[str, Any]


class AIInteractionLogDialog(QDialog):
    """Show prompts and replies exchanged between Loci and AI services."""

    def __init__(self, storage: StorageService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.storage = storage
        self.setWindowTitle("AI Interaction Log")
        self.resize(980, 760)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        events = self._events()
        if not events:
            empty = QLabel("No AI interactions have been recorded yet.")
            empty.setObjectName("muted")
            layout.addWidget(empty)
        for event in events:
            layout.addWidget(self._event_card(event))
        layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _events(self) -> list[InteractionEvent]:
        documents = {document.id: document for document in self.storage.list_documents()}
        sections: dict[str, Section] = {}
        threads: list[DiscussionThread] = []
        for document in documents.values():
            for section in self.storage.list_sections(document.id):
                sections[section.id] = section
                threads.extend(self.storage.list_threads(section.id))

        events: list[InteractionEvent] = []
        for artifact in self.storage.list_artifacts():
            events.append(self._artifact_event(artifact, documents.get(artifact.document_id)))
        for thread in threads:
            events.extend(self._thread_events(thread, documents.get(thread.document_id), sections.get(thread.section_id)))
        for trace in self.storage.list_traces():
            events.append(self._trace_event(trace))
        return sorted(events, key=lambda event: event.created_at)

    def _artifact_event(self, artifact: AIArtifact, document: Document | None) -> InteractionEvent:
        document_title = document.title if document else artifact.document_id
        grounding = ", ".join(ref.get("section_id", "?") for ref in artifact.grounding[:8]) or "n/a"
        prompt = (
            f"Generate document artifact: {artifact.artifact_type}\n"
            f"Document: {document_title}\n"
            f"Prompt version: {artifact.prompt_version}\n"
            f"Grounding target sections: {grounding}"
        )
        return InteractionEvent(
            created_at=artifact.created_at,
            title=f"Artifact · {artifact.artifact_type.title()}",
            prompt=prompt,
            reply=artifact.content,
            model=artifact.model,
            prompt_version=artifact.prompt_version,
            source=str(artifact.metadata.get("source", "artifact")),
            metadata=artifact.metadata | {"confidence": artifact.confidence, "grounding": artifact.grounding},
        )

    def _thread_events(
        self,
        thread: DiscussionThread,
        document: Document | None,
        section: Section | None,
    ) -> list[InteractionEvent]:
        events: list[InteractionEvent] = []
        pending_prompt = ""
        document_title = document.title if document else thread.document_id
        section_title = section.title if section else thread.section_id
        for message in self.storage.list_messages(thread.id):
            if message.actor == "user":
                pending_prompt = message.content
                continue
            events.append(self._message_event(message, pending_prompt, document_title, section_title))
            pending_prompt = ""
        return events

    def _message_event(
        self,
        message: DiscussionMessage,
        prompt: str,
        document_title: str,
        section_title: str,
    ) -> InteractionEvent:
        model = str(message.metadata.get("model", "unknown"))
        prompt_version = str(message.metadata.get("prompt_version", "n/a"))
        return InteractionEvent(
            created_at=message.created_at,
            title=f"Discussion · {message.actor.replace('_', ' ').title()}",
            prompt=prompt or "No preceding user prompt was stored for this reply.",
            reply=message.content,
            model=model,
            prompt_version=prompt_version,
            source=f"{document_title} / {section_title}",
            metadata={"grounding": message.grounding, **message.metadata},
        )

    def _trace_event(self, trace: ToolTrace) -> InteractionEvent:
        inputs = dict(trace.inputs)
        run_id = inputs.pop("run_id", "manual")
        return InteractionEvent(
            created_at=trace.timestamp,
            title=f"Tool Trace · {trace.tool_name}",
            prompt=json.dumps(inputs, indent=2, sort_keys=True),
            reply=trace.output_summary,
            model="recursive-context-engine",
            prompt_version=f"depth {trace.depth}",
            source=str(run_id),
            metadata={},
        )

    def _event_card(self, event: InteractionEvent) -> QWidget:
        card = Card()
        card.add_header(event.title, LabelPill(event.source, "ai"))

        meta = QLabel(
            f"{event.created_at.isoformat()} • Model: {escape(event.model)} • "
            f"Prompt: {escape(event.prompt_version)}"
        )
        meta.setObjectName("muted")
        meta.setWordWrap(True)
        card.addWidget(meta)
        card.addWidget(self._block("Prompt / Context", event.prompt))
        card.addWidget(self._block("Reply / Output", event.reply))
        if event.metadata:
            card.addWidget(self._block("Metadata", json.dumps(event.metadata, indent=2, sort_keys=True, default=str)))
        return card

    @staticmethod
    def _block(title: str, text: str) -> QTextBrowser:
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            "<style>"
            "body { background: transparent; color: #C7CBD3; font-family: Inter, -apple-system, sans-serif; }"
            "h3 { color: #F2F3F5; font-size: 13px; margin: 0 0 8px; }"
            "pre { white-space: pre-wrap; margin: 0; line-height: 1.45; }"
            "</style>"
            f"<h3>{escape(title)}</h3><pre>{escape(text)}</pre>"
        )
        browser.setMinimumHeight(120)
        return browser
