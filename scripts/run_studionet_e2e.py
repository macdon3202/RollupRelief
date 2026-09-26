"""Run RollupRelief with two independent auxiliary wallets."""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC="https://studio.genlayer.com/api"; EX="https://explorer-studio.genlayer.com"
IID="cmrazrvph0am30rns9tzwb2oa"; CHAIN="OP_MAINNET"; URL=f"https://status.optimism.io/en-us/{IID}"
NEG_IID="cmthk6pbx0at41ms2q9i1iqlu"; NEG_URL=f"https://status.optimism.io/en-us/{NEG_IID}"

def wallets():
    p=Path(__file__).resolve().parents[2]/"secrets"/"genlayer-test-wallets.env"
    for line in p.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k,v=line.split("=",1);os.environ.setdefault(k.strip(),v.strip().strip("'\"<>") )
    return create_account(os.environ["SERVICE_LEDGER_KEY_A"]),create_account(os.environ["SERVICE_LEDGER_KEY_B"])

def plain(v):
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [plain(x) for x in v]
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)

def signals(info):
    status=str(info.get("status_name") or info.get("status") or "UNKNOWN").upper();cons=str(info.get("result_name") or info.get("consensus_result_name") or "UNKNOWN").upper();vals=[]
    data=info.get("consensus_data")
    if isinstance(data,dict):
        for x in data.get("validators") or []:
            if isinstance(x,dict) and str(x.get("vote","")).lower()!="idle":vals.append(str(x.get("execution_result") or "").upper())
    exe="ERROR" if any(any(t in x for t in("ERROR","FAIL","REVERT"))for x in vals) else "SUCCESS" if vals else "UNKNOWN"
    return status,exe,cons

def read(c,a,w,fn,args=[]):return plain(c.read_contract(address=a,function_name=fn,args=args,account=w))
def send(c,a,w,fn,args,expected_error=False):
    tx=str(c.write_contract(address=a,function_name=fn,args=args,account=w,value=0));print(json.dumps({"submitted":fn,"tx":tx}),flush=True)
    for _ in range(200):
        try:
            info=plain(c.get_transaction(tx));status,exe,cons=signals(info)
        except Exception as error:
            print(json.dumps({"poll_retry":tx,"error":str(error)[:120]}),flush=True);time.sleep(3);continue
        if status=="FINALIZED":
            if (exe=="ERROR")!=expected_error:raise AssertionError(f"{fn}: expected_error={expected_error}, execution={exe}, tx={tx}")
            if not expected_error and cons!="MAJORITY_AGREE":raise RuntimeError(f"{fn}: consensus={cons}")
            return {"method":fn,"tx":tx,"status":status,"execution":exe,"consensus":cons,"expected_error":expected_error,"explorer":f"{EX}/tx/{tx}"}
        if status in{"FAILED","REJECTED","CANCELLED"}:raise RuntimeError(f"{fn}: {status}")
        time.sleep(3)
    raise TimeoutError(tx)

def main():
    if len(sys.argv)!=2:raise SystemExit("usage: run_studionet_e2e.py CONTRACT_ADDRESS")
    address=sys.argv[1];reporter,verifier=wallets();client=create_client(chain=studionet,account=reporter,endpoint=RPC)
    cfg=read(client,address,reporter,"get_config")
    expected={"version":"ROLLUP_RELIEF_V3","architecture":"ROLE_SEPARATED_INCIDENT_ATTESTATION","origin":"https://status.optimism.io","history":"https://status.optimism.io/history/1","access":"PERMISSIONLESS_PER_INCIDENT_TWO_WALLET"}
    for k,v in expected.items():
        if str(cfg.get(k)).lower()!=str(v).lower():raise RuntimeError(f"wrong deployment {k}: {cfg}")
    proof={"network":"studionet","contract":address,"contract_explorer":f"{EX}/address/{address}","roles":{"reporter_for_this_incident":reporter.address,"independent_verifier":verifier.address,"access":"permissionless; roles derive per incident"},"fixtures":{"positive":{"incident_id":IID,"chain":CHAIN,"url":URL,"expected":"WRITE_INCLUSION/MATERIAL/true"},"negative":{"incident_id":NEG_IID,"chain":CHAIN,"url":NEG_URL,"expected":"MAINTENANCE/NONE/false"},"cross_check":"https://status.optimism.io/history/1"},"initial_config":cfg,"transactions":[],"readbacks":{}}
    try: opened=read(client,address,reporter,"get_incident",[IID])
    except Exception: opened=None
    if opened is None:
        proof["transactions"].append(send(client,address,reporter,"register_incident",[CHAIN,IID,URL]))
        opened=read(client,address,reporter,"get_incident",[IID])
    proof["readbacks"]["registered"]=opened
    if opened.get("state")!="REGISTERED":raise AssertionError(opened)
    if opened.get("state")=="REGISTERED":
        proof["transactions"].append(send(client,address,reporter,"assess_incident",[IID],True))
        if read(client,address,reporter,"get_incident",[IID])!=opened:raise AssertionError("self-assessment mutated state")
        proof["transactions"].append(send(client,address,reporter,"register_incident",[CHAIN,IID,URL],True))
        if read(client,address,reporter,"get_incident",[IID])!=opened:raise AssertionError("duplicate mutated state")
    if opened.get("state")=="REGISTERED": proof["transactions"].append(send(client,address,verifier,"assess_incident",[IID]))
    checked=read(client,address,verifier,"get_incident",[IID]);att=read(client,address,verifier,"get_attestation",[IID,1]);proof["readbacks"]["assessed"]=checked;proof["readbacks"]["attestation_1"]=att
    if checked.get("state")!="ATTESTED" or checked.get("affected_operation")!="WRITE_INCLUSION" or checked.get("impact_level")!="MATERIAL" or checked.get("qualifies_for_relief") is not True or len(checked.get("content_digest",""))!=64 or len(checked.get("source_digest",""))!=64:raise AssertionError(checked)
    proof["transactions"].append(send(client,address,verifier,"assess_incident",[IID],True))
    if read(client,address,verifier,"get_incident",[IID])!=checked:raise AssertionError("terminal replay mutated state")
    proof["transactions"].append(send(client,address,reporter,"register_incident",[CHAIN,NEG_IID,NEG_URL]))
    negative_opened=read(client,address,reporter,"get_incident",[NEG_IID]);proof["readbacks"]["negative_registered"]=negative_opened
    negative=None
    for attempt in range(1,4):
        proof["transactions"].append(send(client,address,verifier,"assess_incident",[NEG_IID]))
        negative=read(client,address,verifier,"get_incident",[NEG_IID])
        proof["readbacks"][f"negative_assessed_revision_{negative['revision']}"]=negative
        proof["readbacks"][f"negative_attestation_{negative['revision']}"]=read(client,address,verifier,"get_attestation",[NEG_IID,negative["revision"]])
        if negative.get("state") != "UNRESOLVED":
            break
    if negative.get("state")!="ATTESTED" or negative.get("incident_status")!="MAINTENANCE" or negative.get("affected_operation")!="NONE" or negative.get("impact_level")!="NONE" or negative.get("qualifies_for_relief") is not False or len(negative.get("content_digest",""))!=64 or len(negative.get("source_digest",""))!=64:raise AssertionError(negative)
    proof["final_config"]=read(client,address,reporter,"get_config");proof["result"]="PASS"
    out=Path(__file__).resolve().parents[1]/"docs"/"studionet-e2e.json";out.write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8");print(json.dumps(proof,indent=2),flush=True)
if __name__=="__main__":main()
