import test from'node:test';import assert from'node:assert/strict';import{normalizeHash,receiptState}from'./src/transactions.js';
import{deriveRole,workflowState}from'./src/role-workflow.js';
test('normalizes SDK tx shapes',()=>{const h='0x'+'a'.repeat(64);assert.equal(normalizeHash({txId:h}),h);assert.equal(normalizeHash(h),h)});
test('accepts finalized success',()=>assert.equal(receiptState({statusName:'FINALIZED',execution_result:'SUCCESS'}).accepted,true));
test('does not hide execution error',()=>assert.equal(receiptState({statusName:'FINALIZED',execution_result:'ERROR'}).failed,true));
test('keeps accepted transaction pending until finalization',()=>assert.deepEqual(receiptState({statusName:'ACCEPTED',execution_result:'SUCCESS'}),{label:'ACCEPTED',accepted:false,failed:false,reason:null}));
test('treats undetermined consensus as failure',()=>assert.equal(receiptState({statusName:'UNDETERMINED'}).failed,true));
test('two-wallet frontend workflow hands registration from reporter to verifier',()=>{
 const reporter='0x'+'a'.repeat(40),verifier='0x'+'b'.repeat(40);
 assert.deepEqual(workflowState(reporter,null),{role:'REPORTER_CANDIDATE',step:'REGISTER',canRegister:true,canAssess:false,needsWalletSwitch:false});
 const registered={reporter,state:'REGISTERED'};
 assert.deepEqual(workflowState(reporter,registered),{role:'REPORTER',step:'SWITCH_TO_VERIFIER',canRegister:false,canAssess:false,needsWalletSwitch:true});
 assert.deepEqual(workflowState(verifier,registered),{role:'INDEPENDENT_VERIFIER',step:'ASSESS',canRegister:false,canAssess:true,needsWalletSwitch:false});
 assert.deepEqual(workflowState(verifier,{...registered,state:'ATTESTED'}),{role:'INDEPENDENT_VERIFIER',step:'COMPLETE',canRegister:false,canAssess:false,needsWalletSwitch:false});
});
test('address comparison is case-insensitive and reporter can never assess',()=>{
 const reporter='0xAbCd000000000000000000000000000000000000';
 assert.equal(deriveRole(reporter.toLowerCase(),{reporter,state:'REGISTERED'}),'REPORTER');
 assert.equal(workflowState(reporter.toUpperCase(),{reporter,state:'REGISTERED'}).canAssess,false);
});
