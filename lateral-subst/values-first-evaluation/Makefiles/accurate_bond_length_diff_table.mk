DerivedData/accurate_double_bond_length_diff_table.csv: DerivedData/accurate_double_bond_length_table.csv
	double_bond_nosubst=`cat "DerivedData/accurate_double_bond_length_table.csv" | grep "lateral-9_0-H_1-H_2-H_3-H_4-H_5-H_6-H_7-H_8-H_9-H_10-H_11-H_12-H_13-H_14-H_15-H.csv"`; \
	h_1=`echo "$$double_bond_nosubst" | cut -d',' -f 2`; \
	h_2=`echo "$$double_bond_nosubst" | cut -d',' -f 3`; \
	h_3=`echo "$$double_bond_nosubst" | cut -d',' -f 4`; \
	h_4=`echo "$$double_bond_nosubst" | cut -d',' -f 5`; \
	h_5=`echo "$$double_bond_nosubst" | cut -d',' -f 6`; \
	h_6=`echo "$$double_bond_nosubst" | cut -d',' -f 7`; \
	h_7=`echo "$$double_bond_nosubst" | cut -d',' -f 8`; \
	h_8=`echo "$$double_bond_nosubst" | cut -d',' -f 9`; \
	h_9=`echo "$$double_bond_nosubst" | cut -d',' -f 10`; \
	for i in `cat "DerivedData/accurate_double_bond_length_table.csv"`; do \
		name=`echo "$$i" | cut -d',' -f 1`; \
		x_1=`echo "$$i" | cut -d',' -f 2`; \
		x_2=`echo "$$i" | cut -d',' -f 3`; \
		x_3=`echo "$$i" | cut -d',' -f 4`; \
		x_4=`echo "$$i" | cut -d',' -f 5`; \
		x_5=`echo "$$i" | cut -d',' -f 6`; \
		x_6=`echo "$$i" | cut -d',' -f 7`; \
		x_7=`echo "$$i" | cut -d',' -f 8`; \
		x_8=`echo "$$i" | cut -d',' -f 9`; \
		x_9=`echo "$$i" | cut -d',' -f 10`; \
		d_1=`echo "($$x_1-$$h_1)*1000" | bc -l`; \
		d_2=`echo "($$x_2-$$h_2)*1000" | bc -l`; \
		d_3=`echo "($$x_3-$$h_3)*1000" | bc -l`; \
		d_4=`echo "($$x_4-$$h_4)*1000" | bc -l`; \
		d_5=`echo "($$x_5-$$h_5)*1000" | bc -l`; \
		d_6=`echo "($$x_6-$$h_6)*1000" | bc -l`; \
		d_7=`echo "($$x_7-$$h_7)*1000" | bc -l`; \
		d_8=`echo "($$x_8-$$h_8)*1000" | bc -l`; \
		d_9=`echo "($$x_9-$$h_9)*1000" | bc -l`; \
		echo "$$name,$$d_1,$$d_2,$$d_3,$$d_4,$$d_5,$$d_6,$$d_7,$$d_8,$$d_9"; \
	done >DerivedData/accurate_double_bond_length_diff_table.csv

DerivedData/accurate_single_bond_length_diff_table.csv: DerivedData/accurate_single_bond_length_table.csv
	single_bond_nosubst=`cat "DerivedData/accurate_single_bond_length_table.csv" | grep "lateral-9_0-H_1-H_2-H_3-H_4-H_5-H_6-H_7-H_8-H_9-H_10-H_11-H_12-H_13-H_14-H_15-H.csv"`; \
	h_1=`echo "$$single_bond_nosubst" | cut -d',' -f 2`; \
	h_2=`echo "$$single_bond_nosubst" | cut -d',' -f 3`; \
	h_3=`echo "$$single_bond_nosubst" | cut -d',' -f 4`; \
	h_4=`echo "$$single_bond_nosubst" | cut -d',' -f 5`; \
	h_5=`echo "$$single_bond_nosubst" | cut -d',' -f 6`; \
	h_6=`echo "$$single_bond_nosubst" | cut -d',' -f 7`; \
	h_7=`echo "$$single_bond_nosubst" | cut -d',' -f 8`; \
	h_8=`echo "$$single_bond_nosubst" | cut -d',' -f 9`; \
	for i in `cat "DerivedData/accurate_single_bond_length_table.csv"`; do \
		name=`echo "$$i" | cut -d',' -f 1`; \
		x_1=`echo "$$i" | cut -d',' -f 2`; \
		x_2=`echo "$$i" | cut -d',' -f 3`; \
		x_3=`echo "$$i" | cut -d',' -f 4`; \
		x_4=`echo "$$i" | cut -d',' -f 5`; \
		x_5=`echo "$$i" | cut -d',' -f 6`; \
		x_6=`echo "$$i" | cut -d',' -f 7`; \
		x_7=`echo "$$i" | cut -d',' -f 8`; \
		x_8=`echo "$$i" | cut -d',' -f 9`; \
		d_1=`echo "($$x_1-$$h_1)*1000" | bc -l`; \
		d_2=`echo "($$x_2-$$h_2)*1000" | bc -l`; \
		d_3=`echo "($$x_3-$$h_3)*1000" | bc -l`; \
		d_4=`echo "($$x_4-$$h_4)*1000" | bc -l`; \
		d_5=`echo "($$x_5-$$h_5)*1000" | bc -l`; \
		d_6=`echo "($$x_6-$$h_6)*1000" | bc -l`; \
		d_7=`echo "($$x_7-$$h_7)*1000" | bc -l`; \
		d_8=`echo "($$x_8-$$h_8)*1000" | bc -l`; \
		echo "$$name,$$d_1,$$d_2,$$d_3,$$d_4,$$d_5,$$d_6,$$d_7,$$d_8"; \
	done >DerivedData/accurate_single_bond_length_diff_table.csv
