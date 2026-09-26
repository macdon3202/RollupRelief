import test from'node:test';import assert from'node:assert/strict';import{normalizeHash,receiptState}from'./src/transactions.js';
test('normalizes SDK tx shapes',()=>{const h='0x'+'a'.repeat(64);assert.equal(normalizeHash({txId:h}),h);assert.equal(normalizeHash(h),h)});
test('accepts finalized success',()=>assert.equal(receiptState({statusName:'FINALIZED',execution_result:'SUCCESS'}).accepted,true));
test('does not hide execution error',()=>assert.equal(receiptState({statusName:'FINALIZED',execution_result:'ERROR'}).failed,true));
test('keeps accepted transaction pending until finalization',()=>assert.deepEqual(receiptState({statusName:'ACCEPTED',execution_result:'SUCCESS'}),{label:'ACCEPTED',accepted:false,failed:false,reason:null}));
test('treats undetermined consensus as failure',()=>assert.equal(receiptState({statusName:'UNDETERMINED'}).failed,true));
