# Incremental-SQL-ELT-with-Watermarks
A stateful incremental ELT demo that transfers changed records from a SQLite source into a reporting database. Composite timestamp-and-ID watermarks, deterministic upserts, and replay-safe execution reduce duplicate processing on each run. Includes sample data, operational counters, and tests; models polling-based updates rather than log-based CDC.
