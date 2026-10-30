<div align="center">

<img src="assets/hero.svg" alt="isilicon: security engineer building things that fail closed" width="100%"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1100&color=7EE0FF&center=true&vCenter=true&width=760&height=36&lines=Self-hosted+LLM+fleet+on+one+RTX+PRO+6000;12+model+configs+graded+on+one+matched+screen;Blind+two-grader+panel+%C2%B7+paired+CIs;Embedded+security+%C2%B7+FIDO2+%C2%B7+secure+boot;Red+teaming+and+AI+security;Agents+that+use+computers)](https://git.io/typing-svg)

<a href="https://huggingface.co/isilicon"><img src="https://img.shields.io/badge/Hugging%20Face-isilicon-FFB547?style=for-the-badge&logo=huggingface&logoColor=white&labelColor=0d1117" alt="Hugging Face"/></a>
<a href="https://huggingface.co/collections/isilicon/mango-tested-models-and-preservation-mirrors"><img src="https://img.shields.io/badge/Collection-24%20model%20repos-7EE0FF?style=for-the-badge&logo=huggingface&logoColor=white&labelColor=0d1117" alt="Mango collection"/></a>
<a href="https://pirateface.co/isilicon"><img src="https://img.shields.io/badge/PirateFace-seeding-B69CFF?style=for-the-badge&labelColor=0d1117" alt="PirateFace"/></a>
<a href="https://discord.gg/5n5YDbQCMy"><img src="https://img.shields.io/badge/Infinity-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white&labelColor=0d1117" alt="Infinity Discord"/></a>

<br/>

![C](https://img.shields.io/badge/C-00599C?style=flat-square&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white)
![llama.cpp](https://img.shields.io/badge/llama.cpp%20%C2%B7%20GGUF-1f2937?style=flat-square)
![MLX](https://img.shields.io/badge/MLX-000000?style=flat-square)
![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=flat-square&logo=aiohttp&logoColor=white)
![WebGPU](https://img.shields.io/badge/WebGPU-005A9C?style=flat-square&logo=webgpu&logoColor=white)
![Electron](https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![FIDO2](https://img.shields.io/badge/FIDO2%20%2F%20CTAP2-000000?style=flat-square)

</div>

## Now: Mango, a self-hosted LLM lab

One 96 GB RTX PRO 6000 serving a fleet of open-weight models to my own agents through an
OpenAI-compatible API, with every model measured on the same frozen benchmark before it gets a route.
The fleet uses uncensored / refusal-edited checkpoints, and they have to win on measured quality
and speed like anything else.

<img src="assets/mango-stats.svg" alt="12 configs graded, 3,232 per-question grades, 24 public HF repos, about 1.19 TB of weights preserved, one 96 GB RTX PRO 6000" width="100%"/>

<img src="assets/mango-architecture.svg" alt="Agents to ngrok to mango-server to TensorFold, Strata and llama.cpp engines on one RTX PRO 6000; evaluation loop from fair-bench through graders, blind panel and economics rule to Hugging Face cards and PirateFace" width="100%"/>

**What's interesting about it**

- **mango-server**: one asyncio process replacing a chain of three blocking proxies. Profiles lease the GPU one
  at a time (drain → switch), context windows grow and shrink by tier per request, and `reasoning_effort` maps to
  each engine's real levels. Thinking is always on and no token cap is imposed beyond the context window.
- **Three engines, one card**: TensorFold (MLX 4-bit + DFlash2 speculative drafter), Strata (GSQ quantized
  MoE with hot-expert GPU placement) and pinned llama.cpp builds (GGUF, MTP heads, `--fit` CPU offload for big MoEs).
- **fair-bench**: 404 frozen items weighted to what I actually use (human understanding, coding + cybersecurity,
  agentic work), 12 offline agent cases with injected malicious instructions, and a 22-prompt open-ended suite.
  The graders report Wilson intervals, paired bootstrap differences and an economics rule: a faster model only
  displaces a better one if it is within 3 points and at least 1.5× faster.
- **Blind panel**: Claude and Codex each freeze their ratings before the identity key is opened, and the two are averaged.
- **Wipe-proof**: the GPU host is ephemeral. Results checkpoint continuously, downloads are hash-pinned, and a
  one-cell recovery rebuilds runtime, weights and queue on a fresh host without rerunning finished work.

<img src="assets/mango-leaderboard.svg" alt="Leaderboard of 12 configurations, from Qwen3.8 Flash Next IQ4_XS at 84.19 down to Qwen3.8 27B Cyber v2 Q6_K at 66.98, with workload minutes" width="100%"/>

<details>
<summary><strong>Domain breakdown</strong> · where each model is strong</summary>

<br/>

<img src="assets/mango-domains.svg" alt="Heatmap of social/EQ, cyber, agentic, coding, instruction-following and general scores for 12 configurations" width="100%"/>

**What the numbers say so far**

- Flash Next IQ4_XS leads at 84.19 in 35 workload minutes and is the default under the economics rule.
  Qwen3.8 27B on MLX 4-bit finishes the same screen in 24 minutes at 80.64, which keeps it on the Pareto frontier
  as the fast resident model.
- Size didn't decide the order: Qwen3.5 122B (80.72) took 5× longer than the 27B for the same score, and
  MiMo V2.6 needed 220 minutes.
- Cyber-specialist Qwen 27B fine-tunes did *not* beat the general model on cyber here, and lost 26–31 points
  on social/EQ. Different lineages and draft heads mean that's a finding about those builds, not about quantization.
- Effort study on the 27B (full 403 valid items): xhigh 84.41 vs medium 82.87, paired 95% CI −1.71 to +4.82,
  at 4.46× the time, so medium stays the default. The blind panel gave 8.18 vs 7.77 out of 10.

</details>

<details>
<summary><strong>Public model repos</strong> · exact quants with test results on every card</summary>

<br/>

| Repo | What |
| --- | --- |
| [mango-qwen38-flashnext-iq4xs](https://huggingface.co/isilicon/mango-qwen38-flashnext-iq4xs) | Current leader · 84.19 |
| [mango-flashnext-orca-iq4xs-20261029](https://huggingface.co/isilicon/mango-flashnext-orca-iq4xs-20261029) | Flash Next, Orca build · 83.42 |
| [mango-deepseek41-gsq-iq2xs-uncensored](https://huggingface.co/isilicon/mango-deepseek41-gsq-iq2xs-uncensored) | DeepSeek V4.1 Flash, GSQ IQ2_XS for Strata · 83.19 |
| [mango-qwen38-27b-uncensored-mlx4](https://huggingface.co/isilicon/mango-qwen38-27b-uncensored-mlx4) | Fast resident model + effort study · 80.64 |
| [mango-qwen38-27b-gguf](https://huggingface.co/isilicon/mango-qwen38-27b-gguf) | 8 GGUF quants (Q2 to Q6) in one repo, general and Cyber lineages kept separate |
| [mango-qwen35-122b-q4](https://huggingface.co/isilicon/mango-qwen35-122b-q4) | Qwen3.5 122B A10B · 80.72 |
| [mango-mimo26-flash-mopd-uncensored-q3km](https://huggingface.co/isilicon/mango-mimo26-flash-mopd-uncensored-q3km) | MiMo V2.6 Flash · 79.39 |
| [mango-dflash2](https://huggingface.co/isilicon/mango-dflash2) | DFlash2 speculative drafter |

Everything else (GLM 5.3 Flash builds, Nanbeige, Cyber variants, drafters, tokenizers, queued candidates) is in the
[collection](https://huggingface.co/collections/isilicon/mango-tested-models-and-preservation-mirrors).
Every mirror keeps the original publisher's card, license and attribution. Torrents for preservation are on
[PirateFace](https://pirateface.co/isilicon).

</details>

## Interests

- Self-hosted inference: quantization, speculative decoding, MoE offload, serving many models from one GPU
- Model evaluation that holds up: frozen suites, paired statistics, blind grading
- Embedded and hardware security (bootloaders, authenticators, constrained devices)
- Red teaming, LLM jailbreaking, and AI security research
- Agent tooling and computer-use agents
- ML training, distillation, and efficiency

## Live demos

<table>
<tr>
<td width="50%" align="center">
<a href="https://github.com/isiliconx/spacebunny"><strong>spacebunny</strong></a><br/>
<a href="https://isiliconx.github.io/spacebunny/"><img src="assets/spacebunny.gif" alt="spacebunny site" width="100%"/></a><br/>
<sub>WebGPU three.js site · fifty offline graphics demos</sub>
</td>
<td width="50%" align="center">
<a href="https://github.com/isiliconx/spacebunny"><strong>neon plankton demo</strong></a><br/>
<img src="assets/spacebunny-demo.gif" alt="bioluminescent plankton WebGL demo" width="100%"/><br/>
<sub>73k GPU particles · curl-noise advection · WebGL2</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<a href="https://github.com/isiliconx/nextdrop"><strong>nextdrop</strong></a><br/>
<img src="assets/nextdrop.gif" alt="nextdrop LAN transfer UI" width="100%"/><br/>
<sub>Zero-storage LAN file transfer over authenticated Socket.IO</sub>
</td>
<td width="50%" align="center">
<strong>Quintet Director</strong><br/>
<img src="assets/quintet.gif" alt="Quintet Director web UI" width="100%"/><br/>
<sub>Multi-device computational mic array · source private</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<strong>Storo</strong><br/>
<img src="assets/storo.gif" alt="Storo vault UI" width="100%"/><br/>
<sub>E2E encrypted personal cloud · PWA / desktop / mobile</sub>
</td>
<td width="50%" align="center">
<a href="https://github.com/isiliconx/hardwarekeyemulator"><strong>hardwarekeyemulator</strong></a><br/>
<img src="assets/hke.gif" alt="CTAP2 selftest terminal" width="100%"/><br/>
<sub>Lab CTAP2 / FIDO2 software authenticator · selftests green</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<a href="https://github.com/isiliconx/infinity-codex-releases"><strong>Infinity</strong></a><br/>
<img src="assets/infinity.gif" alt="Infinity install and help" width="100%"/><br/>
<sub>Verified install · checksums · CLI help</sub>
</td>
<td width="50%" align="center">
<strong>Infinite</strong><br/>
<img src="assets/infinite-home.jpg" alt="Infinite desktop bridge" width="100%"/><br/>
<sub>Cross-platform MCP bridge for browser AI hosts</sub>
</td>
</tr>
</table>

## Selected work

| Project | What it is |
| --- | --- |
| [Mango on Hugging Face](https://huggingface.co/isilicon) | Self-hosted LLM fleet: 24 public model repos with exact-quant test results, charts and runtime guides |
| [hardwarekeyemulator](https://github.com/isiliconx/hardwarekeyemulator) | Lab CTAP2 / FIDO2 software authenticator with CTAPHID, Linux UHID transport, and a local WebAuthn RP |
| [hardwarekeyemulator-audit](https://github.com/isiliconx/hardwarekeyemulator-audit) | Security audit of the emulator: critical UV forge, AAGUID defect, remediations, and a differential that proves closures |
| [the-byte-of-87](https://github.com/isiliconx/the-byte-of-87) | Secure embedded design challenge (MITRE eCTF style): ChaCha20-Poly1305 + Ed25519 bootloader and update path on Tiva |
| [spacebunny](https://github.com/isiliconx/spacebunny) | WebGPU three.js site plus fifty offline self-contained graphics / simulation demos |
| [nextdrop](https://github.com/isiliconx/nextdrop) | Zero-storage LAN file transfer portal over authenticated Socket.IO; files relay in memory only |
| [infinity-codex-releases](https://github.com/isiliconx/infinity-codex-releases) | Verified Infinity binaries, installers, checksums, and offline USB bundles |

### the-byte-of-87 · secure boot / update

Two-pass update: Ed25519 over the header and ciphertext first, then ChaCha20-Poly1305 decrypt and tag check. Commit magic is `BOOT_MAGIC ^ diff` so a failed check cannot produce a bootable record. A monotone `min_ver` ratchet on its own flash page blocks rollback. Boot itself is crypto-free; the magic is the proof.

```mermaid
flowchart TD
  A[Power on / reset] --> B[lock_debug + lock_sram_xn]
  B --> C[recover_firmware from backup if needed]
  C --> D[sync_floor: raise min_ver ratchet]
  D --> E{Command}
  E -->|BOOT| F[boot_firmware: magic + size checks only]
  F --> G[Jump to firmware]
  E -->|UPDATE| H[Pass 1: parse 98B header]
  H --> I[Reject if ver below floor]
  I --> J[Stream Ed25519 verify + stage ciphertext]
  J --> K{Signature OK?}
  K -->|no| L[Reject · keep old image]
  K -->|yes| M[Pass 2: derive fw_key · decrypt pages]
  M --> N{Poly1305 tag OK?}
  N -->|no| L
  N -->|yes| O[Backup active FW + record]
  O --> P[Install decrypted image · write magic last]
  P --> Q[sync_floor · erase backup]
  Q --> E
```

## Private projects

Source private; demos available on request.

<details>
<summary><strong>Quintet</strong> · multi-device computational mic array</summary>

<br/>

Phones, laptops, and tablets as coordinated capture nodes with AI-driven placement and mixing (TypeScript / Rust / Swift). Director control surface, local coordinator, signed native pairing, and provenance-backed processing graphs.

<img src="assets/quintet.png" alt="Quintet Director session overview" width="100%"/>

```mermaid
flowchart LR
  D[Director web UI] -->|loopback API| C[Coordinator]
  C -->|signed pair / control| N1[Phone node]
  C --> N2[Laptop node]
  C --> N3[Tablet node]
  N1 -->|local master WAV| C
  N2 --> C
  N3 --> C
  C --> P[Clock fit · resample · mix]
  P --> V[Content-addressed vault]
  V --> X[Authentic / Natural / Enhanced exports]
```

<sub>source private; demos on request</sub>

</details>

<details>
<summary><strong>Infinity</strong> · MCP computer-use agent</summary>

<br/>

MCP computer-use agent across files, shell, browser, and desktop. Verified binaries, installers, and USB bundles at [infinity-codex-releases](https://github.com/isiliconx/infinity-codex-releases).

<img src="assets/infinity-help.png" alt="Infinity CLI help" width="100%"/>

```mermaid
flowchart LR
  H[ChatGPT / Claude / host] -->|MCP HTTPS/WSS| G[Infinity gateway]
  G --> A[Agent runtime]
  A --> F[Files · patch · search]
  A --> S[Shell · PTY]
  A --> B[Browser / CDP]
  A --> U[Desktop observe / input]
  A --> M[Memory · projects · plugins]
```

<sub>source private; demos on request</sub>

</details>

<details>
<summary><strong>Storo</strong> · encrypted personal cloud</summary>

<br/>

End-to-end encrypted personal cloud storage with PWA, desktop, and mobile clients. Chunked uploads, resumable queue, previews, sharing, and vault health.

<img src="assets/storo.png" alt="Storo vault file manager" width="100%"/>

```mermaid
flowchart TB
  C[Browser / PWA / desktop / mobile] -->|password-derived keys| E[AES-GCM in client]
  E -->|chunked blobs| W[Private storage webhook]
  C -->|account session| A[Account API]
  A --> D[(Vault metadata / shares)]
  C --> P[Previews · studio · recorder]
  C --> H[Vault health · dedupe · trash]
```

<sub>source private; demos on request</sub>

</details>

<details>
<summary><strong>Infinite</strong> · MCP bridge desktop app</summary>

<br/>

Cross-platform MCP bridge desktop app: a local permission boundary for browser AI hosts (files, shell, desktop, and companion extension).

<img src="assets/infinite-home.jpg" alt="Infinite permissions and health" width="100%"/>

```mermaid
flowchart LR
  AI[Browser AI host] -->|Secure MCP tunnel| T[Local Infinite app]
  T --> P[Permission gates]
  P --> F[Approved folder roots]
  P --> SH[Shell when enabled]
  P --> DT[Desktop tools]
  X[Companion extension] --> T
```

<sub>source private; demos on request</sub>

</details>

## Stats

<div align="center">

<img height="160" src="https://github-readme-stats.vercel.app/api?username=isiliconx&show_icons=true&count_private=true&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=7EE0FF&icon_color=7EE0FF&text_color=c9d1d9" alt="isiliconx GitHub stats"/>
<img height="160" src="https://streak-stats.demolab.com?user=isiliconx&theme=tokyonight&hide_border=true&background=0d1117&ring=7EE0FF&fire=7EE0FF&currStreakLabel=7EE0FF" alt="isiliconx streak"/>

</div>
