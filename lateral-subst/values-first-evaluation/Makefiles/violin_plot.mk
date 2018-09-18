DerivedData/violin_plot_alpha_9.pdf: $(wildcard ManualData/chain_scan_for_violin/*.csv)
	-mkdir -p DerivedData/
	python Programs/violin.py ManualData/chain_scan_for_violin/alpha_9_nosubst.csv ManualData/chain_scan_for_violin/alpha_9_single.csv ManualData/chain_scan_for_violin/alpha_9_double.csv
	mv violin_plot.pdf DerivedData/violin_plot_alpha_9.pdf

DerivedData/violin_plot_beta_9.pdf: $(wildcard ManualData/chain_scan_for_violin/*.csv)
	-mkdir -p DerivedData/
	python Programs/violin.py ManualData/chain_scan_for_violin/beta_9_nosubst.csv ManualData/chain_scan_for_violin/beta_9_single.csv ManualData/chain_scan_for_violin/beta_9_double.csv
	mv violin_plot.pdf DerivedData/violin_plot_beta_9.pdf

DerivedData/violin_plot_gamma_9.pdf: $(wildcard ManualData/chain_scan_for_violin/*.csv)
	-mkdir -p DerivedData/
	python Programs/violin.py ManualData/chain_scan_for_violin/gamma_9_nosubst.csv ManualData/chain_scan_for_violin/gamma_9_single.csv ManualData/chain_scan_for_violin/gamma_9_double.csv
	mv violin_plot.pdf DerivedData/violin_plot_gamma_9.pdf

