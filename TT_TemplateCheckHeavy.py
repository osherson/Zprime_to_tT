# copy of TT_TemplateMaker with correct values put in for N and a. Makes plots showing how the template morphing applies to a regin outside which it was measured. (In this case m in [250,400] for the lep side.

lumi = 19748.
import ROOT
from ROOT import *
from CutOnTree import writeplot

TW = "(1.0*(1-0.2*0.19361022101362746)*2.71828^(-0.0013*(1-0.2*0.19771016591081025)*0.5*(MCantitoppt+MCtoppt)))" # central value with real N/a inserted


ntW_el = "(0.0618663 + 0.000528015*(topcandmass-170.))"
ntW_mu = "(0.0678199 + 0.000707998*(topcandmass-170.))"

# Define files:
# single top
sFileName = ['t','s','tW','_t','_s','_tW']
sxs = [56.4,3.79,11.117,30.7,1.768,11.117]
sn = [3758227, 259961, 497658, 1935072, 139974, 493460]
sFilePrefix = '/home/osherson/Work/Trees/Gstar/T'
# data
dFileNameE = "/home/osherson/Work/Trees/Gstar/SingleElectron.root"
dFileNameM = "/home/osherson/Work/Trees/Gstar/SingleMu.root"
# ttbar
tFileName = ["tt", "ttl_uncut"]
txs = [107.7,25.17]
tn = [25424818,12043695]
tFilePrefix = "/home/osherson/Work/Trees/Gstar/"

# Define cuts we'll use:
# Cuts:
El = "isElec>0.&isLoose>0."
Mu = "isMuon>0.&isLoose>0."
PreSel = "(topcandtau2/topcandtau1>0.1&(lepcut2Drel>25.||lepcut2Ddr>0.5)&heavytopcandmass>250.&heavytopcandmass<400.)" # has a leptoinc top mass and 2D cut on the leptonic side
TopTag = "(topcandtau3/topcandtau2<0.55&topcandmass<250&topcandmass>140)"
AntiTag = "(topcandmass<250&topcandmass>140&topcandtau3/topcandtau2>0.55)" # inverted tau32 cut

# Subtractions: removed from estimate of NonTop
mtZPs = TH1F("mtZPs", "", 25, 0, 2500)
msZPs = TH1F("msZPs", "", 25, 0, 2500)

etZPs = TH1F("etZPs", "", 25, 0, 2500)
esZPs = TH1F("esZPs", "", 25, 0, 2500)

# Estimates:
mdZPe = TH1F("MU__NT", "", 25, 0, 2500)
edZPe = TH1F("EL__NT", "", 25, 0, 2500)

# data:
mdZP = TH1F("MU__DATA", "", 25, 0, 2500)
edZP = TH1F("EL__DATA", "", 25, 0, 2500)

# MC measurements:
mtZPm = TH1F("MU__tt", "", 25, 0, 2500)
msZPm = TH1F("MU__st", "", 25, 0, 2500)
etZPm = TH1F("EL__tt", "", 25, 0, 2500)
esZPm = TH1F("EL__st", "", 25, 0, 2500)

# Now we fill these all up:
#Subtraction:
for i in range(len(tFileName)): # ttbar
	writeplot(tFilePrefix+tFileName[i]+'.root', lumi*txs[i]/tn[i], etZPs, "EventMass", "("+PreSel+"&"+AntiTag+"&"+El+")", "("+ntW_el+"*"+TW+")")
	writeplot(tFilePrefix+tFileName[i]+'.root', lumi*txs[i]/tn[i], mtZPs, "EventMass", "("+PreSel+"&"+AntiTag+"&"+Mu+")", "("+ntW_mu+"*"+TW+")")
for i in range(len(sFileName)): # signle top
	writeplot(sFilePrefix+sFileName[i]+'.root', lumi*sxs[i]/sn[i], esZPs, "EventMass", "("+PreSel+"&"+AntiTag+"&"+El+")", "("+ntW_el+")")
	writeplot(sFilePrefix+sFileName[i]+'.root', lumi*sxs[i]/sn[i], msZPs, "EventMass", "("+PreSel+"&"+AntiTag+"&"+Mu+")", "("+ntW_mu+")")
#Estimates:
writeplot(dFileNameE, 1.0, edZPe, "EventMass", "("+PreSel+"&"+AntiTag+"&"+El+")", "("+ntW_el+")")
writeplot(dFileNameM, 1.0, mdZPe, "EventMass", "("+PreSel+"&"+AntiTag+"&"+Mu+")", "("+ntW_mu+")")
#data:
writeplot(dFileNameE, 1.0, edZP, "EventMass", "("+PreSel+"&"+TopTag+"&"+El+")", "1.0")
writeplot(dFileNameM, 1.0, mdZP, "EventMass", "("+PreSel+"&"+TopTag+"&"+Mu+")", "1.0")

# Fill MC:
for i in range(len(tFileName)): # All  versions of the ttbar
	writeplot(tFilePrefix+tFileName[i]+'.root', lumi*txs[i]/tn[i], etZPm, "EventMass", "("+PreSel+"&"+TopTag+"&"+El+")", "("+TW+")")
	writeplot(tFilePrefix+tFileName[i]+'.root', lumi*txs[i]/tn[i], mtZPm, "EventMass", "("+PreSel+"&"+TopTag+"&"+Mu+")", "("+TW+")")
for i in range(len(sFileName)):
	writeplot(sFilePrefix+sFileName[i]+'.root', lumi*sxs[i]/sn[i], esZPm, "EventMass", "("+PreSel+"&"+TopTag+"&"+El+")", "1.0")
	writeplot(sFilePrefix+sFileName[i]+'.root', lumi*sxs[i]/sn[i], msZPm, "EventMass", "("+PreSel+"&"+TopTag+"&"+Mu+")", "1.0")

# Correct the NonTop Est to not double-count anything:
edZPe.Add(esZPs,-1)
mdZPe.Add(msZPs,-1)

edZPe.Add(etZPs,-1)
mdZPe.Add(mtZPs,-1)

# Plotting:
# Colors
msZPm.SetFillColor(kViolet)
esZPm.SetFillColor(kViolet)
mtZPm.SetFillColor(kRed)
etZPm.SetFillColor(kRed)
mdZPe.SetFillColor(kSpring)
edZPe.SetFillColor(kSpring)

estack = THStack("E", "E")
estack.Add(esZPm)
estack.Add(etZPm)
estack.Add(edZPe)
mstack = THStack("M", "M")
mstack.Add(esZPm)
mstack.Add(etZPm)
mstack.Add(edZPe)

# Data (and pad info since we draw it first)

edZP.SetStats(0)
edZP.Sumw2()
edZP.SetLineColor(1)
edZP.SetFillColor(0)
edZP.SetMarkerColor(1)
edZP.SetMarkerStyle(20)
edZP.GetXaxis().SetTitle("Event Mass")
edZP.GetYaxis().SetTitle("events")


mdZP.SetStats(0)
mdZP.Sumw2()
mdZP.SetLineColor(1)
mdZP.SetFillColor(0)
mdZP.SetMarkerColor(1)
mdZP.SetMarkerStyle(20)
mdZP.GetXaxis().SetTitle("Event Mass")
mdZP.GetYaxis().SetTitle("events")


# Legend
bl = TLegend(0.5,0.6,0.89,0.89)
bl.SetFillColor(0)
bl.SetLineColor(0)

bl.AddEntry(mtZPm, "corr. semi-leptonic t#bar{t}", "F")
bl.AddEntry(mdZPe, "non-top bkg.", "F")
bl.AddEntry(msZPm, "single top", "F")
bl.AddEntry(mdZP, "data", "PL")



C = TCanvas()
C.Divide(2,1)
C.cd(1)
edZP.Draw()
edZP.GetYaxis().SetRangeUser(0, 40)
estack.Draw("same")
edZP.Draw("same")
bl.Draw()
C.cd(2)
mdZP.Draw()
mdZP.GetYaxis().SetRangeUser(0, 40)
mstack.Draw("same")
mdZP.Draw("same")
bl.Draw()
