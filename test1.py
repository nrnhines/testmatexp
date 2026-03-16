from neuron import h, gui

"""
verify identity of hh and hhmatexp
and voltage clamp result independence on dt.
The "tricks" used for dt independence are
1) use ideal voltage clamp (implemented from LinearCircuitBuilder) with
   step discontinuity from -65mv to -10 mv at 1ms
2) Force voltage change to -10mv with cvode event at 1ms
   Otherwise, for the fixed step method, the voltage change will affect the
   model on the following step
3) Use fcurrent() before evaluating gna and gk.
   Otherwise gna and gk will have been evaluated using voltage at t-dt/2 and
   gating states at t+dt/2
4) Implied by 3), do not use Vector.record to evaluate gna and gk
"""

h("create soma")
h.soma.L = 10
h.soma.diam = 10
h.soma.insert("hh")
h.soma.insert("hhkin")
h.soma.insert("hhmatexp")

h.load_file("test1.ses")  # LINEAR CIRCUIT ideal voltage clamp

if 0:
    h.usetable_hh = 0
    h.usetable_hhkin = 0
    h.usetable_hhmatexp = 0

print(f" usetable {h.usetable_hh} {h.usetable_hhkin} {h.usetable_hhmatexp}")


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
    if h.cvode_active() == 0.0:
        h.cvode.event(1.0, discon)
    print(f"steps_per_ms={h.steps_per_ms}  dt={h.dt}")
    prval()
    for x in range(5):
        h.continuerun(x)
        h.fcurrent()  # make sure gna and gk evaluated based on present m,h,n
        prval()


# h.cvode_active(1)  # KINETIC appears not to work when translated by nmodl
run(1)
run(64)
