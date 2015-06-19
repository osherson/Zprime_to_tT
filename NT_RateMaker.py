lumi = 19748.
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
from CutOnTree import *

TW = "(1.0*(1-0.2*0.19361022101362746)*2.71828^(-0.0013*(1-0.2*0.19771016591081025)*0.5*(MCantitoppt+MCtoppt)))" # central value with real N/a inserted

sFileName = ['t','s','tW','_t','_s','_tW']
sxs = [56.4,3.79,11.117,30.7,1.768,11.117]
sn = [3758227, 259961, 497658, 1935072, 139974, 493460]
sFilePrefix = '/home/osherson/Work/Trees/Gstar/T'

mFileName = "/home/osherson/Work/Trees/Gstar/SingleMu.root"
eFileName = "/home/osherson/Work/Trees/Gstar/SingleElectron.root"

tFileName = ["tt", "ttl_uncut"]
txs = [107.7,25.17]
tn = [25424818,12043695]
tFilePrefix = "/home/osherson/Work/Trees/Gstar/"
# Vars
var = "topcandmass"
varb = [40,100,500]

var2 = "(topcandtau3/topcandtau2)"
varb2 = [20, 0, 1]

# Preselection Cuts:
PreSel = "topcandtau2/topcandtau1>0.1&isLoose>0.&(lepcut2Drel>25.||lepcut2Ddr>0.5)&heavytopcandmass>250."

# plots:
mtPlot = TH2F("mtPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])
mdPlot = TH2F("mdPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])
msPlot = TH2F("msPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])


etPlot = TH2F("etPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])
edPlot = TH2F("edPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])
esPlot = TH2F("esPlotM", "", varb[0],varb[1],varb[2],varb2[0],varb2[1],varb2[2])

# Fill Plots:
write2dplot(eFileName, 1.0, edPlot, var, var2, "("+PreSel+"&isElec>0)", "1.0")
for i in range(len(sFileName)):
	write2dplot(sFilePrefix+sFileName[i]+'.root', sxs[i]*19748/sn[i], esPlot, var, var2, "("+PreSel+"&isElec>0)", "1.0")
for i in range(len(tFileName)):
	write2dplot(tFilePrefix+tFileName[i]+'.root', txs[i]*19748/tn[i], etPlot, var, var2, "("+PreSel+"&isElec>0)", TW)

write2dplot(mFileName, 1.0, mdPlot, var, var2, "("+PreSel+"&isMuon>0)", "1.0")
for i in range(len(sFileName)):
	write2dplot(sFilePrefix+sFileName[i]+'.root', sxs[i]*19748/sn[i], msPlot, var, var2, "("+PreSel+"&isMuon>0)", "1.0")
for i in range(len(tFileName)):
	write2dplot(tFilePrefix+tFileName[i]+'.root', txs[i]*19748/tn[i], mtPlot, var, var2, "("+PreSel+"&isMuon>0)", TW)

# Now that the plots are filled, we can fit on them.
# First we subtract the non-non-top from the field: ttbar and single top are removed:

edPlot.Add(mtPlot,-1.0)
edPlot.Add(msPlot,-1.0)

mdPlot.Add(mtPlot,-1.0)
mdPlot.Add(msPlot,-1.0)

# Start Fitting:
#First arrange the plots in a fittable way: separate by mass bins and compute P/F
# Do thsi for Muons:
mx = []
my = []
mexl = []
meyl = []
mexh = []
meyh = []
mhx = []
mhy = []
mehx = []
mehy = []

mbins = [[100,120],[120,140],[250,270],[270,400]]
for b in mbins:
	passed = 0
	failed = 0
	for i in range(mdPlot.GetNbinsX()): # this is slightly crude, but it works well and doens't have to be run too many times. It loops trhough the bins I define and fills them bin-by-bin (on the histogram) with pass/fail events
		for j in range(mdPlot.GetNbinsY()):
			if mdPlot.GetXaxis().GetBinCenter(i) < b[1] and mdPlot.GetXaxis().GetBinCenter(i) > b[0]:
				if mdPlot.GetYaxis().GetBinCenter(j) > 0.55:
					failed = failed + mdPlot.GetBinContent(i,j)
				else:
					passed = passed + mdPlot.GetBinContent(i,j)
	# If we have low statistics subtracting the ttbar and single top can leave us with "gaps" or just negative events in the least populated bins. This is of course bad, so we just set them to zero. If you want to change the binning it should be such that this is minimized,but this his here ot protect you if need be.
	if passed < 0:
		passed = 0
	if failed < 0:
		failed = 0
	if passed == 0 or failed == 0:
		continue
	mx.append((float((b[0]+b[1])/2)-170.))
	mexl.append(float((b[1]-b[0])/2))
	mexh.append(float((b[1]-b[0])/2))
	my.append(passed/(failed))
	mep = math.sqrt(passed)
	mef = math.sqrt(failed)
	err = (passed/(failed))*math.sqrt((mep/passed)+(mef/(passed))**2)
	meyh.append(err)
	if (passed/failed) - err > 0.:
		meyl.append(err)
	else:
		meyl.append(passed/failed)
mG = TGraphAsymmErrors(len(mx), scipy.array(mx), scipy.array(my), scipy.array(mexl), scipy.array(mexh), scipy.array(meyl), scipy.array(meyh))
# Do it for Electrons:
ex = []
ey = []
eexl = []
eeyl = []
eexh = []
eeyh = []
ehx = []
ehy = []
eehx = []
eehy = []

ebins = [[100,120],[120,140],[250,270],[270,400]]
for b in ebins: # Same as above
	passed = 0
	failed = 0
	for i in range(edPlot.GetNbinsX()):
		for j in range(edPlot.GetNbinsY()):
			if edPlot.GetXaxis().GetBinCenter(i) < b[1] and edPlot.GetXaxis().GetBinCenter(i) > b[0]:
				if edPlot.GetYaxis().GetBinCenter(j) > 0.55:
					failed = failed + edPlot.GetBinContent(i,j)
				else:
					passed = passed + edPlot.GetBinContent(i,j)
	if passed < 0:
		passed = 0
	if failed < 0:
		failed = 0
	if passed == 0 or failed == 0:
		continue
	ex.append((float((b[0]+b[1])/2)-170.))
	eexl.append(float((b[1]-b[0])/2))
	eexh.append(float((b[1]-b[0])/2))
	ey.append(passed/(failed))
	eep = math.sqrt(passed)
	eef = math.sqrt(failed)
	err = (passed/(failed))*math.sqrt((eep/passed)+(eef/(passed))**2)
	eeyh.append(err)
	if (passed/failed) - err > 0.:
		eeyl.append(err)
	else:
		eeyl.append(passed/failed)
eG = TGraphAsymmErrors(len(ex), scipy.array(ex), scipy.array(ey), scipy.array(eexl), scipy.array(eexh), scipy.array(eeyl), scipy.array(eeyh))

# Finally we make a graph with both channels added.
bx = []
by = []
bexl = []
beyl = []
bexh = []
beyh = []
bhx = []
bhy = []
behx = []
behy = []

bbins = [[100,120],[120,140],[250,270],[270,400]]
for b in bbins:  # same as above but with two passes, one for muons and one for electrons (filling the same TGraph)
	passed = 0
	failed = 0
	for i in range(edPlot.GetNbinsX()):
		for j in range(edPlot.GetNbinsY()):
			if edPlot.GetXaxis().GetBinCenter(i) < b[1] and edPlot.GetXaxis().GetBinCenter(i) > b[0]:
				if edPlot.GetYaxis().GetBinCenter(j) > 0.55:
					failed = failed + edPlot.GetBinContent(i,j)
				else:
					passed = passed + edPlot.GetBinContent(i,j)

	for i in range(mdPlot.GetNbinsX()):
		for j in range(mdPlot.GetNbinsY()):
			if mdPlot.GetXaxis().GetBinCenter(i) < b[1] and mdPlot.GetXaxis().GetBinCenter(i) > b[0]:
				if mdPlot.GetYaxis().GetBinCenter(j) > 0.55:
					failed = failed + mdPlot.GetBinContent(i,j)
				else:
					passed = passed + mdPlot.GetBinContent(i,j)

	if passed < 0:
		passed = 0
	if failed < 0:
		failed = 0
	if passed == 0 or failed == 0:
		continue
	bx.append((float((b[0]+b[1])/2)-170.))
	bexl.append(float((b[1]-b[0])/2))
	bexh.append(float((b[1]-b[0])/2))
	by.append(passed/(failed))
	bep = math.sqrt(passed)
	bef = math.sqrt(failed)
	err = (passed/(failed))*math.sqrt((bep/passed)+(bef/(passed))**2)
	beyh.append(err)
	if (passed/failed) - err > 0.:
		beyl.append(err)
	else:
		beyl.append(passed/failed)
bG = TGraphAsymmErrors(len(bx), scipy.array(bx), scipy.array(by), scipy.array(bexl), scipy.array(bexh), scipy.array(beyl), scipy.array(beyh))

# We now have our three lG Graphs and will not need to use any of the previous files.
#Mu:
mfunclin = TF1("mfitting_function_linear", "[0]+ [1]*x",-70,230)
mfunclin.SetParameter(0, 0.5) 
mfunclin.SetParameter(1, 0.5)
mG.Fit(mfunclin, "EMQRN") # This is the fitting step BE SURE TO INCLUDE "E" AS AN OPTION. "E" has the fit take the error into account, thus weighing low statistics bin less than high statistic bins.
mfunclin.SetLineColor(kBlue)

mfitter = TVirtualFitter.GetFitter() # careful if you change the order of things, TVirtualFitter will remember the last fitter used.
mcov = mfitter.GetCovarianceMatrixElement(0,1)

mfunclinup = TF1("mfitting_function_linear_up", "[0]+ [1]*x + sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
mfunclinup.SetParameter(0, mfunclin.GetParameter(0))
mfunclinup.SetParameter(1, mfunclin.GetParameter(1))
mfunclinup.SetParameter(2, mfunclin.GetParErrors()[0])
mfunclinup.SetParameter(3, mfunclin.GetParErrors()[1])
mfunclinup.SetParameter(4, mcov)

mfunclindn = TF1("mfitting_function_linear_dn", "[0]+ [1]*x - sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
mfunclindn.SetParameter(0, mfunclin.GetParameter(0))
mfunclindn.SetParameter(1, mfunclin.GetParameter(1))
mfunclindn.SetParameter(2, mfunclin.GetParErrors()[0])
mfunclindn.SetParameter(3, mfunclin.GetParErrors()[1])
mfunclindn.SetParameter(4, mcov)

mfunclinup.SetLineColor(kBlue)
mfunclindn.SetLineColor(kBlue)
mfunclinup.SetLineStyle(2)
mfunclindn.SetLineStyle(2)
#El:
efunclin = TF1("efitting_function_linear", "[0]+ [1]*x",-70,230)
efunclin.SetParameter(0, 0.5) 
efunclin.SetParameter(1, 0.5)
eG.Fit(efunclin, "EMQRN")
efunclin.SetLineColor(kRed)

efitter = TVirtualFitter.GetFitter()
ecov = efitter.GetCovarianceMatrixElement(0,1)

efunclinup = TF1("efitting_function_linear_up", "[0]+ [1]*x + sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
efunclinup.SetParameter(0, efunclin.GetParameter(0))
efunclinup.SetParameter(1, efunclin.GetParameter(1))
efunclinup.SetParameter(2, efunclin.GetParErrors()[0])
efunclinup.SetParameter(3, efunclin.GetParErrors()[1])
efunclinup.SetParameter(4, ecov)

efunclindn = TF1("mfitting_function_linear_dn", "[0]+ [1]*x - sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
efunclindn.SetParameter(0, efunclin.GetParameter(0))
efunclindn.SetParameter(1, efunclin.GetParameter(1))
efunclindn.SetParameter(2, efunclin.GetParErrors()[0])
efunclindn.SetParameter(3, efunclin.GetParErrors()[1])
efunclindn.SetParameter(4, ecov)

efunclinup.SetLineColor(kRed)
efunclindn.SetLineColor(kRed)
efunclinup.SetLineStyle(2)
efunclindn.SetLineStyle(2)
#Both:
bfunclin = TF1("bfitting_function_linear", "[0]+ [1]*x",-70,230)
bfunclin.SetParameter(0, 0.5) 
bfunclin.SetParameter(1, 0.5)
bG.Fit(bfunclin, "EMQRN")
bfunclin.SetLineColor(kViolet)

bfitter = TVirtualFitter.GetFitter()
bcov = bfitter.GetCovarianceMatrixElement(0,1)

bfunclinup = TF1("bfitting_function_linear_up", "[0]+ [1]*x + sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
bfunclinup.SetParameter(0, bfunclin.GetParameter(0))
bfunclinup.SetParameter(1, bfunclin.GetParameter(1))
bfunclinup.SetParameter(2, bfunclin.GetParErrors()[0])
bfunclinup.SetParameter(3, bfunclin.GetParErrors()[1])
bfunclinup.SetParameter(4, bcov)

bfunclindn = TF1("bfitting_function_linear_dn", "[0]+ [1]*x - sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-70,230)
bfunclindn.SetParameter(0, bfunclin.GetParameter(0))
bfunclindn.SetParameter(1, bfunclin.GetParameter(1))
bfunclindn.SetParameter(2, bfunclin.GetParErrors()[0])
bfunclindn.SetParameter(3, bfunclin.GetParErrors()[1])
bfunclindn.SetParameter(4, bcov)

bfunclinup.SetLineColor(kViolet)
bfunclindn.SetLineColor(kViolet)
bfunclinup.SetLineStyle(2)
bfunclindn.SetLineStyle(2)

# Now some beautification:
for G in [mG,eG,bG]:
	G.SetMarkerStyle(21)
	G.GetXaxis().SetTitle("#Delta(jet - top)_{mass} [GeV/c^{2}]")
	G.GetYaxis().SetTitle("N_{passed}/N_{failed}")
	G.GetYaxis().SetTitleSize(0.05)
	G.GetYaxis().SetTitleOffset(0.9)
	G.GetXaxis().SetTitleOffset(0.87)
	G.GetXaxis().SetTitleSize(0.04)
eleg = TLegend(0.2,0.6,0.55,0.89)
eleg.SetFillColor(0)
eleg.SetLineColor(0)
eleg.AddEntry(efunclin, "linear fit (e channel)", "L")
eleg.AddEntry(mfunclin, "linear fit (#mu channel)", "L")
eleg.AddEntry(bfunclin, "linear fir (both channels)", "L")
eleg.AddEntry(efunclinup, "error in fit", "L")
eleg.AddEntry(eG, "data (e channel)", "PL")

mleg = TLegend(0.2,0.6,0.55,0.89)
mleg.SetFillColor(0)
mleg.SetLineColor(0)
mleg.AddEntry(efunclin, "linear fit (e channel)", "L")
mleg.AddEntry(mfunclin, "linear fit (#mu channel)", "L")
mleg.AddEntry(bfunclin, "linear fir (both channels)", "L")
mleg.AddEntry(mfunclinup, "error in fit", "L")
mleg.AddEntry(mG, "data (#mu channel)", "PL")

bleg = TLegend(0.2,0.6,0.55,0.89)
bleg.SetFillColor(0)
bleg.SetLineColor(0)
bleg.AddEntry(efunclin, "linear fit (e channel)", "L")
bleg.AddEntry(mfunclin, "linear fit (#mu channel)", "L")
bleg.AddEntry(bfunclin, "linear fir (both channels)", "L")
bleg.AddEntry(bfunclinup, "error in fit", "L")
bleg.AddEntry(bG, "data (both channels)", "PL")

C1 = TCanvas("c1", "c1", 1200, 600)
C1.Divide(2,1)
C1.cd(1)
eG.Draw("AP")
eG.GetYaxis().SetRangeUser(-0.,0.6)
efunclin.Draw("same")
mfunclin.Draw("same")
bfunclin.Draw("same")
efunclinup.Draw("same")
efunclindn.Draw("same")
eleg.Draw()
C1.cd(2)
mG.Draw("AP")
mG.GetYaxis().SetRangeUser(-0.,0.6)
efunclin.Draw("same")
mfunclin.Draw("same")
bfunclin.Draw("same")
mfunclinup.Draw("same")
mfunclindn.Draw("same")
mleg.Draw()

C2 = TCanvas("c2", "c2", 600,600)
C2.cd()
bG.Draw("AP")
bG.GetYaxis().SetRangeUser(-0.,0.6)
efunclin.Draw("same")
mfunclin.Draw("same")
bfunclin.Draw("same")
bfunclinup.Draw("same")
bfunclindn.Draw("same")
bleg.Draw()

bfunclin.Print()
bfunclinup.Print()
bfunclindn.Print()



