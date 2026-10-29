<div align="center">

# isilicon

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=22&pause=1200&color=7EE0FF&center=true&vCenter=true&width=680&height=40&lines=Embedded+security;Red+teaming+and+AI+security;Agents+that+use+computers;Distilling+big+models+into+small+ones)](https://git.io/typing-svg)

I build things that fail closed.

https://huggingface.co/isilicon
https://pirateface.co/isilicon

<br/>

![C](https://img.shields.io/badge/C-00599C?style=flat-square&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![WebGPU](https://img.shields.io/badge/WebGPU-005A9C?style=flat-square&logo=webgpu&logoColor=white)
![Electron](https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![FIDO2](https://img.shields.io/badge/FIDO2%20%2F%20CTAP2-000000?style=flat-square)

</div>

## Interests

- Embedded and hardware security (bootloaders, authenticators, constrained devices)
- Red teaming, LLM jailbreaking, and AI security research
- Agent tooling and computer-use agents
- ML training, distillation, and efficiency
- Multi-device audio systems

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
