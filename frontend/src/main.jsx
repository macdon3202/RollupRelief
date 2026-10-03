import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { ADDRESS, EX, connect, read, wait, write } from "./genlayer.js";
import { workflowState } from "./role-workflow.js";
import "./style.css";
import "./review-links.css";
import "./handoff.css";

const FIXTURE = "cmrazrvph0am30rns9tzwb2oa";
const short = (value) => value ? `${String(value).slice(0, 7)}…${String(value).slice(-5)}` : "—";

function App() {
  const [wallet, setWallet] = useState(null);
  const [id, setId] = useState(FIXTURE);
  const [chain, setChain] = useState("OP_MAINNET");
  const [item, setItem] = useState(null);
  const [config, setConfig] = useState(null);
  const [busy, setBusy] = useState("");
  const [notice, setNotice] = useState("Ready to inspect an official incident.");
  const url = `https://status.optimism.io/en-us/${id}`;
  const flow = useMemo(() => workflowState(wallet?.account, item), [wallet?.account, item]);

  const sync = async () => {
    setBusy("sync");
    try {
      setConfig(await read("get_config"));
      setItem(await read("get_incident", [id]));
      setNotice("Authoritative state synchronized.");
    } catch (error) {
      setItem(null);
      setNotice(error.message);
    } finally { setBusy(""); }
  };

  const chooseWallet = async (force = false) => {
    try {
      const next = await connect(force);
      setWallet(next);
      setNotice(force ? `Active account changed to ${short(next.account)}. Re-check the role before signing.` : `Wallet ${short(next.account)} connected.`);
    } catch (error) { setNotice(error.message); }
  };

  useEffect(() => {
    if (ADDRESS) read("get_config").then(setConfig).catch((error) => setNotice(error.message));
  }, []);

  useEffect(() => {
    const provider = window.ethereum;
    if (!provider?.on) return undefined;
    const changed = () => chooseWallet(false);
    provider.on("accountsChanged", changed);
    return () => provider.removeListener?.("accountsChanged", changed);
  }, []);

  const tx = async (fn, args) => {
    if (!wallet) throw Error("Connect a wallet first.");
    setBusy(fn);
    try {
      const hash = await write(wallet, fn, args);
      setNotice(`Submitted ${short(hash)}`);
      await wait(hash, (state) => setNotice(`${fn}: ${state.label}`));
      await sync();
      setNotice(`${fn} finalized successfully; authoritative state re-read.`);
    } catch (error) { setNotice(error.message); }
    finally { setBusy(""); }
  };

  const roleLabel = flow.role.replaceAll("_", " ");
  const steps = [
    ["1", "Reporter", item ? "DONE" : wallet ? "READY" : "CONNECT"],
    ["2", "Register", item ? "DONE" : flow.canRegister ? "READY" : "WAITING"],
    ["3", "Switch wallet", item?.state === "REGISTERED" ? (flow.needsWalletSwitch ? "ACTION" : "DONE") : item ? "DONE" : "WAITING"],
    ["4", "Verifier", item?.state === "REGISTERED" ? (flow.canAssess ? "READY" : "WAITING") : item ? "DONE" : "WAITING"],
  ];

  return <>
    <header><div className="brand"><img src="/rollup-relief-logo.png" alt="RollupRelief"/><div><b>RollupRelief</b><span>Incident attestation registry</span></div></div><nav><a href="https://github.com/macdon3202/RollupRelief" target="_blank" rel="noreferrer">GitHub ↗</a><a href="https://github.com/macdon3202/RollupRelief/blob/main/docs/STUDIONET_V3_E2E.md" target="_blank" rel="noreferrer">E2E evidence ↗</a><a href={ADDRESS ? `${EX}/address/${ADDRESS}` : "#"} target="_blank" rel="noreferrer">Contract ↗</a></nav><button onClick={() => chooseWallet(Boolean(wallet))}>{wallet ? `Switch · ${short(wallet.account)}` : "Connect wallet"}</button></header>
    <main>
      <section className="hero"><div><span className="kicker">OPTIMISM · OFFICIAL STATUS EVIDENCE</span><h1>Was the rollup really<br/><em>unable to accept writes?</em></h1><p>Convert official incident narratives into bounded, replay-protected attestations that deadline-sensitive Web3 apps can query.</p><div className="role"><span>Connected role</span><b>{roleLabel}</b></div></div><div className="mark"><img src="/rollup-relief-logo.png" alt="RollupRelief mark"/><span>Permissionless two-wallet verification</span></div></section>
      <section className="stats"><div><span>Network</span><b>Studionet</b></div><div><span>Authority</span><b>{config?.authority || "OPTIMISM_STATUS"}</b></div><div><span>Incidents</span><b>{config?.incident_count ?? "—"}</b></div><div><span>Contract</span><b>{ADDRESS ? short(ADDRESS) : "Pending deploy"}</b></div></section>
      <section className="handoff"><div><span className="num">GUIDED TWO-WALLET HANDOFF</span><h2>Play both roles from this page</h2><p>Use account A to register. Then select a different account in your wallet and use account B to assess. The contract—not the UI—rejects self-verification.</p></div><div className="handoff-steps">{steps.map(([n, label, state]) => <article className={state.toLowerCase()} key={n}><span>{n}</span><div><b>{label}</b><small>{state}</small></div></article>)}</div><div className="identity"><span>Active wallet<b>{short(wallet?.account)}</b></span><span>On-chain reporter<b>{short(item?.reporter)}</b></span></div>{flow.needsWalletSwitch && <button onClick={() => chooseWallet(true)}>Switch to verifier wallet</button>}</section>
      <section className="work"><div className="panel"><span className="num">01 · INCIDENT INTAKE</span><h2>Bind the official notice</h2><label>Chain key<input value={chain} onChange={(event) => setChain(event.target.value)}/></label><label>Incident ID<input value={id} onChange={(event) => setId(event.target.value)}/></label><label>Canonical source<input readOnly value={url}/></label><button disabled={busy || !flow.canRegister} onClick={() => tx("register_incident", [chain, id, url])}>Register as reporter</button><button className="ghost" disabled={busy} onClick={sync}>Sync existing incident</button><small>Any wallet may register an unused canonical incident. The registered reporter cannot assess that same incident.</small></div>
        <div className="panel result"><div className="head"><div><span className="num">02 · CONSENSUS ATTESTATION</span><h2>Operational impact</h2></div><span className={`badge ${item?.state || ""}`}>{item?.state || "NOT LOADED"}</span></div>{item ? <><div className="impact"><article><span>Affected operation</span><b>{item.affected_operation || "PENDING"}</b></article><article><span>Impact</span><b>{item.impact_level || "PENDING"}</b></article><article className={item.qualifies_for_relief ? "yes" : "no"}><span>Relief eligibility</span><b>{item.qualifies_for_relief ? "QUALIFIES" : "DOES NOT QUALIFY"}</b></article></div><dl><dt>Reporter</dt><dd>{item.reporter}</dd><dt>Reason code</dt><dd>{item.reason_code || "Awaiting assessment"}</dd><dt>Content digest</dt><dd>{item.content_digest || "Not sealed"}</dd><dt>Evidence bundle</dt><dd>{item.source_digest || "Not sealed"}</dd><dt>Revision</dt><dd>{String(item.revision)}</dd></dl><button disabled={busy || !flow.canAssess} onClick={() => tx("assess_incident", [id])}>Assess as independent verifier</button>{flow.needsWalletSwitch && <small>This account is the reporter. Switch to a different wallet account to enable assessment.</small>}</> : <div className="empty">Register or sync an incident to reveal its attestation timeline.</div>}</div></section>
      <section className="method"><span className="num">03 · PROOF MODEL</span><h2>One official source.<br/>Any two independent wallets.</h2><div>{[["01", "Bind", "Exact Optimism origin and incident ID."], ["02", "Fetch", "Validators independently retrieve the page."], ["03", "Classify", "Consensus distinguishes write outage from maintenance."], ["04", "Seal", "Digest, outcome and revision become queryable state."]].map((entry) => <article key={entry[0]}><b>{entry[0]}</b><h3>{entry[1]}</h3><p>{entry[2]}</p></article>)}</div></section>
      <section className="review-links"><div><span className="num">04 · REVIEW LINKS</span><h2>Verify the complete submission.</h2><p>Direct public links to source, deployed contract, two-wallet test and transaction-level Studionet evidence.</p></div><div><a href="https://github.com/macdon3202/RollupRelief" target="_blank" rel="noreferrer"><b>Source repository</b><span>github.com/macdon3202/RollupRelief ↗</span></a><a href="https://github.com/macdon3202/RollupRelief/blob/main/docs/FRONTEND_TWO_WALLET_E2E.md" target="_blank" rel="noreferrer"><b>Two-wallet frontend proof</b><span>Reporter → account switch → verifier ↗</span></a><a href="https://github.com/macdon3202/RollupRelief/blob/main/docs/STUDIONET_V3_E2E.md" target="_blank" rel="noreferrer"><b>V3 E2E ledger</b><span>Happy, negative, conflict and rollback paths ↗</span></a><a href={ADDRESS ? `${EX}/address/${ADDRESS}` : "#"} target="_blank" rel="noreferrer"><b>Studionet contract</b><span>{ADDRESS || "Not configured"} ↗</span></a></div></section>
    </main>
    <footer><span>{notice}</span><span>{busy ? "Working…" : "Post-write readback required"}</span></footer>
  </>;
}

createRoot(document.getElementById("root")).render(<App/>);
