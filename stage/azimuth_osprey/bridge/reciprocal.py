"""Bounded, deterministic Azimuth/Osprey reciprocal qualification bridge.
No external collection, network access, evidence mutation or authority promotion.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Any

DIMENSIONS = ('Identity', 'Relationship', 'Space', 'Time', 'Transformation', 'Verification')
STATES = {'OBSERVED', 'NO_SIGNAL', 'INSUFFICIENT_EVIDENCE', 'EVIDENCE_CEILING_REACHED', 'VIEW_RESTRICTED', 'BOUNDARY_BLOCKED', 'PROVENANCE_INCOMPLETE', 'STALE_BINDING', 'DIVERGENT_BINDING', 'SEMANTIC_CONFLICT', 'OPERATING_SCOPE_EXCEEDED', 'AUTHORITY_VIOLATION', 'SCARRED'}

class BridgeError(ValueError):
    pass

def digest(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def validate_request(req: dict) -> None:
    required = {'object_id','room_id','room_revision','operation_id','question','dimensions','evidence_refs','claim_ceiling','authorized_view','permitted_operation','time_constraint','authority','human_gate'}
    if not isinstance(req, dict) or required - req.keys():
        raise BridgeError('REQUEST_FIELDS_MISSING')
    if not all(isinstance(req[k], str) and req[k].strip() for k in ('object_id','room_id','room_revision','operation_id','question','claim_ceiling','authorized_view','permitted_operation','time_constraint')):
        raise BridgeError('INVALID_IDENTITY_OR_SCOPE')
    if req['authority'] != 'NONE' or req['human_gate'] != 'ACTIVE':
        raise BridgeError('AUTHORITY_OR_GATE_VIOLATION')
    if not isinstance(req['dimensions'], dict) or set(req['dimensions']) != set(DIMENSIONS):
        raise BridgeError('SIX_DIMENSIONS_REQUIRED')
    if not isinstance(req['evidence_refs'], list) or any(not isinstance(x,str) or not x for x in req['evidence_refs']):
        raise BridgeError('INVALID_EVIDENCE_REFS')
    if req['permitted_operation'] != 'CONTEXT_PRESSURE_ONLY':
        raise BridgeError('OPERATION_NOT_PERMITTED')

def validate_return(req: dict, ret: dict) -> None:
    required = {'observer_id','observer_class','operation_id','object_id','room_id','room_revision','authorized_view','evidence_refs','claim_ceiling','disposition','observations','provenance_refs','authority','human_gate'}
    if not isinstance(ret, dict) or required - ret.keys():
        raise BridgeError('RETURN_FIELDS_MISSING')
    for k in ('operation_id','object_id','room_id','room_revision','authorized_view','claim_ceiling'):
        if ret[k] != req[k]:
            raise BridgeError('BINDING_DIVERGENCE:' + k)
    if ret['observer_id'] != 'osprey' or ret['observer_class'] != 'CONTROLLED_SUB_OBSERVER':
        raise BridgeError('OBSERVER_IDENTITY_VIOLATION')
    if ret['authority'] != 'NONE' or ret['human_gate'] != 'ACTIVE':
        raise BridgeError('AUTHORITY_OR_GATE_VIOLATION')
    if ret['disposition'] not in STATES:
        raise BridgeError('INVALID_DISPOSITION')
    if not isinstance(ret['evidence_refs'], list) or any(x not in req['evidence_refs'] for x in ret['evidence_refs']):
        raise BridgeError('EVIDENCE_SCOPE_ESCALATION')
    if not isinstance(ret['provenance_refs'], list) or not isinstance(ret['observations'], list):
        raise BridgeError('INVALID_RETURN_CONTENT')
    if ret['observations'] and not ret['provenance_refs']:
        raise BridgeError('UNATTRIBUTED_OBSERVATION')
    for obs in ret['observations']:
        if not isinstance(obs, dict) or not {'claim','evidence_refs','status'} <= obs.keys():
            raise BridgeError('UNSTRUCTURED_OBSERVATION')
        if not isinstance(obs['evidence_refs'], list) or any(x not in ret['evidence_refs'] for x in obs['evidence_refs']):
            raise BridgeError('OBSERVATION_EVIDENCE_ESCALATION')
        if obs['status'] not in STATES:
            raise BridgeError('INVALID_OBSERVATION_STATUS')

def qualify(req: dict, returns: list[dict], max_rounds: int = 3) -> dict:
    """Qualify supplied returns. No invented Osprey observations or auto-execution.

    The caller explicitly supplies each Osprey response. Repetition is detected;
    a subsequent round requires an externally supplied response and same bindings.
    """
    validate_request(req)
    if not isinstance(max_rounds, int) or not 1 <= max_rounds <= 16:
        raise BridgeError('INVALID_ROUND_BOUND')
    if not isinstance(returns, list) or len(returns) > max_rounds:
        raise BridgeError('ROUND_BOUND_EXCEEDED')
    records = []
    seen = set()
    for index, ret in enumerate(returns, 1):
        validate_return(req, ret)
        signature = digest(ret)
        if signature in seen:
            records.append({'round': index, 'disposition': 'REPEATED_RETURN_STOP', 'return_sha256': signature})
            break
        seen.add(signature)
        records.append({'round': index, 'disposition': ret['disposition'], 'return_sha256': signature,
                        'observations': ret['observations'], 'provenance_refs': ret['provenance_refs']})
    last = records[-1]['disposition'] if records else 'AWAITING_OSPREY_RETURN'
    return {'schema':'azimuth-osprey-stage/v1','standing':'STAGED_CANDIDATE',
            'object_id':req['object_id'],'operation_id':req['operation_id'],
            'request_sha256':digest(req),'rounds':records,'round_count':len(records),
            'disposition':last,'qualification':'BOUNDED_CONTRACT_VALIDATION_ONLY',
            'claim_ceiling':req['claim_ceiling'],'authority':'NONE','human_gate':'ACTIVE',
            'canonical_mutation':False,'external_collection':False,
            'next_action':'HUMAN_REVIEW_OR_EXPLICIT_NEXT_ROUND'}
