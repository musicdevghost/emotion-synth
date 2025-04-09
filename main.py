import time
import ollama
from pyo import *
import ast
import re
import random

s = Server().boot()
s.start()
print("Audio server started.")

loading_osc = Sine(freq=220, mul=0.2).out()
time.sleep(0.5)

def get_sequence_from_prompt(prompt):
    full_prompt = (
        f"Generate a list of 16 [pitch (Hz), duration (seconds)] pairs that express the emotion '{prompt}'. "
        "Use a variety of pitch and rhythm values to reflect emotional nuance. "
        "Avoid repeating the same value more than twice. Format: [[pitch, duration], ...]. "
        "Respond ONLY with the list — no explanation, no code block, no comments."
    )

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "system",
                    "content": "You are a musical assistant that returns only raw Python-style lists of [pitch, duration] pairs.",
                },
                {"role": "user", "content": full_prompt},
            ],
        )
        content = response["message"]["content"]
        print("\nRaw LLM response:\n", content)

        match = re.search(r"\[\s*(\[[^\[\]]+?\]\s*,?\s*){4,}\]", content, re.DOTALL)
        if not match:
            raise ValueError("No valid list found in response.")

        cleaned = match.group(0)
        print("\nExtracted list:\n", cleaned)

        cleaned = cleaned.replace("\n", "").replace(",,", ",").strip()
        if cleaned.endswith(","):
            cleaned = cleaned[:-1]

        sequence = ast.literal_eval(cleaned)
        unique_freqs = set(f[0] for f in sequence)
        if len(unique_freqs) <= 2:
            raise ValueError("Too little variation")

        print("\nParsed sequence:\n", sequence)
        return sequence

    except Exception as e:
        print("Using fallback randomized melody due to error:", e)
        return [
            [random.choice([440, 554, 660, 880]), random.choice([0.2, 0.3, 0.4])]
            for _ in range(16)
        ]

prompt = input("Enter a musical mood or emotion: ")
sequence = get_sequence_from_prompt(prompt)

loading_osc.stop()

freq_sig = SigTo(value=sequence[0][0], time=0.05)
amp = SigTo(value=0.3, time=0.1)
osc = Sine(freq=freq_sig, mul=amp).out()

index = [0]

def play_note():
    i = index[0]
    if i < len(sequence):
        freq, dur = sequence[i]
        print(f"Step {i}: freq={freq} Hz, dur={dur} s")
        freq_sig.setValue(freq)
        index[0] += 1
        p.time = dur
    else:
        index[0] = 0

p = Pattern(function=play_note, time=sequence[0][1]).play()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
