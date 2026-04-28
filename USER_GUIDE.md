# Loci User Guide

Loci is a local desktop knowledge-base app for importing technical content, reading it with source/AI separation, and working with grounded AI agents.

## Core Concepts

Loci is built around a strict split between source material and generated material.

`Source content` is content you import or paste. It is treated as the ground truth. Loci stores source files under `loci/data/sources/` with hash-based filenames and keeps section text as verbatim slices. Source content is not silently rewritten by the app.

`AI-generated content` is anything produced by the app or by an AI model: summaries, critiques, scratchpad notes, research fragments, generated documents, consistency scan results, and agent replies. Generated content is stored separately and carries metadata such as model, provider, prompt version, provenance, confidence, and grounding references when available.

`Grounding` means that a generated claim is tied back to imported source sections. Loci uses local retrieval through the Recursive Context Engine and lexical grounding checks to attach section IDs, quotes, and confidence scores. Grounding is a warning system and traceability layer; it does not mathematically prove that a claim is true.

`Artifacts` are AI outputs that are kept outside the original source. Some artifacts are database records, such as summaries and critiques. Larger generated documents are also mirrored as Markdown files under `loci/data/artifacts/generated_documents/`.

`Scratchpads` are durable workspaces where agents collaborate. A scratchpad contains ordered entries, each with an actor, iteration number, content, grounding references, confidence, and metadata.

## Launch

From the repository root:

```bash
conda activate loci
python app.py
```

Optional API configuration lives in `.env`. Loci can run without keys by using deterministic fallback behavior.

For OpenAI:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

For LM Studio local dreaming:

```bash
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=local-model
```

## Import Content

Use the top toolbar:

- `Upload File` imports PDF, Markdown, or text files.
- `Paste Text` creates a new document from pasted source text.

Imported source files are stored immutably under `loci/data/sources/`. Loci does not rewrite user source content.

The left Library pane shows documents and sections. Selecting a section opens it in the center reader and loads the right-side agent workspace.

## Reader

The center pane shows:

- `Source`: the original imported section content.
- `AI Summary`: generated summary/provenance metadata.
- Artifact buttons: `Whole Summary`, `FAQ`, `Critique`, and `Takeaways`.
- `Write Mode`: editable only for AI-generated sections. Imported user source stays read-only.

AI-generated documents and sections are marked with `[AI]` in the library and reader.

## Agent Workspace

The right pane has five tabs:

- `Dreaming`: shared scratchpads where Beginner, Critique, and Expert agents discuss the selected content.
- `Question`: user questions and final Expert answers.
- `Actions`: quick AI actions and document-level tools.
- `References`: cross-references and research inbox fragments.
- `Consistency`: section/document quality scans.

### Dream Cycles

Click `Dream Cycle` to start a bounded agent loop for the selected section. The agents work together for up to 10 iterations:

1. Beginner raises questions and unclear points.
2. Critique challenges assumptions and weak grounding.
3. Expert decides whether the synthesis is grounded enough.

If the Expert approves the result, Loci creates a separate AI-generated document under `loci/data/artifacts/generated_documents/`. It does not go into the user source folder.

Dream cycles run asynchronously, so the UI remains responsive while local or remote models are working.

#### What Dreaming Means

Dreaming is Loci's background thinking mode for imported content. Instead of waiting for a user question, the agents proactively inspect the selected section and ask: What is unclear? What is important? What might a reader ask next? What synthesis is supported by the saved material?

The current dream cycle is section-scoped. When a section is selected, Loci checks whether a dream scratchpad already exists for that section. If not, it can start a dream cycle. You can also run one manually with `Dream Cycle`.

Each dream cycle creates an `AgentScratchpad` with kind `dream`. The scratchpad records:

- the selected document and section
- the selected dream provider, such as LM Studio or OpenAI
- the model name and local base URL if applicable
- the maximum iteration count
- the final Expert answer if one is approved
- confidence and grounding metadata

Each iteration can produce three kinds of entries:

- Beginner entry: raises plain-language questions, confusions, and reader needs.
- Critique entry: challenges evidence, scope, assumptions, contradictions, and unsupported claims.
- Expert entry: synthesizes the strongest grounded result and either approves it or asks for more grounding.

The loop stops early if the Expert approves a grounded result. Otherwise, it stops at 10 iterations. The iteration cap prevents runaway local model calls and keeps the UI predictable.

#### Dreaming Data Flow

The dream flow is:

1. The selected section defines the scope.
2. The Recursive Context Engine searches and reads relevant local sections.
3. Beginner and Critique agents write scratchpad notes using the selected dream provider.
4. The Expert agent writes a Markdown synthesis using the same provider.
5. Grounding checks compare the Expert synthesis against source sections.
6. If the grounding confidence is high enough, the Expert result is approved.
7. Approved dream output becomes an AI-generated document and an artifact file.

The imported source file is never edited during this process.

#### Why Dreaming Uses Local Models

Dreaming is designed to be frequent and exploratory. Local models are a good default because they keep the loop private, cheap, and available even when the network is not. The `Dream: LM Studio` option points to LM Studio's OpenAI-compatible server, so Loci can use a local model through the same client interface it uses for OpenAI.

If LM Studio is not running or the selected model is unavailable, Loci falls back to deterministic local text generation for that call rather than crashing the app.

### Dream Model Switch

Use the `Dream:` dropdown beside the composer:

- `Dream: LM Studio`: uses a local OpenAI-compatible LM Studio endpoint.
- `Dream: OpenAI`: uses the OpenAI API.
- `Dream: Fallback`: uses local deterministic fallback behavior.

LM Studio should be running with an OpenAI-compatible server enabled. The default endpoint is `http://localhost:1234/v1`.

The switch only controls dream-agent generation. It does not change imported source content. It also does not currently change the embedding model. Embeddings are handled separately by `EmbeddingService`.

Provider metadata is stored on the scratchpad entries, so later you can inspect whether a dream note came from LM Studio, OpenAI, or fallback generation.

### Asking Questions

Type a question in the composer and click `Ask / Run`. Loci creates a new scratchpad for that question, lets the agents work together, and shows only the final Expert answer as the user-facing response.

Use the pipeline dropdown to choose:

- `Research`
- `Book Writer`
- `Bottom-Up Synthesis`
- `Graph Narrative`

The current implementation uses local Loci content first. If web search is unavailable, pipeline metadata notes that outside evidence was not fetched.

Question scratchpads are separate from dream scratchpads. A dream scratchpad is the agents thinking proactively about saved content. A question scratchpad is created from a user prompt and exists to produce one final answer for the user.

The final answer is stored as an Expert message in the section discussion thread. The intermediate agent work remains available in the scratchpad so the reasoning trail can be inspected without crowding the user-facing answer.

## Artifacts And Generated Documents

Loci uses the word `artifact` for AI-generated material that is not part of the original source.

There are several artifact-like outputs:

- `AIArtifact` records: document-level generated outputs such as summaries, FAQs, critiques, takeaways, pipeline reports, and consistency scans.
- `DiscussionMessage` records: user and agent messages in section threads.
- `AgentScratchpad` and `AgentScratchpadEntry` records: multi-agent collaboration history.
- `ResearchFragment` records: staged generated notes that are not yet part of the manuscript.
- AI-generated `Document` and `Section` records: approved generated Markdown content visible in the library.
- Generated Markdown files: filesystem copies under `loci/data/artifacts/generated_documents/`.

The important distinction is that generated documents are visible in the library like normal documents, but they are marked `[AI]` and have `source_type = ai_generated`. Their source path points to `artifacts/generated_documents/`, not `sources/`.

### Artifact Metadata

Generated content usually stores metadata such as:

- `provenance`: where it came from, such as `ai_generated`
- `generated_by`: which agent or pipeline created it
- `source_scratchpad_id`: the scratchpad that led to the output
- `confidence`: grounding confidence
- `grounding`: section references and quotes
- `model`: model name
- `provider`: `local`, `openai`, or `fallback`
- `base_url`: local OpenAI-compatible endpoint when applicable

This metadata is meant to make generated content auditable. You should be able to tell what created a piece of content and which source sections it relied on.

### Generated Documents vs Research Fragments

Generated documents are promoted, structured outputs. They appear in the Library and can contain a section tree. They are appropriate for Expert-approved dream synthesis, pipeline reports, and longer generated Markdown.

Research fragments are staged notes. They live in the research inbox and do not appear as manuscript sections until you promote them with `Add to Manuscript`. Quick Actions usually create fragments because their output may need review before becoming part of a document.

## Quick Actions

The `Actions` tab provides section-level actions such as:

- `Expand`
- `Summarize`
- `Critique`
- `Generate Title`
- `Generate Questions`
- `Split Section`
- `Rewrite for Clarity`
- `Expand Derivation`
- `Generate Figure`
- `Add Exercises`
- `Reorganize`

Document-level actions include:

- `Consistency Scan`
- `Duplicate Detection`
- `Terminology Normalization`
- `Structure Critique`

Action outputs are saved as research fragments. Fragments can be promoted into AI-generated manuscript sections from the `References` tab.

Quick Actions are intentionally conservative. They do not rewrite imported source sections. Instead, they create reviewable generated fragments. This gives you a chance to inspect, edit, or discard the output before it becomes part of an AI-generated section.

## References

Open the `References` tab to:

- View explicit cross-references for the selected section.
- Add a related/supports/contradicts/extends/summarizes/cites reference to another section.
- Review research inbox fragments related to the selected section.
- Promote a fragment into the manuscript with `Add to Manuscript`.

Reference relationship types are:

- `Related`: loose conceptual connection.
- `Supports`: target section supports the source section.
- `Contradicts`: target section challenges or conflicts with the source section.
- `Extends`: target section develops the idea further.
- `Summarizes`: target section summarizes the source section.
- `Cites`: source section cites or depends on the target.

Grounding references and cross-references are related but different. Grounding references are evidence links created by AI/retrieval workflows. Cross-references are editorial links you explicitly create between sections.

## Consistency Scans

The `Consistency` tab can scan either the selected section or the whole document. Results include severity, category, and a short issue description.

Examples of checks include:

- Empty sections
- Missing summaries
- Duplicate titles
- Low grounding for AI-generated sections
- Draft markers such as `TODO` or `TBD`

Consistency scan results are stored as generated issue records. They are not permanent changes to the source. You can clean them with `Clean AI Generated Content`.

## Organizing Documents

Right-click items in the left Library tree to:

- Add a section
- Add a chapter
- Rename
- Promote a section to chapter
- Delete a section

Manually added sections are treated as AI-generated/editable content, preserving the immutability of imported user sources.

## Cleaning AI-Generated Content

Use `Actions` -> `Clean AI Generated Content` to remove generated AI data while preserving imported source files and source sections.

Cleanup removes:

- AI-generated documents and generated Markdown files
- Agent scratchpads and entries
- Research fragments
- AI artifacts
- Consistency issues
- RCE traces
- Embeddings
- AI agent messages
- AI summaries on source sections

Cleanup preserves:

- Imported source files in `loci/data/sources/`
- Imported source documents and sections
- User messages

This is useful when you want to keep the imported library but reset all AI work. For example, after changing model settings, prompts, or provider choices, you can clean generated content and let Loci rebuild summaries, scratchpads, and generated documents from the preserved source.

Cleanup also clears AI summaries on source sections because those summaries are generated annotations, not imported source text.

## Data Locations

Default runtime data is stored under:

```text
loci/data/
  loci.sqlite
  sources/
  crops/
  artifacts/
    generated_documents/
```

Tests use temporary data directories and do not modify the default app database.

### SQLite Storage

Most metadata lives in `loci/data/loci.sqlite`. Key tables include:

- `documents`: imported and AI-generated documents.
- `sections`: section text, hierarchy, summaries, and metadata.
- `ai_artifacts`: generated document-level outputs.
- `discussion_threads` and `discussion_messages`: section discussions.
- `agent_scratchpads` and `agent_scratchpad_entries`: dream and question workspaces.
- `research_fragments`: staged generated notes.
- `content_references`: explicit section-to-section links.
- `consistency_issues`: scan results.
- `embeddings`: local or API-generated vectors.
- `rce_traces`: retrieval and tool-use traces.

The database and filesystem work together. For generated documents, SQLite stores the document and sections, while the generated Markdown file is stored under `artifacts/generated_documents/`.

## Test

Run the test suite with:

```bash
conda activate loci
python -m pytest
```
