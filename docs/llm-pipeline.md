# LLM/NLP Pipeline Plan (Milestone 1 Design)

## Current M1 Approach
- Deterministic extraction first for reliable prototype.
- Pattern and section-based parsing for core CV fields.

## Planned LLM Hook (for M2/M3)
1. Chunk CV text by semantic sections.
2. Run extraction prompts per section.
3. Validate structured outputs with schema checks.
4. Store confidence and source span for each extracted attribute.

## Prompting Strategy (Planned)
- Use strict JSON schema responses.
- Ask model to extract evidence spans with each field.
- Use low temperature for consistency.

## Verification (Planned)
- Normalize with deterministic rules.
- Cross-check with external sources where needed in future milestones.
