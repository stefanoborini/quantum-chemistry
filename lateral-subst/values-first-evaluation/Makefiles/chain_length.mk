DerivedData/chain_length/__multifile__: DerivedData/bond_center/__multifile__
	-mkdir -p DerivedData/chain_length/
	for i in DerivedData/bond_center/*.csv; \
	do \
		echo $$i; \
		name=`basename $$i`; \
		first_x=`cat DerivedData/bond_center/$$name | sed -e "s/^ *$$//g" | grep -v -e "^$$" | grep -v -e "^#"| head -1 | cut -d',' -f1`; \
		first_y=`cat DerivedData/bond_center/$$name | sed -e "s/^ *$$//g" | grep -v -e "^$$" | grep -v -e "^#"| head -1 | cut -d',' -f2`; \
		last_x=`cat DerivedData/bond_center/$$name | sed -e "s/^ *$$//g" | grep -v -e "^$$" | grep -v -e "^#" | tail -1 | cut -d',' -f1`; \
		last_y=`cat DerivedData/bond_center/$$name | sed -e "s/^ *$$//g" | grep -v -e "^$$" | grep -v -e "^#" | tail -1 | cut -d',' -f2`; \
		echo "sqrt(( ($$first_x) - ($$last_x) )^2+( ($$first_y) - ($$last_y))^2)"|bc -l >DerivedData/chain_length/`basename $$i`; \
	done
	touch DerivedData/chain_length/__multifile__
