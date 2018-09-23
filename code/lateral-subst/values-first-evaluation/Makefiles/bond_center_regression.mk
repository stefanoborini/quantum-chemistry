DerivedData/bond_center_regression/__multifile__: DerivedData/bond_center/__multifile__
	-mkdir -p DerivedData/bond_center_regression/
	for i in DerivedData/bond_center/*.csv; \
	do \
		echo $$i; \
		cnrun csvUtils-1/linreg $$i | sed -e "s/^ *$$//g" | grep -v -e "^$$" | grep -v -e "^#" >DerivedData/bond_center_regression/`basename $$i`; \
	done
	touch DerivedData/bond_center_regression/__multifile__
