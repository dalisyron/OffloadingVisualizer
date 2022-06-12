# -*- coding: utf-8 -*-
import sys
from dtmc_creator import DTMCCreator
from dtmc_visualizer import DTMCVisualizer

creator = DTMCCreator(2, 1, 2)
chain = creator.create()

visualizer = DTMCVisualizer(chain)
out = visualizer.visualize()

out.render(directory='doctest-output').replace('\\', '/')