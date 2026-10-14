import copy
import unittest
from bridge.reciprocal import BridgeError, qualify

REQ = dict(object_id='obj:sample', room_id='room:sample',room_revision='rev:1',operation_id='op:1',question='Where is the object in this analytical frame?',dimensions={k:None for k in ('Identity','Relationship','Space','Time','Transformation','Verification')},evidence_refs=['e:1'],claim_ceiling='CONTEXT_ONLY',authorized_view='view:1',permitted_operation='CONTEXT_PRESSURE_ONLY',time_constraint='t:1',authority='NONE',human_gate='ACTIVE')
RET = dict(observer_id='osprey',observer_class='CONTROLLED_SUB_OBSERVER',operation_id='op:1',object_id='obj:sample',room_id='room:sample',room_revision='rev:1',authorized_view='view:1',evidence_refs=['e:1'],claim_ceiling='CONTEXT_ONLY',disposition='OBSERVED',observations=[dict(claim='Relationship observed in supplied context',evidence_refs=['e:1'],status='OBSERVED')],provenance_refs=['e:1'],authority='NONE',human_gate='ACTIVE')

class ContractTests(unittest.TestCase):
    def test_valid(self):
        out=qualify(REQ,[RET]); self.assertEqual(out['round_count'],1);self.assertEqual(out['authority'],'NONE')
    def test_no_return(self): self.assertEqual(qualify(REQ,[])['disposition'],'AWAITING_OSPREY_RETURN')
    def test_repeat_stops(self): self.assertEqual(qualify(REQ,[RET,RET])['disposition'],'REPEATED_RETURN_STOP')
    def test_deterministic(self): self.assertEqual(qualify(REQ,[RET]),qualify(REQ,[RET]))
    def test_immutability(self):
        a,b=copy.deepcopy(REQ),copy.deepcopy(RET);qualify(REQ,[RET]);self.assertEqual((REQ,RET),(a,b))
    def reject_req(self, key, value):
        x=copy.deepcopy(REQ);x[key]=value
        with self.assertRaises(BridgeError): qualify(x,[RET])
    def reject_ret(self,key,value):
        x=copy.deepcopy(RET);x[key]=value
        with self.assertRaises(BridgeError): qualify(REQ,[x])
    def test_authority(self): self.reject_req('authority','MODEL')
    def test_human_gate(self): self.reject_req('human_gate','SATISFIED')
    def test_missing_dimension(self): self.reject_req('dimensions',{'Identity':1})
    def test_collection(self): self.reject_req('permitted_operation','COLLECT')
    def test_binding(self): self.reject_ret('room_revision','rev:2')
    def test_wrong_observer(self): self.reject_ret('observer_id','eagle')
    def test_ceiling(self): self.reject_ret('claim_ceiling','PRIMARY_EVIDENCE')
    def test_evidence_escalation(self): self.reject_ret('evidence_refs',['new'])
    def test_provenance(self): self.reject_ret('provenance_refs',[])
    def test_round_limit(self):
        with self.assertRaises(BridgeError): qualify(REQ,[RET,RET],1)
    def test_observation_scope(self):
        x=copy.deepcopy(RET);x['observations'][0]['evidence_refs']=['new']
        with self.assertRaises(BridgeError): qualify(REQ,[x])
    def test_disposition(self): self.reject_ret('disposition','VERIFIED_TRUTH')

if __name__ == '__main__': unittest.main()
