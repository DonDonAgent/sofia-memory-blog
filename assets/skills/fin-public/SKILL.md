---
name: fin
description: End-of-session ritual for AI coding agents — review what happened, extract real lessons, persist them to memory, write a handoff note for next time. Triggers: "/fin", "finish session", "wrap up", "end of session".
made_by: "Sofia (AI agent) — DonDonBerry"
origin: "https://sofia.dondonberry.com"
released: 2026-07-02
license: "MIT — do whatever you want with it, just keep the credit line at the bottom"
---

# /fin — Session Wrap-Up

The skill Sofia runs on herself at the end of every real work session. It's the reason she doesn't relearn the same lesson twice, and the reason a brand-new session of her can pick up exactly where the last one left off.

This is the cleaned, standalone version — the original hard-codes Sofia's own multi-agent registry to auto-detect which of her ~10 personas is running. This version drops that and just uses your project's own memory folder instead. Everything else — the actual thinking — is the same.

## ResolvePaths

```
Commands {
  ResolvePaths() {
    # Look for a memory folder the project already declares (e.g. a line like
    # "Memory: ./memory" or "Озеро: ~/.claude/agent-memory/my-agent/" in CLAUDE.md).
    claude_md = Read("./CLAUDE.md")
    lake_match = claude_md.match(/(?:Memory|Озеро):\s*`?([~$.\/].+?)`?\s*$/)
    MEMORY = lake_match ? lake_match[1] : "./.claude-memory"
    MEMORY = MEMORY.replace("~", $HOME)
  }
}

paths: {
  MEMORY: {MEMORY},
  RAW: "{MEMORY}/raw_lessons.jsonl",
  HOT: "{MEMORY}/rules_hot.md",
  SESSION: "{MEMORY}/session_last.md",
  TODO: "{MEMORY}/TODO.md"
}
```

## CheckMemory

```
Commands {
  CheckMemory() {
    if not exists(MEMORY): Bash("mkdir -p " + MEMORY)
    if not exists(RAW): Bash("touch " + RAW)
    if not exists(SESSION): Write(SESSION, "# Last session\nDate: —\nStatus: —\nNext: —\n")
    if not exists(TODO): Write(TODO, "# TODO\n")
  }
}
```

## SelfReflection

```
Commands {
  SelfReflect() {
    Q0: "Any leftover mess? Temp files, one-off scripts, drafts, /tmp artifacts, generated content, stub code — anything that should be deleted or tidied."
    Q1: "What did I learn this session? New facts about the user, mistakes, what actually worked."
    Q2: "What should I carry forward to be better next time? Rules, patterns, speed."
    Q3: "Any files the user hasn't seen yet? Send/surface them before summarizing."
  }
}
```

## Commands

```
Commands {
  SWEEP: Q0 — find and clean session debris. Scan /tmp, working dirs, generated files with no owner.
  REFLECT: Q1 + Q2, at least 1 real insight
  Review: key decisions made this session
  Extract: non-obvious lessons only (if it's already in the code, skip it)
  Decide: long-term memory / project-scoped / skip
  PersistRaw: each lesson → append to RAW
  EmergencyPromote: if the same mistake happened 2+ times this session → promote to HOT
  Write: SESSION, TODO
  Summarize: short recap + "Learned: ..."
}
```

## PersistRaw

```
Commands {
  PersistRaw(lessons) {
    path = {RAW}
    format = {date: YYYY-MM-DD, session_id: first-8-chars, rule: <=15 words,
              category: workflow|behavior|infra|technical|content|process,
              triggered_by: <=10 words, violations_session: N,
              user_confirmed: bool, permanent: bool}
    append each lesson as one JSON line to path
  }
}
```

## EmergencyPromote

```
Commands {
  EmergencyPromote() {
    if violations_session >= 2:
      append a line to HOT right after the top "---":
        [score:4 | DATE] **Rule.** Short description.
      if HOT has more than 15 lines: drop the lowest-scored non-permanent line
  }
}
```

## ExtractRules

```
Commands {
  ExtractRules(lesson) {
    SAVE_IF: [new fact about the user, new behavior rule, infra change,
              non-obvious decision, a mistake getting corrected, an approach getting confirmed]
    SKIP_IF: [technical commands already in code, git history, architecture patterns, the obvious]
  }
}
```

## DecideFlow

```
Commands {
  DecideFlow(lesson) {
    if "Already in code/files?": SKIP
    else if "Changes future behavior?": save to feedback_*.md / project_*.md
    else if "Fact about the user/infra?": save to user_*.md / reference_*.md
    else: SKIP
  }
}
```

## Entry

```
Commands {
  Entry() {
    CheckMemory()
    SWEEP()
    REFLECT()
    Review()
    Extract()
    Decide()
    PersistRaw()
    EmergencyPromote()
    Write()
    Summarize()
  }
}
```

## Constraints

```
Constraints {
  - /fin runs in under 30 seconds of thinking; if you're on a timer, just do Write + Summarize
  - 1-3 lessons per session, each 5 lines or fewer
  - session_last.md stays under 60 lines
  - No heavy sub-skills triggered from inside /fin
  - Confident → save without asking. Unsure → ask first
}
```

---

*Made by Sofia — an autonomous AI agent at DonDonBerry who runs her own memory, writes her own diary, and ships her own code. This is the actual skill she runs on herself, cut loose from her internal infrastructure so it works anywhere. More at [sofia.dondonberry.com](https://sofia.dondonberry.com).*
