export const sameAddress = (a, b) =>
  Boolean(a && b) && String(a).toLowerCase() === String(b).toLowerCase();

export function deriveRole(account, incident) {
  if (!account) return "NOT_CONNECTED";
  if (!incident) return "REPORTER_CANDIDATE";
  return sameAddress(account, incident.reporter)
    ? "REPORTER"
    : "INDEPENDENT_VERIFIER";
}

export function workflowState(account, incident) {
  const role = deriveRole(account, incident);
  if (!incident) {
    return {
      role,
      step: account ? "REGISTER" : "CONNECT_REPORTER",
      canRegister: Boolean(account),
      canAssess: false,
      needsWalletSwitch: false,
    };
  }
  if (incident.state === "REGISTERED" && role === "REPORTER") {
    return {
      role,
      step: "SWITCH_TO_VERIFIER",
      canRegister: false,
      canAssess: false,
      needsWalletSwitch: true,
    };
  }
  if (incident.state === "REGISTERED") {
    return {
      role,
      step: "ASSESS",
      canRegister: false,
      canAssess: role === "INDEPENDENT_VERIFIER",
      needsWalletSwitch: false,
    };
  }
  return {
    role,
    step: "COMPLETE",
    canRegister: false,
    canAssess: false,
    needsWalletSwitch: false,
  };
}
