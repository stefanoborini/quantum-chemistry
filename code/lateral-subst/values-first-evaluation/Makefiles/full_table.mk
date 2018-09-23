DerivedData/full_table/full_table_double.csv: $(wildcard ManualData/chain_scan/*.csv)
	-mkdir -p DerivedData/full_table
	for i in `cat SourceData/raw/alpha_9_double.csv | cut -d',' -f 1`; \
	do \
		alpha=`cat SourceData/raw/alpha_9_double.csv | grep $$i | cut -d',' -f 2`; \
		beta=`cat SourceData/raw/beta_9_double.csv | grep $$i | cut -d',' -f 2`; \
		gamma=`cat SourceData/raw/gamma_9_double.csv | grep $$i | cut -d',' -f 2`; \
		echo "$$i,$$alpha,$$beta,$$gamma"; \
	done >DerivedData/full_table/full_table_double.csv

DerivedData/full_table/full_table_single.csv: $(wildcard ManualData/chain_scan/*.csv)
	-mkdir -p DerivedData/full_table
	for i in `cat SourceData/raw/alpha_9_single.csv | cut -d',' -f 1`; \
	do \
		alpha=`cat SourceData/raw/alpha_9_single.csv | grep $$i | cut -d',' -f 2`; \
		beta=`cat SourceData/raw/beta_9_single.csv | grep $$i | cut -d',' -f 2`; \
		gamma=`cat SourceData/raw/gamma_9_single.csv | grep $$i | cut -d',' -f 2`; \
		echo "$$i,$$alpha,$$beta,$$gamma"; \
	done >DerivedData/full_table/full_table_single.csv

DerivedData/full_table/full_table_none.csv: $(wildcard ManualData/chain_scan/*.csv)
	-mkdir -p DerivedData/full_table
	for i in `cat SourceData/raw/alpha_9_none.csv | cut -d',' -f 1`; \
	do \
		alpha=`cat SourceData/raw/alpha_9_none.csv | grep $$i | cut -d',' -f 2`; \
		beta=`cat SourceData/raw/beta_9_none.csv | grep $$i | cut -d',' -f 2`; \
		gamma=`cat SourceData/raw/gamma_9_none.csv | grep $$i | cut -d',' -f 2`; \
		echo "$$i,$$alpha,$$beta,$$gamma"; \
	done >DerivedData/full_table/full_table_none.csv
