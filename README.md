# Incremental SQL ELT with Watermarks

A stateful incremental loading pattern that copies changed records from a transactional source into an analytics target using a composite high-watermark. Supports deterministic upserts, resumable reruns, and clear operational counters. Uses two SQLite databases to emulate source and warehouse systems without needing paid cloud credentials.

## Quick start

```bash
python incremental.py --demo
python -m unittest discover -s tests -v
```

## Architecture and scope

Illustrates timestamp/id watermarks, target UPSERT and exactly-once application for repeated runs. This is *polling-based incremental ELT*, not a database log-based CDC implementation; backdated changes require reconciliation.

**Portfolio note:** Original educational starter code, not a production deployment. Use only synthetic/public datasets, document your own extensions, and test integrations before claiming production experience.
