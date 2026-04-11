# Milestone 2 Backlog (Prepared During M1)

## High Priority
1. Add SQL storage layer and migration plan from CSV outputs.
2. Add robust parsing for multiple CV templates.
3. Implement education analysis module:
   - CGPA normalization
   - institution ranking lookup
   - gap detection
4. Implement professional experience analysis:
   - overlap detection
   - gap detection
   - progression checks
5. Implement missing-info detection and email draft generation.

## Medium Priority
1. Integrate Scopus/WoS/CORE stubs for publication validation.
2. Add section-level confidence scoring and source traceability.
3. Add richer dashboard summary endpoint.

## Risks to Track
1. API/provider limits for external ranking services.
2. CV variability causing parser misses.
3. Data schema drift if M2 introduces breaking changes.
