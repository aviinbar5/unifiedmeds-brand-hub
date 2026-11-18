"""Prototype sounds for unifiedmeds (16.11.2026). PROTOTYPES, to be produced by a sound designer.

Python standard library only. Run from anywhere:  python3 -I build_sounds.py
Writes 44.1 kHz, mono, 16-bit WAV files next to this script, each peak-normalised to -3 dBFS
with short fades. The musical material comes from the approved 8-second logo stings
(assets/animations/logo-sting-B.html and logo-sting-C.html):
  - the contact click (triangle 990 Hz plus a short bright noise tick) and a soft low thump,
  - a C5 bell on contact, then G5 for "unified" and C6 for "meds" (the rising fourth),
  - a quiet C major 9 pad (C3 C4 E4 G4 B4 D5) under the end.
"""
import math
import pathlib
import random
import struct
import wave

SR = 44100
PEAK = 10 ** (-3 / 20)  # -3 dBFS
OUT = pathlib.Path(__file__).resolve().parent
random.seed(16112026)  # deterministic noise, so a rebuild gives the same files

# note frequencies (Hz)
G4, B4, C5, D5, E5, G5, C6 = 392.00, 493.88, 523.25, 587.33, 659.25, 783.99, 1046.50
PAD = (130.81, 261.63, 329.63, 392.00, 493.88, 587.33)


def buf(seconds):
    return [0.0] * int(SR * seconds)


def add(out, t0, samples, gain=1.0):
    i0 = int(t0 * SR)
    for i, s in enumerate(samples):
        j = i0 + i
        if 0 <= j < len(out):
            out[j] += s * gain


def tri(phase):
    """Triangle wave from a phase in cycles."""
    p = phase % 1.0
    return 4 * p - 1 if p < 0.5 else 3 - 4 * p


def bell(f, dur, amp, attack=0.006):
    """Soft bell: sine partials 1, 2.76 and 5.4 (as in the stings), higher partials die faster."""
    n = int(dur * SR)
    parts = ((1.0, 1.0, dur / 5.0), (2.76, 0.18, dur / 9.0), (5.4, 0.05, dur / 14.0))
    out = []
    for i in range(n):
        t = i / SR
        a = min(1.0, t / attack)
        s = 0.0
        for m, g, tau in parts:
            s += g * math.exp(-t / tau) * math.sin(2 * math.pi * f * m * t)
        out.append(a * s * amp)
    return out


def click(amp, pitch=990.0):
    """The capsule click: a short triangle at 990 Hz plus a 25 ms high-passed noise tick."""
    n = int(0.12 * SR)
    out, prev_x, prev_y = [], 0.0, 0.0
    rc = 1.0 / (2 * math.pi * 3500)
    alpha = rc / (rc + 1.0 / SR)
    for i in range(n):
        t = i / SR
        body = tri(pitch * 0.99 * t) * math.exp(-t / 0.022) * min(1.0, t / 0.002)
        x = random.uniform(-1, 1) if t < 0.03 else 0.0
        y = alpha * (prev_y + x - prev_x)  # one-pole high-pass
        prev_x, prev_y = x, y
        tick = y * math.exp(-t / 0.006)
        out.append((0.8 * body + 0.6 * tick) * amp)
    return out


def thump(amp, dur=0.45):
    """Soft low impact: a sine gliding 92 to 40 Hz. Mostly felt on headphones and speakers, gone on a phone."""
    n = int(dur * SR)
    out, ph = [], 0.0
    for i in range(n):
        t = i / SR
        f = 40 + 52 * math.exp(-t / 0.08)
        ph += f / SR
        out.append(math.sin(2 * math.pi * ph) * math.exp(-t / 0.11) * min(1.0, t / 0.004) * amp)
    return out


def whoosh(dur, f0, f1, amp):
    """Band-passed noise sweeping f0 to f1, swelling to 70% of its length then gone (RBJ band-pass)."""
    n = int(dur * SR)
    out = []
    x1 = x2 = y1 = y2 = 0.0
    q = 1.4
    for i in range(n):
        p = i / n
        f = f0 * (f1 / f0) ** min(1.0, p / 0.85)
        w = 2 * math.pi * f / SR
        al = math.sin(w) / (2 * q)
        b0, b2 = al, -al
        a0, a1, a2 = 1 + al, -2 * math.cos(w), 1 - al
        x = random.uniform(-1, 1)
        y = (b0 * x + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1, y2, y1 = x1, x, y1, y
        env = (p / 0.7) ** 2 if p < 0.7 else ((1 - p) / 0.3) ** 1.5
        out.append(y * env * amp)
    return out


def glide(f0, f1, dur, amp):
    """A soft sine gliding f0 to f1: the u turning on its hinge (C1)."""
    n = int(dur * SR)
    out, ph = [], 0.0
    for i in range(n):
        p = i / n
        f = f0 * (f1 / f0) ** (0.5 - 0.5 * math.cos(math.pi * p))
        ph += f / SR
        env = math.sin(math.pi * p) ** 2
        out.append(math.sin(2 * math.pi * ph) * env * amp)
    return out


def pad(dur, amp, rise):
    """Quiet C major 9 pad: detuned triangles, low-passed, swelling over `rise` seconds, then fading out."""
    n = int(dur * SR)
    out = [0.0] * n
    for f in PAD:
        for det in (-3, 3):
            fr = f * 2 ** (det / 1200)
            for i in range(n):
                out[i] += tri(fr * i / SR)
    # one-pole low-pass at 1800 Hz
    a = 1 - math.exp(-2 * math.pi * 1800 / SR)
    y = 0.0
    for i in range(n):
        y += a * (out[i] - y)
        t = i / SR
        env = min(1.0, t / rise) * (1.0 if t < dur * 0.55 else max(0.0, (dur - t) / (dur * 0.45)))
        out[i] = y * env * amp / (len(PAD) * 2)
    return out


def finish(samples, name, fade_in=0.004, fade_out=0.12):
    n = len(samples)
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    for i in range(min(fi, n)):
        samples[i] *= i / fi
    for i in range(min(fo, n)):
        samples[n - 1 - i] *= i / fo
    peak = max(abs(s) for s in samples) or 1.0
    g = PEAK / peak
    data = b"".join(struct.pack("<h", int(round(max(-1.0, min(1.0, s * g)) * 32767))) for s in samples)
    path = OUT / name
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data)
    rms = math.sqrt(sum((s * g) ** 2 for s in samples) / n)
    print(f"{name}: {n / SR:.2f} s, peak -3.0 dBFS, RMS {20 * math.log10(rms):.1f} dBFS, {path.stat().st_size // 1024} KB")


# ---------- Sting sounds (short sonic logo, < 2 s) ----------

def sting_b():
    """B · Two halves: two halves rush in, click together, then the rising fourth G5 to C6."""
    out = buf(1.8)
    contact = 0.46
    add(out, 0.00, whoosh(0.50, 300, 2400, 0.20))
    add(out, 0.03, whoosh(0.47, 320, 2600, 0.20))
    add(out, contact, click(0.55))
    add(out, contact + 0.005, thump(0.60))
    add(out, contact + 0.02, bell(C5, 1.2, 0.16))
    add(out, contact, pad(1.8 - contact, 0.16, 0.45))
    add(out, 0.78, bell(G5, 1.0, 0.30))
    add(out, 0.98, bell(C6, 0.82, 0.26))
    finish(out, "sting-b-prototype.wav", fade_out=0.18)


def sting_c1():
    """C1 · From u: the u turns on its hinge (a soft rising glide), a lighter click, then G5 to C6."""
    out = buf(1.85)
    contact = 0.58
    add(out, 0.00, glide(G4, C5, 0.6, 0.22))
    add(out, 0.10, whoosh(0.48, 260, 1800, 0.10))
    add(out, contact, click(0.42))
    add(out, contact + 0.005, thump(0.45))
    add(out, contact, pad(1.85 - contact, 0.16, 0.45))
    add(out, 0.86, bell(G5, 0.95, 0.30))
    add(out, 1.06, bell(C6, 0.79, 0.26))
    finish(out, "sting-c1-prototype.wav", fade_out=0.18)


def sting_c2():
    """C2 · From u + m: two quiet notes for u and m (G4, B4, as in the C2 opening), a click, then G5 to C6."""
    out = buf(1.9)
    contact = 0.62
    add(out, 0.02, bell(G4, 0.7, 0.16))
    add(out, 0.18, bell(B4, 0.7, 0.14))
    add(out, 0.20, whoosh(0.42, 280, 2200, 0.12))
    add(out, contact, click(0.5))
    add(out, contact + 0.005, thump(0.5))
    add(out, contact, pad(1.9 - contact, 0.16, 0.45))
    add(out, 0.90, bell(G5, 0.95, 0.30))
    add(out, 1.10, bell(C6, 0.80, 0.26))
    finish(out, "sting-c2-prototype.wav", fade_out=0.18)


# ---------- UI and notification sounds (in-app only, opt-in) ----------

def ui_confirm():
    """Confirm: the brand fourth, fast and small (G5 then C6)."""
    out = buf(0.55)
    add(out, 0.0, bell(G5, 0.40, 0.30))
    add(out, 0.075, bell(C6, 0.47, 0.28))
    finish(out, "ui-confirm-prototype.wav", fade_out=0.08)


def ui_message():
    """Message from your provider: an open, unhurried fifth (C5 then G5) with a soft tail."""
    out = buf(0.95)
    add(out, 0.0, bell(C5, 0.85, 0.30))
    add(out, 0.13, bell(G5, 0.82, 0.24))
    finish(out, "ui-message-prototype.wav", fade_out=0.12)


def ui_error():
    """Gentle error: a soft falling step (D5 to C5), sine only, low level. Never a buzz."""
    out = buf(0.5)
    n = int(0.5 * SR)
    for f, t0, a in ((D5, 0.0, 0.26), (C5, 0.12, 0.24)):
        seg = []
        for i in range(n):
            t = i / SR
            seg.append(math.sin(2 * math.pi * f * t) * math.exp(-t / 0.09) * min(1.0, t / 0.008) * a)
        add(out, t0, seg)
    finish(out, "ui-error-prototype.wav", fade_out=0.08)


if __name__ == "__main__":
    sting_b()
    sting_c1()
    sting_c2()
    ui_confirm()
    ui_message()
    ui_error()
