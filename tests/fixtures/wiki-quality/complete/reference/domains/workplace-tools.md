# Workplace Tools

## Feature Coverage

### Feature: `poster-generation`

- Spec Basis: `WT-POSTER-001`.
- Surface: `src/ui/PosterTool.tsx` collects the selected poster type, inputs, and generation request.
- API or Event: `POST /api/jobs/poster/stream` is registered in `src/api/poster.routes.ts` and streams start, partial-image, completion, and error events.
- Authorization and Limits: `requireAuth` establishes the current user before provider selection, upload persistence, or generation.
- Service and Provider: the route resolves configured defaults and overrides, selects an allowed image provider, composes editable prompt content with enforced policy, and starts generation.
- Persistence and Lifecycle: the result and request conditions are stored through `recordPosterGeneration`; temporary inputs are attached to the snapshot and later retention cleanup.
- Usage, Cost and Audit: provider terminal usage is written to the shared usage ledger while the poster snapshot preserves the model and policy version used for the request.
- Failure and Recovery: connection close aborts active generation, rejected uploads fail before provider work, and best-effort retention cleanup cannot convert a completed generation into failure.
- Exact Tests: `tests/poster-generation.test.ts` covers provider selection, policy composition, snapshot persistence, cancellation, and cleanup boundaries.
