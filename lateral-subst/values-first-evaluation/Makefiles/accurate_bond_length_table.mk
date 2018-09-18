DerivedData/accurate_single_bond_length_table.csv: DerivedData/accurate_single_bond_length/__multifile__
	for file in DerivedData/accurate_single_bond_length/*.csv; \
	do \
		echo -n `basename $$file`","; \
		for i in `cat $$file`; do echo -n $$i","; done; \
		echo ""; \
	done >DerivedData/accurate_single_bond_length_table.csv

DerivedData/accurate_double_bond_length_table.csv: DerivedData/accurate_double_bond_length/__multifile__
	for file in DerivedData/accurate_double_bond_length/*.csv;\
	do \
		echo -n `basename $$file`","; \
		for i in `cat $$file`; do echo -n $$i","; done; \
		echo ""; \
	done >DerivedData/accurate_double_bond_length_table.csv
