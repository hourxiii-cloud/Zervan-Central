# Zervan Git Forensics & File Resurrection Playbook

Authoritative Recovery Procedure for Surgically Restoring Deleted Artifacts  
Status: Operational  
Scope: Non-destructive repository repair

---

## Purpose

This playbook restores specific deleted files from Git history **without reverting the repository**.

It preserves:
- current architecture
- current branch state
- commit history integrity

It only reconstructs missing artifacts.

This is not rollback.
This is not reset.
This is controlled reconstruction.

---

## When To Use

Use this procedure when:

• A rollback removed operational files  
• A purge removed tooling  
• Architecture is correct but functionality broke  
• Only specific files must be recovered  

Do NOT use if you want the repository to go back in time.

---

## Conceptual Model

Git is treated as a temporal filesystem.

We are not changing history.
We are retrieving an object from a previous point in time.

Operation type: **Artifact Resurrection**

| Operation | Effect |
|--------|------|
git reset | rewrites history
git revert | undoes commit
git checkout branch | changes state
THIS METHOD | extracts file only

---

## Phase 1 — Locate Last Known Good Commit

Find commits affecting a file:
