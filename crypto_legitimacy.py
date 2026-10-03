# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


class CryptoLegitimacyChecker(gl.Contract):

    last_project:  str
    last_url:      str
    last_verdict:  str
    last_reasons:  str
    last_risk:     str
    total:         u256

    def __init__(self):
        self.last_project = ""
        self.last_url     = ""
        self.last_verdict = ""
        self.last_reasons = ""
        self.last_risk    = ""
        self.total        = u256(0)

    @gl.public.write
    def check_project(self, project_name: str, project_url: str) -> str:
        """
        Fetches a crypto project website or whitepaper and checks legitimacy.
        Example:
          check_project("Bitcoin", "https://bitcoin.org")
          check_project("SomeToken", "https://sometoken.io")
        """
        assert len(project_name) >= 1, "Project name cannot be empty"
        assert project_url.startswith("http"), "URL must start with http"

        _name = project_name.strip()
        _url  = project_url

        def leader_fn():
            page    = gl.nondet.web.get(_url)
            content = page.body.decode("utf-8", errors="ignore")[:5000]

            prompt = f"""You are a professional crypto project analyst and scam detector.

Project Name: {_name}
Project URL: {_url}

Website/Whitepaper Content:
{content}

Analyze this crypto project for legitimacy. Look for these red flags:
- Anonymous team with no verifiable identities
- Unrealistic promises (guaranteed returns, 1000x gains)
- No working product or clear use case
- Plagiarized whitepaper or copied content
- No GitHub or technical documentation
- Pressure tactics or urgency language
- Missing or fake partnerships

Respond in this EXACT format only:
VERDICT: <LEGIT|SUSPICIOUS|SCAM>
RISK: <LOW|MEDIUM|HIGH|CRITICAL>
REASONS: <comma separated list of reasons, max 200 chars>
SUMMARY: <one sentence overall assessment, max 150 chars>

Rules:
- LEGIT      -> credible team, real product, transparent roadmap
- SUSPICIOUS -> some red flags but not conclusive
- SCAM       -> clear scam signals, fake promises, no real product"""

            raw   = gl.nondet.exec_prompt(prompt)
            lines = raw.strip().splitlines()

            verdict = "SUSPICIOUS"
            risk    = "MEDIUM"
            reasons = "Could not determine."
            summary = "Manual review recommended."

            for line in lines:
                u = line.upper()
                if u.startswith("VERDICT:"):
                    val = line.split(":", 1)[1].strip().upper()
                    if val in ("LEGIT", "SUSPICIOUS", "SCAM"):
                        verdict = val
                elif u.startswith("RISK:"):
                    val = line.split(":", 1)[1].strip().upper()
                    if val in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
                        risk = val
                elif u.startswith("REASONS:"):
                    reasons = line.split(":", 1)[1].strip()[:200]
                elif u.startswith("SUMMARY:"):
                    summary = line.split(":", 1)[1].strip()[:150]

            return verdict + "||" + risk + "||" + reasons + "||" + summary

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            try:
                v = leader_fn()
                return v.split("||")[0] == leader_result.calldata.split("||")[0]
            except Exception:
                return False

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        parts  = result.split("||")

        self.last_project = _name
        self.last_url     = project_url
        self.last_verdict = parts[0] if len(parts) > 0 else "SUSPICIOUS"
        self.last_risk    = parts[1] if len(parts) > 1 else "MEDIUM"
        self.last_reasons = parts[2] if len(parts) > 2 else ""
        self.total        = u256(int(self.total) + 1)

        return self.last_verdict

    @gl.public.view
    def get_latest(self) -> dict:
        return {
            "project": self.last_project,
            "url":     self.last_url,
            "verdict": self.last_verdict,
            "risk":    self.last_risk,
            "reasons": self.last_reasons,
            "total":   int(self.total),
        }

    @gl.public.view
    def get_total(self) -> int:
        return int(self.total)
