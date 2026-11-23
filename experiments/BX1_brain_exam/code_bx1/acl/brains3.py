"""W3's learning brain (questions.md, W3-frozen): W2's MapVIN (W1e's V+: plus mask, K = 30, max) on W3's 5-channel
15 x 15 map, with a drive-weighted reward map

    r_map = conv(W0, map) + s*conv(Ws, map) + f*conv(Wf, map) + c*conv(Wc, map) + b

W0 starts random (as W2's Wr); Ws, Wf, Wc start at zero and are learned (D3, D2, Dc), or are fixed by design (D3i:
+1 at the centre tap of the food, shelter and uncertainty channels). Learning: advantage actor-critic on 64-step
segments bootstrapped with the critic, gamma 0.97, learning rate 0.01, entropy 0.01, gradient clip 1.0 (W1's).
"""
from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

import world3 as W

N, C, A, K = W.N, W.C, 8, 30
GAMMA, LR, ENT, CLIP = 0.97, 0.01, 0.01, 1.0
SEG = 64
DRIVES = ("s", "f", "c")


def cols(m):
    """im2col for a batch of maps (T, Cin, N, N), padding 1 -> (T*N*N, Cin*9)."""
    T, ci = m.shape[0], m.shape[1]
    mp = np.pad(m, ((0, 0), (0, 0), (1, 1), (1, 1)))
    win = sliding_window_view(mp, (3, 3), axis=(2, 3))
    return win.transpose(0, 2, 3, 1, 4, 5).reshape(T * N * N, ci * 9)


def uncols(d, T):
    out = np.zeros((T, N + 2, N + 2))
    dc = d.reshape(T, N, N, 3, 3)
    for ky in range(3):
        for kx in range(3):
            out[:, ky:ky + N, kx:kx + N] += dc[:, :, :, ky, kx]
    return out[:, 1:-1, 1:-1]


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


class DriveVIN:
    def __init__(self, seed, fixed_map=False):
        r = np.random.default_rng(seed)
        self.mask = np.ones((A, 1, 3, 3))
        self.mask[:, :, [0, 0, 2, 2], [0, 2, 0, 2]] = 0.0
        self.p = {"W0": r.normal(0, 0.3, (1, C, 3, 3)), "br": np.zeros(1),
                  "Ws": np.zeros((1, C, 3, 3)), "Wf": np.zeros((1, C, 3, 3)), "Wc": np.zeros((1, C, 3, 3)),
                  "Wq": r.normal(0, 0.3, (A, 1, 3, 3)), "Wv": r.normal(0, 0.3, (A, 1, 3, 3)),
                  "Wo": r.normal(0, 0.3, (5, A)), "bo": np.zeros(5), "wv": r.normal(0, 0.1, A), "bv": np.zeros(1)}
        self.p["Wv"] = self.p["Wv"] * self.mask
        self.fixed_map = fixed_map
        if fixed_map:                                   # D3i: the designer's link, never learned
            self.p["Ws"][0, W.CH_FOOD, 1, 1] = 1.0
            self.p["Wf"][0, W.CH_SHELTER, 1, 1] = 1.0
            self.p["Wc"][0, W.CH_UNC, 1, 1] = 1.0
        self.frozen = {"Ws", "Wf", "Wc"} if fixed_map else set()

    def plan(self, maps, levels):
        """maps (T, C, N, N), levels (T, 3) = (s, f, c) -> the forward trace; q per cell is the last item."""
        p, T = self.p, maps.shape[0]
        c_x = cols(maps)                                                    # (T*N*N, C*9)
        Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
        parts = c_x @ Wstack                                                # (T*N*N, 4)
        lev = np.concatenate([np.ones((T, 1)), levels], 1)                  # (T, 4)
        lev_cells = np.repeat(lev, N * N, axis=0)                           # (T*N*N, 4)
        r = (parts * lev_cells).sum(1) + p["br"][0]
        c_r = cols(r.reshape(T, 1, N, N))
        Rq = c_r @ p["Wq"].reshape(A, 9).T
        q, trace, idx = Rq, [], np.arange(T * N * N)
        Wv9 = p["Wv"].reshape(A, 9).T
        for _ in range(K - 1):
            am = q.argmax(1)
            c_v = cols(q[idx, am].reshape(T, 1, N, N))
            trace.append((c_v, am))
            q = Rq + c_v @ Wv9
        return (T, c_x, lev_cells, c_r, trace, q)

    def head(self, fw, rows):
        q = fw[5][rows]
        z = q @ self.p["Wo"].T + self.p["bo"]
        v = q @ self.p["wv"] + self.p["bv"][0]
        return z, v

    def act(self, m, levels, cell, rng=None, greedy=False):
        fw = self.plan(m[None], np.asarray(levels, float)[None])
        z, v = self.head(fw, np.array([cell[1] * N + cell[0]]))
        pi = softmax(z[0])
        a = int(pi.argmax()) if greedy else int(rng.choice(5, p=pi))
        return a, pi, float(v[0])

    def backprop(self, fw, rows, dl, dv):
        p = self.p
        T, c_x, lev_cells, c_r, trace, q = fw
        g = {k: np.zeros_like(v) for k, v in p.items()}
        qa = q[rows]
        g["Wo"] += dl.T @ qa
        g["bo"] += dl.sum(0)
        g["wv"] += dv @ qa
        g["bv"] += dv.sum()
        dq = np.zeros((T * N * N, A))
        np.add.at(dq, rows, dl @ p["Wo"] + dv[:, None] * p["wv"][None, :])
        dRq = np.zeros_like(dq)
        Wv9 = p["Wv"].reshape(A, 9)
        idx = np.arange(T * N * N)
        for c_v, am in reversed(trace):
            dRq += dq
            g["Wv"] += (dq.T @ c_v).reshape(A, 1, 3, 3)
            dv_map = uncols(dq @ Wv9, T).ravel()
            dq = np.zeros((T * N * N, A))
            dq[idx, am] = dv_map
        dRq += dq
        g["Wv"] *= self.mask
        g["Wq"] += (dRq.T @ c_r).reshape(A, 1, 3, 3)
        dr = uncols(dRq @ p["Wq"].reshape(A, 9), T).ravel()               # (T*N*N,)
        g["br"] += dr.sum()
        dparts = dr[:, None] * lev_cells                                    # (T*N*N, 4)
        gW = c_x.T @ dparts                                                 # (C*9, 4)
        for j, k in enumerate(("W0", "Ws", "Wf", "Wc")):
            g[k] += gW[:, j].reshape(1, C, 3, 3)
        for k in self.frozen:
            g[k][:] = 0.0
        return g

    def apply(self, g):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, CLIP / n) if n > 0 else 1.0
        for k in self.p:
            if k not in self.frozen:
                self.p[k] -= LR * s * g[k]

    def update(self, maps, levels, cells, acts, rets):
        """One A2C update on a segment: maps (T,C,N,N), levels (T,3), cells [(x,y)], acts [a], rets [G]."""
        fw = self.plan(np.asarray(maps), np.asarray(levels, float))
        rows = np.arange(len(cells)) * N * N + np.array([c[1] * N + c[0] for c in cells])
        z, v = self.head(fw, rows)
        dl = np.zeros_like(z)
        for t in range(len(acts)):
            pi = softmax(z[t])
            adv = rets[t] - v[t]
            d = pi.copy()
            d[acts[t]] -= 1.0
            d *= adv
            logp = np.log(pi + 1e-12)
            ent_grad = pi * (logp + 1.0) - pi * float(pi @ (logp + 1.0))
            dl[t] = d + ENT * ent_grad
        dv = v - np.asarray(rets)
        self.apply(self.backprop(fw, rows, dl, dv))

    def row_norms(self):
        return {k: float(np.sqrt((self.p[k] ** 2).sum())) for k in ("Ws", "Wf", "Wc")}
