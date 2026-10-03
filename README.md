# CryptoLegitimacyChecker — GenLayer Intelligent Contract

An Intelligent Contract on **GenLayer Testnet Bradbury** that checks
whether a crypto project is LEGIT, SUSPICIOUS, or a SCAM by analyzing
its website or whitepaper using on-chain LLM inference.

## What it does

1. Fetches a crypto project website or whitepaper URL
2. Analyzes content for scam signals and red flags
3. Reaches consensus via Optimistic Democracy
4. Returns LEGIT / SUSPICIOUS / SCAM verdict on-chain

## Contract Methods

| Method | Type | Description |
|---|---|---|
| `check_project(project_name, project_url)` | write | Fetches project site, runs LLM, returns verdict |
| `get_latest()` | view | Returns last check result |
| `get_total()` | view | Total checks done |

## Deployment

- **Network:** GenLayer Testnet Bradbury
- **Contract address:** `0xEe16EF12161b27914D484B608ed2886b1Dc9d897`
- **Deploy tx:** `0x2574bac54459e5747366fa61df148c5d97704ea7b213751a195c78441b0fbab8`

## License
MIT
