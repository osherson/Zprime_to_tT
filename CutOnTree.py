import ROOT
from ROOT import *

# Takes a File (which must contain a tree named "tree") and applies the cut "Cut" and the weight "Weight", then plots the var "var" on the TH1F "plot".
def writeplot(File, scale, plot, var, Cut, Weight):
	temp = plot.Clone("temp") # Allows to add multiple distributions to the plot
	chain = ROOT.TChain("tree")
	chain.Add(File)
	chain.Draw(var+">>"+"temp", Weight+"*"+Cut, "goff")
	temp.Scale(scale)
	plot.Add(temp)
