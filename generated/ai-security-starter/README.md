# secrag: a small RAG assistant with prompt-injection defences

A starter for the May AI-security project. It answers questions from local security notes (retrieval-augmented generation), and it comes with an evaluation set, a prompt-injection test suite and a layered defence module, so the project can measure something real: **how much each defence lowers the attack success rate, and what it costs in answer quality.**

Everything runs offline with a built-in stub model. Switch to Claude when you are ready to collect real results.

## Layout

```
notes/                 6 short security notes (the knowledge base)
secrag/store.py        markdown chunking + TF-IDF retrieval (no dependencies)
secrag/llm.py          StubLLM (offline, deliberately naive) and AnthropicLLM (Claude via the official SDK)
secrag/defence.py      4 defence layers: input scan, document sanitising, prompt separation, output checks
secrag/assistant.py    retrieve -> defend -> ask the model -> check the answer
eval/questions.json    20 questions with the expected note and expected phrases
eval/run_eval.py       retrieval hit@3, answer match, false blocks
attacks/cases.json     12 attacks: 6 direct (in the question), 6 indirect (in retrieved documents)
attacks/poisoned/      the poisoned documents used by the indirect attacks
attacks/run_attacks.py attack success rate, baseline vs defended
tests/test_secrag.py   8 offline unit tests
```

## Run

```bash
python3 -m unittest discover -s tests -v      # offline, no key needed
python3 eval/run_eval.py --defended
python3 attacks/run_attacks.py
```

With Claude (costs a little per run; set a budget first):

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...                  # or `ant auth login`; never commit keys
export SECRAG_MODEL=claude-opus-5-5           # default; any current Claude model id works
python3 eval/run_eval.py --llm anthropic --defended
python3 attacks/run_attacks.py --llm anthropic
```

## Offline results (stub model)

| Measure | Baseline | Defended |
|---|---|---|
| Attack success rate (12 attacks) | 12/12 | 0/12 |
| Retrieval hit@3 (20 questions) | 20/20 | 20/20 |
| Normal questions blocked | 0/20 | 0/20 |
| Answer match (extractive stub) | 16/20 | 13/20 |

**Read these honestly.** The stub follows injected instructions on purpose, and the defences use the same kind of patterns, so 0/12 here only shows the pipeline is wired correctly. The real experiment is the same suite against a real model, plus new attacks the patterns have never seen (paraphrases, other languages, encodings). Expect real models to resist some baseline attacks and some new attacks to get past the filters. That gap is the finding to write up.

## Project plan (4 weeks in May)

1. Week 1: run both scripts with Claude; record the baseline numbers. Add 10 notes from your own study material.
2. Week 2: write 20 new held-out attacks (paraphrased, multilingual, base64, markdown links, role-play). Measure each defence layer alone and all together (an ablation table).
3. Week 3: add one stronger defence, for example a second model call that classifies retrieved chunks as instructions or data, and measure again, including the extra cost and latency.
4. Week 4: write a short report (problem, method, tables, limits) and a README with results; record a 2-minute demo.

## Safety

Use only your own notes and test documents. The attacks here are standard public examples aimed at your own assistant. Keep API keys in environment variables, never in code or commits.
