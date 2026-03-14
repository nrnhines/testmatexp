from neuron import h, gui

h("create soma")
h.soma.L = 10
h.soma.diam = 10
h.soma.insert("hh")
h.soma.insert("hhkin")
h.soma.insert("hhmatexp")

h.load_file("test1.ses")  # LINEAR CIRCUIT ideal voltage clamp
