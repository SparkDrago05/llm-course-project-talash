from app.m3_analysis import (
    analyze_books,
    analyze_coauthor_patterns,
    analyze_patents,
    analyze_skill_alignment,
    analyze_supervision_profile,
    analyze_topic_variability,
)


def _sample_publications() -> list[dict]:
    return [
        {
            "title": "Deep learning based sentiment analysis for Urdu text",
            "year": 2022,
            "type": "journal",
            "authors": ["Talash Candidate", "Ayesha Khan", "Ali Raza"],
            "candidate_authorship_role": "first",
            "api_info": {"is_indexed": True, "inferred_quartile": "Q1"},
        },
        {
            "title": "Cybersecurity intrusion detection using machine learning",
            "year": 2023,
            "type": "conference",
            "authors": ["Ayesha Khan", "Talash Candidate", "John Doe"],
            "candidate_authorship_role": "corresponding",
            "api_info": {"is_indexed": True, "inferred_quartile": "Q2"},
        },
    ]


def test_topic_variability_returns_distribution_and_score() -> None:
    result = analyze_topic_variability(_sample_publications())

    assert result["dominant_topic"] in {"machine_learning", "cybersecurity", "nlp", "other"}
    assert 0 <= result["variability_score"] <= 100
    assert isinstance(result["theme_distribution"], dict)


def test_coauthor_analysis_returns_expected_metrics() -> None:
    result = analyze_coauthor_patterns(_sample_publications(), "Talash Candidate")

    assert result["unique_coauthors"] >= 2
    assert result["average_coauthors_per_paper"] >= 1
    assert "collaboration_diversity_score" in result


def test_supervision_books_patents_and_skill_alignment() -> None:
    supervision = [
        {"raw": "Ayesha Khan - MS main supervisor - 2022"},
        {"raw": "Ali Raza - PhD co-supervisor - 2024"},
    ]
    publications = _sample_publications()

    supervision_result = analyze_supervision_profile(supervision, publications)
    assert supervision_result["main_supervisor_count"] == 1
    assert supervision_result["co_supervisor_count"] == 1

    books = [
        {
            "title": "Talash Candidate, Ayesha Khan, AI for Smart Hiring",
            "authors": ["Talash Candidate", "Ayesha Khan"],
            "publisher": "Springer",
            "isbn": "978-3-16-148410-0",
            "publishing_year": 2025,
        }
    ]
    books_result = analyze_books(books, "Talash Candidate")
    assert books_result["total_books"] == 1
    assert books_result["books"][0]["candidate_role"] in {"lead-author", "co-author", "sole-author"}

    patents = [
        {
            "title": "AI Recruitment Scoring Engine",
            "inventors": ["Talash Candidate", "Ali Raza"],
            "patent_number": "PK123456",
            "country": "PAKISTAN",
        }
    ]
    patents_result = analyze_patents(patents, "Talash Candidate")
    assert patents_result["total_patents"] == 1
    assert patents_result["patents"][0]["candidate_role"] in {"lead-inventor", "co-inventor"}

    topic_variability = analyze_topic_variability(publications)
    skill_alignment = analyze_skill_alignment(
        skills=["machine learning", "cybersecurity", "project management"],
        experience=[{"job_title": "Machine Learning Engineer", "organization": "TALASH Lab", "raw": ""}],
        publications=publications,
        topic_variability=topic_variability,
    )

    assert 0 <= skill_alignment["alignment_score"] <= 100
    assert "machine learning" in skill_alignment["strongly_evidenced"]
