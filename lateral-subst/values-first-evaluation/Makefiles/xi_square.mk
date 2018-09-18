DerivedData/xi_square.csv: DerivedData/bond_center_distance/__multifile__ DerivedData/chain_length/__multifile__
	-mkdir DerivedData
	>DerivedData/xi_square.csv
	for i in DerivedData/bond_center_distance/*.csv; \
	do \
		echo $$i; \
		name=`basename $$i`; \
		sum_of_squares=`cat DerivedData/bond_center_distance/$$name | cnrun csvUtils-1/transform --operation=1,pow2 | cnrun csvUtils-1/columnop --operation=1,sum`; \
		squared_length=`cat DerivedData/chain_length/$$name | cnrun csvUtils-1/transform --operation=1,pow2 |tr -d '\015'`; \
		xi_square=`echo "($$sum_of_squares)/($$squared_length)" | bc -l`; \
		echo "$$name,$$xi_square" >>DerivedData/xi_square.csv; \
	done

