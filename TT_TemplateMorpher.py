# Run with python run_test_theta.py (in a theta directory, or with sufficient ../../../.. s)
def build_ttfit():
    model = build_model_from_rootfile('TTBAR_THETA_FEED.root')
    model.fill_histogram_zerobins()
    return model

model = build_ttfit()

for p in model.distribution.get_parameters():
    model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0]) # limits how far we can go with any variation on a parameter, important because if the subtracted ttbar estimate gets too small we can get negative expected events and this will crash or blow up.
signal_process_groups = {'': []} # just returns nuisance params (no signal)
parVals = mle(model, input = 'data', n=1, signal_process_groups = signal_process
_groups)
print parVals

model_summary(model)
report.write_html('htmlout')

