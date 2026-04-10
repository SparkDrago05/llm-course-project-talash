# Storage Schema (Milestone 1)

## Entities
- candidates(candidate_id, name, email, phone, current_title)
- education(candidate_id, entry)
- experience(candidate_id, entry)
- skills(candidate_id, skill)
- publications(candidate_id, entry)
- supervision(candidate_id, entry)
- patents(candidate_id, entry)
- books(candidate_id, entry)

## Relationship Model
- `candidate_id` is the join key across all tables.
- One candidate has many rows in each detail table.

## Output Targets
- `data/output/candidates.csv`
- `data/output/education.csv`
- `data/output/experience.csv`
- `data/output/skills.csv`
- `data/output/publications.csv`
- `data/output/supervision.csv`
- `data/output/patents.csv`
- `data/output/books.csv`

## Milestone 2 Additions (Planned)
- extraction metadata table (confidence, source offsets, parser version)
