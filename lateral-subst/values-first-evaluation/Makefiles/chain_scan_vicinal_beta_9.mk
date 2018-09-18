DerivedData/plot_chain_scan_vicinal/chain_scan_vicinal_beta_9.pdf: $(wildcard ManualData/chain_scan_vicinal/*.csv)
	-mkdir -p DerivedData/plot_chain_scan_vicinal/
	echo "set datafile separator ','; set terminal pdf; set output 'DerivedData/plot_chain_scan_vicinal/chain_scan_vicinal_beta_9.pdf'; plot 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_13-NO2_14-NO2.csv' u 0:2 w lp lt 1 pt 1, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_13-NO2_14-NH2.csv' u 0:2 w lp lt 1 pt 2, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_13-NH2_14-NO2.csv' u 0:2 w lp lt 1 pt 3, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_13-NH2_14-NH2.csv' u 0:2 w lp lt 1 pt 4, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_14-NO2_15-NO2.csv' u 0:2 w lp lt 2 pt 1, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_14-NO2_15-NH2.csv' u 0:2 w lp lt 2 pt 2, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_14-NH2_15-NO2.csv' u 0:2 w lp lt 2 pt 3, 'ManualData/chain_scan_vicinal/beta/beta_9_vicinal_14-NH2_15-NH2.csv' u 0:2 w lp lt 2 pt 4" | gnuplot