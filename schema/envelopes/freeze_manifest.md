# Freeze Manifest (PASS-1 → PASS-2 Bridge)
Status: CANONICAL-CANDIDATE (schema only)
Purpose: Domain-agnostic observational freeze boundary.

This schema defines the ONLY artifact class that may cross the Pass-1/Pass-2 boundary
as "observed reality claims" without importing algorithmic interpretation, tool behavior,
or narrative reasoning.

Pass 1: MAY EMIT freeze_manifest.json
Pass 2: MAY READ freeze_manifest.json (and verify hash/provenance), but MUST NOT mutate it.

---

## File
- Canonical name: `freeze_manifest.json`
- Canonical schema: `schema/envelopes/freeze_manifest.schema.json`

---

## Core Design Rules (Hard)
1. Freeze contains **claims**, not explanations.
2. Freeze contains **observations**, not conclusions.
3. Freeze is **domain-agnostic**:
   - no malware-specific, finance-specific, HR-specific ontology
   - all domain meaning is deferred to Pass-2 governance/interpretation
4. Every claim is:
   - attributable (source / method pointer)
   - scoped (context)
   - bounded (confidence / uncertainty)
   - replayable (references to the admission + normalization context)
5. Freeze MUST be hash-sealed and bound to the init/hydration context.

---

## JSON Schema: freeze_manifest.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "zervan://schema/envelopes/freeze_manifest/1.0.0",
  "title": "Zervan Freeze Manifest",
  "description": "Domain-agnostic observational freeze boundary artifact emitted in Pass-1 and consumed in Pass-2.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "artifact_class",
    "artifact_id",
    "created_utc",
    "pass",
    "authority_posture",
    "context",
    "inventory",
    "entities",
    "claims",
    "uncertainty",
    "freeze_seal"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0.0"
    },
    "artifact_class": {
      "type": "string",
      "const": "freeze_manifest"
    },
    "artifact_id": {
      "type": "string",
      "description": "Stable identifier for this freeze artifact (UUID recommended).",
      "minLength": 8
    },
    "created_utc": {
      "type": "string",
      "format": "date-time"
    },

    "pass": {
      "type": "integer",
      "description": "Pass number that emitted this artifact.",
      "enum": [1]
    },

    "authority_posture": {
      "type": "object",
      "additionalProperties": false,
      "required": ["mode", "posture", "mutation", "discovery"],
      "properties": {
        "mode": { "type": "string", "description": "e.g., CONTROLLED / DOUBLE_HELIX" },
        "posture": { "type": "string", "description": "e.g., READ-ONLY" },
        "mutation": { "type": "string", "enum": ["DISABLED"] },
        "discovery": { "type": "string", "enum": ["DISABLED", "CONDITIONAL"] }
      }
    },

    "context": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "run_id",
        "init_manifest_ref",
        "hydration_receipt_ref",
        "admission_ref",
        "normalization_ref"
      ],
      "properties": {
        "run_id": {
          "type": "string",
          "description": "Human and system reference for the run that produced this freeze."
        },
        "init_manifest_ref": {
          "type": "object",
          "additionalProperties": false,
          "required": ["path", "sha256"],
          "properties": {
            "path": { "type": "string" },
            "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        },
        "hydration_receipt_ref": {
          "type": "object",
          "additionalProperties": false,
          "required": ["path", "sha256"],
          "properties": {
            "path": { "type": "string" },
            "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        },
        "admission_ref": {
          "type": "object",
          "additionalProperties": false,
          "required": ["path", "sha256"],
          "properties": {
            "path": { "type": "string" },
            "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        },
        "normalization_ref": {
          "type": "object",
          "additionalProperties": false,
          "required": ["path", "sha256"],
          "properties": {
            "path": { "type": "string" },
            "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        }
      }
    },

    "inventory": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "input_artifacts",
        "evidence_binding"
      ],
      "properties": {
        "input_artifacts": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["ref", "sha256", "role"],
            "properties": {
              "ref": { "type": "string", "description": "Path, CAS, or external reference." },
              "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
              "role": { "type": "string", "description": "e.g., dataset, document_set, log, transcript" }
            }
          }
        },
        "evidence_binding": {
          "type": "object",
          "additionalProperties": false,
          "required": ["binding_type"],
          "properties": {
            "binding_type": {
              "type": "string",
              "description": "How evidence is referenced (inline, file, CAS, chunked+CAS)."
            },
            "cas_chunk_manifest_ref": {
              "type": "object",
              "additionalProperties": false,
              "required": ["path", "sha256"],
              "properties": {
                "path": { "type": "string" },
                "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
              }
            }
          }
        }
      }
    },

    "entities": {
      "type": "array",
      "description": "What exists in the observed world (subjects/objects) without interpreting meaning.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["entity_id", "entity_type"],
        "properties": {
          "entity_id": { "type": "string" },
          "entity_type": { "type": "string", "description": "e.g., person, host, account, file, transaction, event, concept" },
          "labels": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Optional human tags; must not imply authority (no 'malicious', 'fraud', etc.)."
          },
          "stable_attributes": {
            "type": "object",
            "description": "Key/value attributes intended to remain stable across runs.",
            "additionalProperties": { "type": ["string", "number", "boolean", "null"] }
          }
        }
      }
    },

    "claims": {
      "type": "array",
      "description": "Observed reality statements, not conclusions.",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "claim_id",
          "claim_type",
          "subject_ref",
          "predicate",
          "value",
          "units",
          "context",
          "confidence",
          "provenance"
        ],
        "properties": {
          "claim_id": { "type": "string" },
          "claim_type": {
            "type": "string",
            "enum": ["observation", "measurement", "relationship", "deviation", "constraint"]
          },
          "subject_ref": { "type": "string", "description": "entity_id or stable reference" },
          "object_ref": { "type": "string", "description": "optional entity_id if claim is relational" },

          "predicate": {
            "type": "string",
            "description": "Verb/descriptor for the claim (e.g., 'has_value', 'connected_to', 'frequency', 'distance_from_baseline')."
          },

          "value": {
            "description": "Claim value; MUST be meaning-neutral.",
            "oneOf": [
              { "type": "string" },
              { "type": "number" },
              { "type": "boolean" },
              { "type": "null" },
              { "type": "array", "items": { "type": ["string", "number", "boolean", "null"] } },
              { "type": "object", "additionalProperties": { "type": ["string", "number", "boolean", "null"] } }
            ]
          },

          "units": {
            "type": "string",
            "description": "e.g., count, seconds, bytes, score, probability, ratio, none"
          },

          "context": {
            "type": "object",
            "additionalProperties": false,
            "required": ["scope", "time_window"],
            "properties": {
              "scope": { "type": "string", "description": "Where/when this claim applies." },
              "time_window": {
                "type": "object",
                "additionalProperties": false,
                "required": ["start_utc", "end_utc"],
                "properties": {
                  "start_utc": { "type": "string", "format": "date-time" },
                  "end_utc": { "type": "string", "format": "date-time" }
                }
              },
              "population_ref": {
                "type": "string",
                "description": "Optional baseline population or cohort reference used ONLY to compute a measurement."
              }
            }
          },

          "confidence": {
            "type": "object",
            "additionalProperties": false,
            "required": ["level"],
            "properties": {
              "level": {
                "type": "string",
                "enum": ["low", "medium", "high"]
              },
              "numeric": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Optional numeric confidence for systems that compute it."
              }
            }
          },

          "provenance": {
            "type": "object",
            "additionalProperties": false,
            "required": ["evidence_ref", "method_ref"],
            "properties": {
              "evidence_ref": {
                "type": "string",
                "description": "Pointer to evidence (file path, CAS address, chunk id)."
              },
              "method_ref": {
                "type": "string",
                "description": "Pointer to method/mechanism ID (not narrative). Example: operator id, transform id, rule id."
              },
              "operator_chain": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Optional: ordered list of operator IDs applied to produce this claim."
              }
            }
          }
        }
      }
    },

    "uncertainty": {
      "type": "object",
      "additionalProperties": false,
      "required": ["unknowns", "exclusions", "resolution_limits"],
      "properties": {
        "unknowns": { "type": "array", "items": { "type": "string" } },
        "exclusions": { "type": "array", "items": { "type": "string" } },
        "resolution_limits": { "type": "array", "items": { "type": "string" } }
      }
    },

    "freeze_seal": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "freeze_sha256",
        "sealed_utc",
        "envelope_ref"
      ],
      "properties": {
        "freeze_sha256": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "SHA-256 of the canonicalized freeze_manifest JSON bytes (after stable ordering/canonicalization)."
        },
        "sealed_utc": { "type": "string", "format": "date-time" },
        "envelope_ref": {
          "type": "object",
          "additionalProperties": false,
          "required": ["path", "sha256"],
          "properties": {
            "path": { "type": "string", "description": "Path to proof/envelope artifact that binds freeze hash into governance." },
            "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        }
      }
    }
  }
}
