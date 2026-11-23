"""MoveVIN: a planner that must plan like value iteration (W3p, draft). The feelings part is DriveVIN's, unchanged:

    r = conv(W0, map) + s*conv(Ws, map) + f*conv(Wf, map) + c*conv(Wc, map) + br        (what each place is worth now)

What changes is the thinking loop. DriveVIN's loop used 8 free learned channels (Wq, Wv), and the diagnosis (W3p
explore/diag_plan.py) showed its value map does not lead to the food (uphill 0-11% on detours). Here the loop is the
body's own physics, with one learned perception:

    p(x)   = sigmoid(conv(Wp, map) + bp)       can I enter place x?  (learned; no wall label is given)
    gamma  = sigmoid(g)                        how much the future counts (learned)
    v_0    = r
    m_a(x) = p(x+a) v(x+a) + (1 - p(x+a)) v(x)    for the 4 moves: trying to move into a blocked place leaves you where
                                                  you are (as the world does); m_stay(x) = v(x); off the map p = 0
    q_a(x) = r(x) + gamma m_a(x),   v = max_a q_a,    K = 30 rounds

The hand reads the 5 move values at its own place: z = exp(lb) q(pos) + bo; the critic: wv v(pos) + bv.
236 learned numbers. The interface (plan, head, backprop, apply, update, act, row_norms, p) is DriveVIN's, so W3's
whole training recipe runs on it unchanged.
"""
from __future__ import annotations

import numpy as np

import brains3 as B

N, C, K = B.N, B.C, B.K
MOVES = [(0, -1), (0, 1), (1, 0), (-1, 0)]          # world3.MOVES[:4]: north, south, east, west; index 4 = stay


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def shift_in(a, dx, dy):
    """b[t, y, x] = a[t, y+dy, x+dx], 0 off the map."""
    ap = np.pad(a, ((0, 0), (1, 1), (1, 1)))
    return ap[:, 1 + dy:1 + dy + N, 1 + dx:1 + dx + N]


def shift_back(d, dx, dy):
    """The adjoint of shift_in: scatters d[t, y, x] onto (x+dx, y+dy)."""
    out = np.zeros((d.shape[0], N + 2, N + 2))
    out[:, 1 + dy:1 + dy + N, 1 + dx:1 + dx + N] += d
    return out[:, 1:-1, 1:-1]


def add_shifted(dst, d, dx, dy):
    """dst += shift_back(d, dx, dy), without building the shifted copy (the same additions, element by element)."""
    tx, sx = slice(max(0, dx), N + min(0, dx)), slice(max(0, -dx), N + min(0, -dx))
    ty, sy = slice(max(0, dy), N + min(0, dy)), slice(max(0, -dy), N + min(0, -dy))
    dst[:, ty, tx] += d[:, sy, sx]


class MoveVIN(B.DriveVIN):
    def __init__(self, seed, fixed_map=False):
        r = np.random.default_rng(seed)
        self.p = {"W0": r.normal(0, 0.3, (1, C, 3, 3)), "br": np.zeros(1),
                  "Ws": np.zeros((1, C, 3, 3)), "Wf": np.zeros((1, C, 3, 3)), "Wc": np.zeros((1, C, 3, 3)),
                  "Wp": r.normal(0, 0.1, (1, C, 3, 3)), "bp": np.full(1, 2.0), "g": np.full(1, 2.2),
                  "lb": np.zeros(1), "bo": np.zeros(5), "wv": np.ones(1), "bv": np.zeros(1)}
        self.fixed_map, self.frozen = False, set()

    def plan(self, maps, levels):
        p, T = self.p, maps.shape[0]
        c_x = B.cols(maps)
        Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
        parts = c_x @ Wstack
        lev_cells = np.repeat(np.concatenate([np.ones((T, 1)), levels], 1), N * N, axis=0)
        r = ((parts * lev_cells).sum(1) + p["br"][0]).reshape(T, N, N)
        pas = sig(c_x @ p["Wp"].reshape(-1) + p["bp"][0]).reshape(T, N, N)
        gam = float(sig(p["g"][0]))
        pn = [shift_in(pas, dx, dy) for dx, dy in MOVES]
        qn = [1 - x for x in pn]
        v, trace = r, []
        vp = np.zeros((T, N + 2, N + 2))
        for _ in range(K):
            vp[:, 1:-1, 1:-1] = v                         # one padded copy per round; the 4 neighbours are views of it
            m = [pn[a] * vp[:, 1 + dy:1 + dy + N, 1 + dx:1 + dx + N] + qn[a] * v
                 for a, (dx, dy) in enumerate(MOVES)] + [v]
            q = np.empty((5, T, N, N))
            for a in range(5):
                np.multiply(gam, m[a], out=q[a])
                q[a] += r
            am = q.argmax(0)
            trace.append((v, m, am))
            v = np.take_along_axis(q, am[None], 0)[0]
        return (T, c_x, lev_cells, r, pas, pn, gam, trace, q, v)

    def head(self, fw, rows):
        q, v = fw[8], fw[9]
        qr = q.reshape(5, -1)[:, rows].T                                      # (R, 5)
        z = np.exp(self.p["lb"][0]) * qr + self.p["bo"]
        val = self.p["wv"][0] * v.reshape(-1)[rows] + self.p["bv"][0]
        return z, val

    def backprop(self, fw, rows, dl, dv):
        p = self.p
        T, c_x, lev_cells, r, pas, pn, gam, trace, q, v = fw
        g = {k: np.zeros_like(x) for k, x in p.items()}
        beta = np.exp(p["lb"][0])
        qr = q.reshape(5, -1)[:, rows].T
        g["bo"] += dl.sum(0)
        g["lb"] += float((dl * qr).sum()) * beta
        g["wv"] += float(dv @ v.reshape(-1)[rows])
        g["bv"] += float(dv.sum())
        dq = np.zeros((5, T * N * N))
        np.add.at(dq.T, rows, beta * dl)                                      # the head reads the last round's q
        dvn = np.zeros(T * N * N)
        np.add.at(dvn, rows, p["wv"][0] * dv)                                 # the critic reads the last v
        dq, dvn = dq.reshape(5, T, N, N), dvn.reshape(T, N, N)
        dr, dpas, dgam = np.zeros((T, N, N)), np.zeros((T, N, N)), 0.0
        for k in range(K - 1, -1, -1):
            v_prev, m, am = trace[k]
            dq_k = dq if k == K - 1 else np.zeros((5, T, N, N))
            np.put_along_axis(dq_k, am[None], np.take_along_axis(dq_k, am[None], 0) + dvn[None], 0)
            dr += dq_k.sum(0)
            dgam += float(sum((dq_k[a] * m[a]).sum() for a in range(5)))
            dm = gam * dq_k
            dvp = dm[4].copy()
            vpp = np.pad(v_prev, ((0, 0), (1, 1), (1, 1)))
            for a, (dx, dy) in enumerate(MOVES):
                dvp += dm[a] * (1 - pn[a])
                add_shifted(dvp, dm[a] * pn[a], dx, dy)
                add_shifted(dpas, dm[a] * (vpp[:, 1 + dy:1 + dy + N, 1 + dx:1 + dx + N] - v_prev), dx, dy)
            dvn = dvp
        dr += dvn                                                             # v_0 = r
        g["g"] += dgam * gam * (1 - gam)
        du = (dpas * pas * (1 - pas)).reshape(-1)
        g["Wp"] += (c_x.T @ du).reshape(1, C, 3, 3)
        g["bp"] += du.sum()
        drf = dr.reshape(-1)
        g["br"] += drf.sum()
        gW = c_x.T @ (drf[:, None] * lev_cells)
        for j, kk in enumerate(("W0", "Ws", "Wf", "Wc")):
            g[kk] += gW[:, j].reshape(1, C, 3, 3)
        return g
