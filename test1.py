from neuron import h, gui

h("create soma")
h.soma.L = 10
h.soma.diam = 10
h.soma.insert("hh")
h.soma.insert("hhkin")
h.soma.insert("hhmatexp")

h.load_file("test1.ses")  # LINEAR CIRCUIT ideal voltage clamp

print(f" usetable {h.usetable_hh} {h.usetable_hhkin} {h.usetable_hhmatexp}")

"""
h.usetable_hh = 0
h.usetable_hhkin = 0
h.usetable_hhmatexp = 0
"""
hhmat = h.soma(0.5).hhmatexp
hhkin = h.soma(0.5).hhkin
hh = h.soma(0.5).hh

vecs = [
    h.Vector().record(x, 1.0, sec=h.soma)
    for x in [h._ref_t, h.soma(0.5)._ref_v, hh._ref_n, hhkin._ref_n4, hhmat._ref_n4]
]


def pvecs(vecs):
    n = vecs[0].size()
    for i in range(n):
        for j, vec in enumerate(vecs):
            z = vec[i] if j != 2 else vec[i] ** 4
            print(f"{z}", end="  ")
        print()


def prval():
    s = h.soma(0.5)
    print(f"{h.t}  {s.v}")
    print(f"    hh       {s.hh.gna}  {s.hh.gk}")
    print(f"    hhkin    {s.hhkin.gna}  {s.hhkin.gk}")
    print(f"    hhmatexp {s.hhmatexp.gna}  {s.hhmatexp.gk}")


def discon():
    newv = -10.0
    print(f"discon t={h.t} v={h.soma(.5).v} change to {newv}")
    h.soma.v = newv


h.tstop = 5


def run(i):
    h.steps_per_ms = i
    h.dt = 1.0 / h.steps_per_ms
    h.stdinit()
    h.cvode.event(1.0, discon)
    print(f"steps_per_ms={h.steps_per_ms}  dt={h.dt}")
    prval()
    for x in range(5):
        h.continuerun(x)
        h.fcurrent()  # make sure gna and gk evaluated based on present m,h,n
        prval()


run(1)
run(64)
