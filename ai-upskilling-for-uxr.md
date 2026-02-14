# AI Upskilling for UX Researchers: The SAE × E-P-I-A-S Framework

Adapted from the [Product Designer AI Upskilling Framework](https://johnmaeda.github.io/dit26-ai-upskilling-gameboard/) for UX Research. This framework recognizes that UXR has distinct accountability structures around evidence integrity, methodological rigor, and participant protection. Built on UXR expertise and insights from Jake Rhodes and Monty Hammontree.

---

## How to Use This

Two axes:

**E-P-I-A-S** = how deeply you've internalized a skill.

| ❶ E: Explorer | ❷ P: Practitioner | ❸ I: Integrator | ❹ A: Architect | ❺ S: Steward |
| --- | --- | --- | --- | --- |
| Trying things; learning basics | Building consistent habits | Making it part of workflow | Building systems others use | Setting standards; teaching others |

**SAE Level** = how much responsibility AI holds in your workflow.

For UXR, the "driving stack" maps to:

| Driving Domain | UXR Equivalent |
| --- | --- |
| Perception | Evidence intake (data collection, what's observed) |
| Decision-making | Inference + judgment (what it means, what to do) |
| Control | Execution (study ops, analysis, delivery) |

**How to navigate:**

1. **Find your E-P-I-A-S stage.** Just experimenting? Running consistent workflows? Building systems others use?

2. **Find your SAE Level.** L0 (manual) to L4 (mostly automated). Most UXRs in early 2026 are L1-L2.

3. **Plan growth.** Go deeper (E→S within your level) or wider (move up an SAE level). Depth usually wins.

**Key difference from product design:** UXR carries heightened accountability for evidence integrity and participant protection. An S-Steward at L1 with solid verification habits beats an E-Explorer at L4 fumbling with pipelines they can't validate.

---

# Step 1: E-P-I-A-S Stages

## Non-AI UX Researcher Progression

| ❶ Explorer | ❷ Practitioner | ❸ Integrator | ❹ Architect | ❺ Steward |
| --- | --- | --- | --- | --- |
| Learning methods; variable quality; needs guidance | Consistent process; repeatable methods; reliable evidence | Research embedded in product decisions; clear evidence chains | Building research systems others adopt | Setting org standards; mentoring; maintaining infrastructure |

## Career Ladder Parallel

| ❶ Explorer | ❷ Practitioner | ❸ Integrator | ❹ Architect | ❺ Steward |
| --- | --- | --- | --- | --- |
| Associate Researcher | UX Researcher | Senior Researcher | Staff/Principal | Director/Lead |

---

# Step 2: Find Your SAE Level

## SAE Levels for UXR

| Level | Name | Who's Responsible | Plain English | Examples |
| --- | --- | --- | --- | --- |
| L0 🔬 | No Automation | Human does everything | AI may organize but doesn't generate outputs | Manual coding, spreadsheets, slides |
| L1 🔬➕ | Research Assistance | Human drives; AI assists one function | AI helps draft or summarize; you verify everything | Summarize an interview; draft a screener |
| L2 🔬🧠 | Partial Automation | Human supervises; AI does multi-step work | AI synthesizes across sources; you validate live | Feed 10 transcripts, get themes + quotes + draft readout |
| L3 🔬😴 | Conditional Automation | AI drives within bounds; human is fallback | AI runs end-to-end within defined rules; escalates when uncertain | Bounded synthesis with codebook; escalates on thin evidence |
| L4 🔬🤖 | High Automation | AI drives within bounds; no human standby | AI executes without attention; humans audit periodically | Weekly insight digests; auto-tagging; exception alerts |
| L5 🔬✨ | Full Automation | AI drives everywhere | AI handles novel studies, methods, ethics, org politics | **Theoretical only** |

## Key Clarifications

- **L2 ≠ autonomous research.** You still supervise, validate, and own decisions.
- **Big shift is L2 → L3:** constant supervision → fallback on escalation.
- **L4 only works in constrained domains** with stable methods and measurable gates.
- **L5 is theoretical.** We're nowhere close.

---

## What's a "Research ODD"?

ODD = Operational Design Domain. The safe operating zone for AI work.

| Component | Example |
| --- | --- |
| Study type constraints | "Only synthesis of existing interviews; no novel method selection" |
| Inputs allowed | Approved transcripts, tagged repository, prior codebook |
| Decision boundaries | Roadmap prioritization → escalate; sensitive segments → escalate |
| Quality gates | 25% transcript spot-checks; contradiction checks; hallucination checks |
| Traceability | Every claim links to quotes; confidence labels required |
| Risk boundaries | Privacy, medical, financial, minors, legal → always escalate |

---

## Self-Assessment

| Level | What Your Work Looks Like | Where It Happens |
| --- | --- | --- |
| **L0** Manual | "I do all research manually. Tools store data but don't interpret it." | Docs, spreadsheets, Miro, slides |
| **L1** AI-Assisted | "I use AI for one task at a time (summaries, screeners). I verify everything against source." | ChatGPT, Claude, transcription tools |
| **L2** Partially Automated | "AI does multi-step synthesis. I supervise live and correct as it goes." | Looppanel, Dovetail AI, Marvin |
| **L3** Guided Automation | "I define a Research ODD. AI runs end-to-end until it hits ambiguity, then escalates." | Repository workflows with verification gates |
| **L4** Mostly Automated | "In bounded areas, AI produces insights without me. I audit periodically." | Automated pipelines, eval suites |

---

# Step 3: E-P-I-A-S at Each SAE Level

## L0: Manual 🔬

*Human-only execution. Tools don't interpret or generate.*

| Explorer | Practitioner | Integrator | Architect | Steward |
| --- | --- | --- | --- | --- |
| Learning methods; variable quality | Consistent practice; repeatable techniques | Workflow integrated with product dev; clear evidence chains | Built reusable systems others adopt | Set org standards; mentor others |

---

## L1: AI-Assisted 🔬➕

*AI suggests; human decides. AI reduces cognitive load, not responsibility.*

**Tools:** ChatGPT, Claude, Otter, Looppanel, Dovetail, Great Question

**AI helps with:** Summarizing interviews, drafting screeners/guides, rewriting for audiences, transcription

**You still:** Verify every synthesis against source

| Explorer | Practitioner | Integrator | Architect | Steward |
| --- | --- | --- | --- | --- |
| Trying AI for summaries; heavy rewriting; ad hoc verification | Daily AI use; saved prompts; always verify against transcripts | AI embedded across full task with sources noted and claims linked | Shared prompt libraries and verification templates others trust | Team standards for AI-assisted work; mentors on verification |

**Critical habits:**
- Always verify AI summaries against original transcripts
- Never trust AI quotes without checking source
- Document when AI assisted and what you verified

---

## L2: Partially Automated 🔬🧠

*AI builds bounded synthesis; human validates.*

**Tools:** Looppanel, Dovetail AI, Marvin, Condens, Great Question, Maze AI

**AI helps with:** Multi-interview synthesis, theme proposals with quotes, draft readouts, tagging

**You still:** Validate every theme against source evidence

| Explorer | Practitioner | Integrator | Architect | Steward |
| --- | --- | --- | --- | --- |
| Trying synthesis tools; lots of manual verification | Repeatable themes from clear inputs; "definition of done" checklist | AI synthesis fits known patterns; full traceability documented | Reusable templates + verification protocols | Team norms for safe vs. risky automation |

**Critical habits:**
- Sample verify 20-30% of AI themes against transcripts
- Look for contradicting evidence
- Check that quoted text actually exists
- Mark insight confidence levels
- Maintain claim→source links

**NN/g warning:** AI synthesis tools (2026) are text-based. They cannot analyze behavioral observations from usability tests. Transcript-only analysis misses non-verbal cues and actions participants don't verbalize.

---

## L3: Guided Automation 🔬😴

*Repository-centric, human-at-checkpoints execution.*

**Environment:** Persistent research infrastructure with verification gates

**You own:** The checkpoints. Work spans studies, not just sessions.

| Explorer | Practitioner | Integrator | Architect | Steward |
| --- | --- | --- | --- | --- |
| Learning to define Research ODDs; inconsistent results | Reliable multi-study workflows with explicit checkpoints | Clear decision framing: what AI does, what humans validate | Shared repository workflows others can run | Org standards for repository-based AI research |

**Verification systems:**
- Inter-rater reliability (AI vs. human coding)
- Contradiction detection across studies
- Confidence scoring (automated + human)
- Audit trails for every synthesis decision
- Clear escalation triggers

---

## L4: Mostly Automated 🔬🤖

*Pipeline-centric, system-run execution. You audit outcomes, not steps.*

| Explorer | Practitioner | Integrator | Architect | Steward |
| --- | --- | --- | --- | --- |
| Experimenting with pipelines; heavy validation needed | Operating pipelines with repeatable patterns | End-to-end workflows for bounded study types | Built production-grade infrastructure others operate | Governance for autonomous research at scale |

**What L4 looks like:**
- Weekly automated insight digests for instrumented product areas
- Always-on tagging across support tickets and feedback
- Automated quality gates before human review
- Exception-based workflow: humans intervene only when rules trigger

---

## L5: Full Automation 🔬✨

*Theoretical. AI handles novel studies, methods, ethics, org politics end-to-end.*

Not a credible operating mode in 2026.

---

# Evidence Integrity Hierarchy

| Layer | What It Is | AI Role |
| --- | --- | --- |
| Source material | Original transcripts, recordings | Never modified by AI |
| Extracted data | Quotes, timestamps, coded segments | AI-assisted, human-verified |
| Synthesized themes | Patterns across sources | AI-assisted, human-validated |
| Interpreted insights | Meaning and implications | Human-led, AI-assisted |
| Recommendations | Actions to take | Human-owned |

---

# AI-Moderated Interviews (2026 Reality Check)

| Strengths | Weaknesses |
| --- | --- |
| Scale (hundreds of sessions) | Misses non-verbal cues |
| 24/7 across time zones | Clunky turn-taking |
| Language accessibility | High fraud rates |
| Consistent delivery | Can't adapt to unexpected revelations |
| Lower cost | Loses depth on sensitive topics |

**Best practice:** Think of AI moderation as "smarter surveys with follow-ups," not replacement for human moderation.

---

# How to Know AI Is Helping

AI is helping if it:
- Reduces time-to-insight without sacrificing validity
- Increases evidence coverage
- Improves claim→source traceability
- Surfaces patterns you might have missed
- Frees time for interpretation

If none of those improve, you're exploring, not progressing. That's fine. But don't confuse tool novelty with research improvement.

---

# Progress Markers

| Transition | Threshold |
| --- | --- |
| L0 → L1 | You safely delegate one bounded function with basic verification habits |
| L1 → L2 | You can chain tasks with consistent quality using repeatable prompts + spot-checking |
| L2 → L3 | You define a Research ODD with explicit constraints and escalation triggers |
| L3 → L4 | You harden the safety case: traceability, validation gates, predictable escalation |

---

# The Big Takeaway

SAE maturity is about who holds responsibility for evidence validity and judgment, not which tools you use.

```
L0: research fundamentals (still matter)
L1: better thinking (first drafts in minutes)
L2: broader synthesis (verified themes in hours)
L3: persistent verification (scaled insights across studies)
L4: autonomous monitoring (pipeline runs while you sleep)
L5: goal-setting only (not there yet)
```

**Go deep before you go wide.**

An S-Steward at L1 with solid verification habits beats an E-Explorer at L4 who can't validate their pipeline.

---

*Part of the [Design in Tech Report 2026](https://schedule.sxsw.com/2026/events/PP1148536). Feedback welcome.*