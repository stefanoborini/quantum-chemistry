DerivedData/plot_chain_scan/chain_scan_alpha_9.pdf: $(wildcard ManualData/chain_scan/*.csv)
	-mkdir -p DerivedData/plot_chain_scan/
	echo "set datafile separator ','; set terminal pdf; set output 'DerivedData/plot_chain_scan/chain_scan_alpha_9.pdf'; plot [0:14] 'ManualData/chain_scan/alpha_9_NH2_even.csv' u 2:3 w lp, 'ManualData/chain_scan/alpha_9_NO2_even.csv' u 2:3 w lp, 'ManualData/chain_scan/alpha_9_nosubst.csv' u 2:3 w lp;" | gnuplot

