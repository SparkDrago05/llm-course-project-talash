# TALASH (SMART HR RECRUITMENT)
## Milestone 3 Detailed Technical Report

**Course:** CS 417 – Large Language Models (Spring 2026)  
**Project:** Talent Acquisition & Learning Automation for Smart Hiring (TALASH)  
**Repository:** `llm-course-project-talash`  
**Submitted Milestone:** Milestone 3 – Full Integrated System  
**Prepared for:** Faculty of Computing, BSDS-2K23

---

## Executive Summary

TALASH is an AI-assisted recruitment support system designed to help university hiring committees and recruiters evaluate candidate CVs in a more structured, evidence-based, and scalable way. The project addresses a major limitation of conventional recruitment workflows: human reviewers often rely on manual reading, keyword matching, and subjective judgment, which can overlook deeper signals such as academic progression, publication quality, supervisory experience, collaboration patterns, topical consistency, and evidence-backed skill relevance.

This report documents the complete evolution of TALASH across the three milestones of the course project. Milestone 1 established the foundation through architecture design, wireframes, preprocessing planning, and an early upload/read prototype. Milestone 2 delivered the first functional intermediate system with multi-CV ingestion, structured extraction, educational analysis, professional experience analysis, missing-information detection, and personalized email drafting. Milestone 3 completes the system with a fully integrated analysis and ranking pipeline that adds research profile enrichment, topic variability analysis, co-author analysis, supervision analysis, books and patents extraction, skill alignment analysis, quantifiable candidate ranking, and a more comprehensive dashboard.

The final system is implemented as a modular Python backend using FastAPI, with a React + Vite frontend for visualization and interactive review. The design emphasizes interpretability, traceability, and practical usability. Rather than using a black-box decision model, the system combines deterministic parsing, rule-based evidence extraction, thematic matching, and weighted scoring to keep the output explainable to evaluators. Every candidate profile is converted into structured JSON with supporting analysis artifacts, chart-ready data, ranking scores, missing-information flags, and draft communication for follow-up.

---

## 1. Project Background

Recruitment in academic and research settings is not only about matching titles and keywords. A strong candidate may have a solid educational record, a consistent publication trail, meaningful supervision experience, a credible professional timeline, and evidence that claimed skills are actually supported by work history and research output. TALASH was developed to bring these signals together in one assistive system.

The project is especially suitable for CS 417 because it applies large language model inspired system design principles to document understanding, information extraction, semantic profile evaluation, ranking, and summarization. While the current implementation remains mostly deterministic and rule-based for reliability and traceability, it is architected so that LLM components can be added later for deeper reasoning, richer summarization, and better semantic inference.

The system processes PDF CVs, extracts raw text, normalizes structured fields, performs multiple analysis passes, and presents the results in a recruiter-friendly web dashboard. It also identifies missing information and drafts candidate-specific emails requesting clarifications, which is important in university recruitment workflows where CVs are often incomplete or inconsistently formatted.

---

## 2. Milestone 1 Overview

Milestone 1 established the conceptual and technical foundation of TALASH. The focus was not full implementation, but rather project definition, architecture, interface planning, and early pipeline prototyping.

### 2.1 Goals of Milestone 1

Milestone 1 aimed to answer the following questions:

- What problems does TALASH solve?
- What modules are needed to support CV screening and profile analysis?
- How should the system ingest and store candidate data?
- What should the user interface look like?
- How should the backend and frontend interact?

### 2.2 Deliverables Completed in Milestone 1

The first milestone included:

- System problem statement and scope definition
- High-level architecture design
- Initial preprocessing design for PDF CV ingestion
- Preliminary folder-based ingestion flow
- Early structured extraction plan
- UI/UX wireframes and interaction sketches
- Traceability mapping between course objectives and system functionality

### 2.3 Milestone 1 Implementation Perspective

Milestone 1 focused on building a clean conceptual boundary for the final product. The preprocessing module was designed to convert unstructured CV PDFs into machine-readable records. The architecture separated ingestion, parsing, storage, analysis, and presentation so the future system would remain modular and easy to extend.

The milestone also introduced the idea of linked structured outputs rather than a single monolithic document. This was important because candidate profiles include different information types: personal details, education, experience, publications, and later research enrichment. By planning the system around structured fields from the start, Milestone 1 laid the groundwork for a scalable pipeline in later milestones.

### 2.4 Milestone 1 Significance

Milestone 1 was important because it transformed the project from an idea into an engineering plan. It clarified what TALASH would and would not do, what kind of data it would consume, and how the output would be used in an academic recruitment context. The milestone also gave early confidence that the project could be implemented incrementally rather than as a single large build.

---

## 3. Milestone 2 Overview

Milestone 2 moved TALASH from design into a functioning intermediate system. It concentrated on reliable parsing, core candidate analysis, missing-information detection, and the first version of a usable dashboard.

### 3.1 Main Milestone 2 Objectives

The implemented goals for Milestone 2 were:

- Multi-CV ingestion and PDF processing
- Raw text extraction and traceable storage
- Structured extraction of candidate profile sections
- Educational profile analysis
- Professional experience and employment history analysis
- Missing-information detection
- Personalized draft email generation
- Initial candidate summary generation
- Partial research profile processing
- Intermediate web interface with tabular and chart outputs

### 3.2 Milestone 2 Outcomes

By the end of Milestone 2, TALASH could:

- Read multiple CVs from the input folder or uploaded files
- Convert PDFs into raw text files for auditing
- Parse education and experience entries into structured objects
- Detect missing fields such as incomplete dates or absent marks
- Produce candidate-specific summaries and email drafts
- Display candidate data in a browser-based interface

### 3.3 Milestone 2 Contribution to the Final System

Milestone 2 gave TALASH its first end-to-end operational pipeline. It established the main backend data flow, candidate JSON format, and frontend review style. It also introduced analysis functions that were intentionally simple and interpretable. This was a deliberate design choice: in a recruitment setting, explainability matters as much as accuracy.

---

## 4. Milestone 3 Objectives

Milestone 3 is the final integration phase of TALASH. It expands the system beyond the baseline profile analysis delivered in Milestone 2 and turns it into a more complete candidate assessment platform.

### 4.1 Milestone 3 Goals

The major implementation goals for Milestone 3 were:

- Extend research analysis beyond simple publication counting
- Analyze topic variability across candidate publications
- Measure co-author collaboration patterns
- Capture supervision strength and student-linked publication signals
- Extract and interpret books and patents
- Assess skill alignment with evidence from experience and publications
- Add a quantifiable weighted ranking module
- Improve dashboard comparison and candidate review support
- Preserve missing-information detection and email drafting
- Maintain backward compatibility with earlier milestone endpoints

### 4.2 Why Milestone 3 Matters

Milestone 3 is where TALASH becomes a full decision-support system rather than a basic parser. It now evaluates not just what a candidate wrote in the CV, but how strong the publication venues are, whether their research is focused or diverse, whether their collaboration footprint is broad, whether they have supervisory experience, and whether their claimed skills are supported by evidence across the profile.

This is a major shift from shallow screening to richer, quantifiable candidate assessment.

---

## 5. System Architecture in Milestone 3

TALASH follows a modular architecture with a Python backend and a React frontend. The modules are intentionally separated so that parsing, analysis, ranking, reporting, and presentation can evolve independently.

### 5.1 Backend Architecture

The backend is built with FastAPI and uses a structured, layered pipeline:

1. **Ingestion layer** reads PDF files from uploads or folders.
2. **Extraction layer** converts PDFs into raw text.
3. **Parsing layer** builds normalized structured objects.
4. **Analysis layer** computes educational, experience, research, and M3-specific signals.
5. **Ranking layer** combines multiple scores into a final numeric ranking.
6. **Output layer** writes results to JSON, CSV, and raw-text files.
7. **API layer** exposes endpoints for processing and dashboard use.

### 5.2 Frontend Architecture

The frontend uses React with Vite and presents the analysis in a recruiter-friendly dashboard. It includes:

- Multi-file CV upload
- Ranking weight controls
- Candidate leaderboard table
- Summary charts
- Radar-style candidate profile visualization
- Weighted composition chart
- Detailed modal views
- Email draft modal for missing information

### 5.3 Key Design Principle

The architecture separates data extraction from interpretation. That means the system first builds a clean structured representation of each candidate, then runs analysis over that structure. This improves traceability and makes debugging easier when a field is missing or a score looks unusual.

---

## 6. Implementation of the Core Pipeline

### 6.1 PDF Ingestion and Raw Text Extraction

The system supports batch PDF processing and upload-based processing. Each CV is extracted into raw text and stored under the output directory for traceability. This allows reviewers or developers to inspect the exact text that drove downstream decisions.

The main pipeline behavior is:

- Accept multiple CVs
- Validate file types
- Extract text from PDFs
- Store text artifacts
- Parse structured fields
- Generate analysis output
- Save consolidated candidate results

### 6.2 Structured Profile Parsing

The parser converts raw CV text into candidate-centered structured information such as:

- Personal information
- Education entries
- Experience entries
- Skills
- Publications
- Supervision entries
- Books
- Patents

This structured format is the foundation for all later analysis. It keeps the system flexible because each module can focus on one field family rather than reprocessing the raw CV repeatedly.

### 6.3 Output Traceability

TALASH stores key outputs to disk, including:

- `data/output/raw_text/` for extracted CV text
- `data/output/milestone2_candidates.json` for integrated candidate results
- CSV outputs for table-style reporting

This improves reproducibility and makes it easier to demonstrate the pipeline in a live evaluation.

---

## 7. Educational Profile Analysis

Educational analysis remained a core feature from Milestone 2 and continues to be part of the final system.

### 7.1 What the Module Evaluates

The educational module analyzes:

- SSE and HSSC performance
- Undergraduate and postgraduate records
- CGPA and percentage normalization
- Degree sequence and progression
- Institutional history
- Educational gaps and continuity
- Evidence-based strength interpretation

### 7.2 Analysis Logic

The module interprets education as a progression narrative rather than just a list of degrees. It looks at:

- Whether the candidate shows stable academic growth
- Whether the degree sequence is coherent
- Whether gaps exist between levels
- Whether progression supports research-oriented roles

### 7.3 Why It Matters

In recruitment for academic positions, education is not only about the highest degree. It also reflects consistency, depth, and readiness for higher-level work. TALASH uses educational analysis to help recruiters quickly identify whether a profile is academically strong, mixed, or incomplete.

---

## 8. Professional Experience and Employment History Analysis

Professional analysis was another important Milestone 2 feature and remains integral in Milestone 3.

### 8.1 Goals of the Module

The experience module checks:

- Timeline consistency
- Overlap between education and employment
- Overlap between jobs
- Employment gaps
- Gap justification
- Career progression

### 8.2 Analytical Focus

TALASH does not simply count jobs. It examines the sequence and consistency of job roles and dates to detect:

- Whether a candidate’s work history is internally coherent
- Whether the profile shows growth from junior to senior roles
- Whether work history helps explain educational gaps
- Whether the timeline contains questionable inconsistencies

### 8.3 Recruitment Relevance

This analysis is especially useful for university hiring because it helps differentiate between a candidate who had a legitimate research or teaching trajectory and one whose CV contains unexplained timeline issues.

---

## 9. Missing Information Detection and Email Drafting

A practical strength of TALASH is its ability to identify incomplete records and automatically draft follow-up communication.

### 9.1 Missing-Information Signals

The system identifies missing or unclear information such as:

- Absent academic scores
- Missing dates
- Incomplete publication metadata
- Missing authorship roles
- Unclear supervision entries
- Incomplete employment records

### 9.2 Email Drafting Function

If information is missing, TALASH generates a personalized draft email asking the candidate to provide the missing details. This is valuable because recruiters often need a polite and standardized way to request clarifications.

### 9.3 Why This Feature is Useful

The feature turns the system into a workflow assistant rather than only an analyzer. It supports action after analysis, helping recruiters follow up efficiently when CVs are incomplete.

---

## 10. Milestone 3 Research Profile Enrichment

Milestone 3 significantly expands the research analysis layer. Instead of only classifying publications, TALASH now interprets venue quality, topic diversity, collaboration structure, supervision evidence, and scholarly output beyond papers.

### 10.1 Research Quality Summary

The system calculates a research quality signal using publication metadata such as indexing status and quartile hints. The result is a compact interpretation such as:

- Strong
- Moderate
- Emerging
- Insufficient data

This helps recruiters quickly understand whether the publication record appears mature and visible.

### 10.2 Topic Variability Analysis

The topic variability module measures whether a candidate’s publications are concentrated in one research area or spread across several domains.

#### Inputs considered

- Publication titles
- Publication years
- Topic keywords and thematic signals

#### Internal logic

The system assigns each publication to a thematic cluster such as:

- Machine learning
- NLP
- Computer vision
- Cybersecurity
- Data science
- Software engineering
- Networks and IoT
- HR analytics

The system then computes:

- Dominant topic
- Theme distribution
- Variability score
- Specialization label
- Topic trend over time

#### Interpretation

- Low variability suggests deep specialization
- Medium variability suggests balanced diversity
- High variability suggests broad interdisciplinary activity

This is useful for assessing both focused researchers and broadly collaborative candidates.

### 10.3 Co-Author Analysis

The co-author analysis module examines collaboration patterns across publications.

#### Measures produced

- Number of unique co-authors
- Most frequent collaborators
- Average co-authors per paper
- Recurring collaboration ratio
- Team structure classification
- Collaboration diversity score

#### What the module reveals

This analysis helps determine whether a candidate:

- Works repeatedly with the same group
- Has a broad collaboration network
- Publishes in small or large teams
- Shows stable long-term collaborations

This is especially useful in research-heavy hiring because collaboration diversity and network strength can be meaningful academic signals.

### 10.4 Supervision Analysis

Supervision is a strong indicator of academic maturity and mentoring experience.

#### What the system extracts

From supervision-related entries, the module identifies:

- Total supervised students
- Main supervisor count
- Co-supervisor count
- Student level such as MS or PhD
- Graduation year where available
- Links between supervised students and publications

#### Additional signals

The system also checks whether publications include supervised students and whether the candidate appears as a corresponding author on those papers. This is a practical way to estimate mentorship-related scholarly output.

### 10.5 Books Analysis

The books module extends scholarly evaluation beyond journal and conference papers.

#### Extracted book details

- Title
- Authors
- ISBN
- Publisher
- Year
- Online link if available

#### Additional interpretation

The system assigns a candidate role such as:

- Sole author
- Lead author
- Co-author
- Contributor

It also estimates publisher strength using publisher hints, which helps distinguish stronger academic publishers from unknown ones.

### 10.6 Patents Analysis

The patents module captures applied innovation output.

#### Extracted patent details

- Patent number
- Title
- Date
- Inventors
- Country
- Verification link

#### Interpretation

The module determines whether the candidate appears as:

- Lead inventor
- Co-inventor
- Contributor

This is useful in academic or applied research hiring because patents show translation of research into practical innovation.

---

## 11. Skill Alignment Analysis

Skill alignment is one of the most important Milestone 3 additions because it checks whether claimed skills are actually supported by the candidate’s broader profile.

### 11.1 What the Module Compares

The system compares skills against:

- Job titles and job descriptions in experience entries
- Publication titles and research themes
- Topic variability output
- Overall consistency across the profile

### 11.2 Evidence Categories

Skills are classified into four categories:

- Strongly evidenced
- Partially evidenced
- Weakly evidenced
- Unsupported

### 11.3 Scoring Logic

The module uses text matching across experience and publication evidence. A skill is considered stronger when it appears in both employment and research evidence. It is considered partial when it appears in only one. Unsupported skills are those with no clear backing in the profile.

### 11.4 Why This Matters

CVs often contain inflated skill lists. TALASH reduces that risk by checking whether skills are consistent with the rest of the record. This is especially important in screening systems where overclaimed technical ability can be misleading.

---

## 12. Quantifiable Candidate Ranking Module

One of the major objectives of Milestone 3 was to implement a full-scale ranking system that combines the candidate’s evidence signals into a single numeric score.

### 12.1 Ranking Inputs

The ranking score is built from these components:

- Education score
- Experience score
- Research score
- Skills score
- M3 enrichment score

### 12.2 Default Weighting Model

The system uses configurable weights with a default structure similar to:

- Education: 0.25
- Experience: 0.20
- Research: 0.30
- Skills: 0.15
- M3: 0.10

These values can be adjusted through the frontend ranking controls and the `/api/rank` endpoint.

### 12.3 How the Ranking Score is Computed

The ranking function combines normalized sub-scores and produces a final score rounded to two decimal places. Research quality, educational strength, work experience, skills, and milestone-3 analysis all contribute to the final ranking.

### 12.4 Benefits of the Ranking Module

The ranking module provides:

- Consistent candidate ordering
- Adjustable recruiter preferences
- A clearer shortlist view
- An interpretable numeric summary

This is a strong improvement over purely descriptive output because it helps reviewers compare candidates quickly.

---

## 13. Web Application and Dashboard

### 13.1 Upload and Processing Flow

The web app allows users to:

- Upload one or more PDF CVs
- Trigger automated processing
- Recalculate rankings with updated weights
- Inspect candidate results in tabular form
- Open detailed profile modals

### 13.2 Candidate Leaderboard

The leaderboard shows:

- Rank
- Score
- Candidate name
- Education score
- Experience summary
- Research volume
- Topic diversity
- Skill alignment
- Missing information indicators
- Action buttons

### 13.3 Visualization Layer

The frontend includes multiple chart views:

- Academic performance bar chart
- Professional tenure bar chart
- Research productivity bar chart
- Topic variability chart
- Skill evidence alignment chart
- Radar chart for one-candidate profile overview
- Weighted composition chart for ranking contribution analysis

### 13.4 Candidate Detail Modal

When a candidate is selected, the modal reveals:

- Personal information
- Education analysis
- Experience analysis
- Research and publication details
- Supervision information
- Books and patents
- Skill alignment evidence
- Radar summary values

### 13.5 Email Draft Modal

If a candidate has missing information, the interface can display a draft email and support quick copy-to-clipboard behavior. This closes the loop between analysis and follow-up action.

---

## 14. API Design and Endpoints

TALASH exposes both legacy milestone-compatible endpoints and Milestone 3 API endpoints.

### 14.1 Core Endpoints

- `GET /health`
- `POST /ingest`
- `POST /process/all`
- `GET /results/candidates`
- `GET /results/report`

### 14.2 Milestone 2 and M3 Analysis Endpoints

- `POST /api/ingest`
- `POST /api/process/all`
- `POST /api/upload-and-process`
- `GET /api/results/latest`
- `GET /api/dashboard`
- `POST /api/rank`

### 14.3 Why Dual Support Exists

The system keeps compatibility with earlier milestone behaviors while also exposing the newer integrated endpoints. This is useful for demo continuity, testing, and rubric alignment.

---

## 15. Data Outputs and Traceability

TALASH writes outputs to disk so that every stage of the pipeline can be audited.

### 15.1 Main Output Artifacts

- Raw extracted text per CV
- Candidate-level JSON results
- Batch result file with processed and failed files
- CSV-based presentation output

### 15.2 Traceability Importance

Traceability is critical in academic recruitment because candidate evaluation should be transparent. If a score is questioned, the system can show the raw evidence used to derive that score.

### 15.3 Result Structure

Each candidate record now includes fields such as:

- `name`
- `personal_info`
- `structured_data`
- `education_analysis`
- `experience_analysis`
- `research_profile`
- `research_quality`
- `topic_variability`
- `coauthor_analysis`
- `supervision_analysis`
- `books_analysis`
- `patents_analysis`
- `skill_alignment`
- `ranking_score`
- `missing_info`
- `summary`
- `email_draft`
- `raw_text_path`

---

## 16. Validation and Testing

The final system is supported by automated tests that cover the Milestone 3 analysis functions.

### 16.1 Testing Coverage

The current test suite checks that:

- Topic variability returns a score and distribution
- Co-author analysis returns collaboration metrics
- Supervision analysis counts main and co-supervisor records
- Books analysis assigns candidate role correctly
- Patents analysis assigns inventor role correctly
- Skill alignment returns evidence categories and a score

### 16.2 Purpose of Testing

The tests help ensure that the Milestone 3 expansion does not break the analytical pipeline and that the new modules return structured, expected outputs for downstream reporting.

---

## 17. How Milestone 3 Maps to the Course Rubric

Milestone 3 is aligned with the final project expectations in the course description.

### 17.1 Functional Coverage

TALASH now includes the requested functional areas:

- Educational profile analysis
- Research profile analysis
- Topic variability analysis
- Co-author analysis
- Supervision analysis
- Books and patents analysis
- Professional experience analysis
- Skill alignment analysis
- Tabular and graphical presentation
- Missing-information detection and email drafting
- Quantifiable candidate ranking

### 17.2 Evaluation Readiness

The system is ready for live demo because it provides:

- End-to-end processing
- Clear UI output
- Multiple candidate comparison
- Candidate detail inspection
- Ranking adjustability
- Evidence-backed summaries

---

## 18. Strengths of the Final System

### 18.1 Interpretability

The system is transparent. Recruiters can see why a candidate scored well because the logic is based on explicit evidence and readable analysis fields.

### 18.2 Modularity

The codebase separates parsing, analysis, ranking, and presentation. This makes future changes easier and lowers integration risk.

### 18.3 Practical Workflow Support

TALASH not only analyzes candidates but also supports follow-up actions through missing-information emails and summary generation.

### 18.4 Balanced Candidate View

The final ranking is not based on a single factor. It combines education, experience, research, skills, and M3 signals into a more complete profile assessment.

---

## 19. Limitations and Current Constraints

Even though Milestone 3 completes the requested scope, the system still has some practical constraints:

- Some extraction logic remains rule-based and may miss unusual CV formats
- Publication venue verification is heuristic in parts and can be improved with stronger external integration
- Topic clustering is keyword-driven rather than embedding-based
- Skill matching relies on text overlap and not full semantic reasoning
- Supervision, books, and patents are only as complete as the candidate-provided data

These are acceptable for the current project stage, but they also define a clear roadmap for future refinement.

---

## 20. Future Enhancements

If TALASH is extended beyond Milestone 3, the following improvements would be valuable:

- Add LLM-assisted semantic extraction for harder CV formats
- Integrate live external APIs for journal, conference, and patent verification
- Improve topic modeling with embeddings or clustering models
- Add stronger visualization for collaboration networks
- Include explainable ranking breakdowns at the feature level
- Support database-backed persistence for multi-session use
- Add authentication and role-based access for recruiter workflows

---

## 21. Conclusion

Milestone 3 transforms TALASH into a complete smart recruitment support platform for academic and research hiring. Milestone 1 established the architecture and workflow vision. Milestone 2 delivered the core CV ingestion, structured parsing, education analysis, experience analysis, missing-information detection, and initial UI. Milestone 3 adds the richer academic and research intelligence needed for a serious profile evaluation system.

With the final integration of research quality interpretation, topic variability, co-author analysis, supervision analysis, books and patents extraction, skill alignment, and weighted ranking, TALASH now provides a broad and practical evidence-based candidate assessment workflow. The result is a transparent, modular, and demo-ready system that aligns well with the goals of CS 417 and the Smart HR Recruitment project.

---

## Appendix A: Milestone Summary Table

| Milestone | Main Focus | Key Deliverables |
|---|---|---|
| Milestone 1 | Proposal and design | Architecture, wireframes, preprocessing plan, early prototype |
| Milestone 2 | Core pipeline | Multi-CV ingestion, structured extraction, education/experience analysis, missing info detection, summary generation |
| Milestone 3 | Full integration | Research enrichment, topic variability, co-author analysis, supervision, books, patents, skill alignment, ranking, dashboard integration |

## Appendix B: Final Candidate Analysis Fields

| Category | Fields |
|---|---|
| Identity | `name`, `personal_info` |
| Structure | `structured_data`, `raw_text_path` |
| Education | `education_analysis` |
| Experience | `experience_analysis` |
| Research | `research_profile`, `research_quality` |
| Research Enrichment | `topic_variability`, `coauthor_analysis`, `supervision_analysis`, `books_analysis`, `patents_analysis` |
| Skills | `skill_alignment` |
| Ranking | `ranking_score` |
| Workflow Support | `missing_info`, `summary`, `email_draft` |

## Appendix C: Useful Project References

- Architecture notes: `docs/architecture.md`
- Milestone 1 traceability: `docs/m1-traceability.md`
- Milestone 2 report baseline: `milestone2_report.txt`
- Frontend app: `frontend/src/App.jsx`
- Core analysis service: `app/analysis_service.py`
- Milestone 3 analysis module: `app/m3_analysis.py`
