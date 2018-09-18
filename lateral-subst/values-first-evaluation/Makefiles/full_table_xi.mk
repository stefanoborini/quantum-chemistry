DerivedData/full_table_xi.csv: DerivedData/xi.csv DerivedData/xi_square.csv DerivedData/xi_tilde_square.csv
	-mkdir -p DerivedData/
	> DerivedData/full_table_xi.csv
	for i in `cat DerivedData/xi.csv | cut -d',' -f 1`; \
	do \
		name=`basename $$i`; \
		xi=`cat DerivedData/xi.csv | grep $$i | cut -d',' -f 2`; \
		xi_square=`cat DerivedData/xi_square.csv | grep $$i | cut -d',' -f 2`; \
		xi_tilde_square=`cat DerivedData/xi_tilde_square.csv | grep $$i | cut -d',' -f 2`; \
		division=`echo "$$xi_tilde_square/$$xi_square" | bc -l `; \
		echo "$$name,$$xi,$$xi_square,$$xi_tilde_square,$$division" >>DerivedData/full_table_xi.csv; \
	done 

