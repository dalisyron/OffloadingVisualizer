from dtmc_creator import DTMCCreator
from dtmc_visualizer import DTMCVisualizer

creator = DTMCCreator(3, 2, 2)
chain = creator.create()

visualizer = DTMCVisualizer(chain)
out = visualizer.visualize()

out.render(directory='doctest-output').replace('\\', '/')