DerivedData/bond_center_distance/__multifile__: DerivedData/bond_center/__multifile__ DerivedData/bond_center_regression/__multifile__
	-mkdir -p DerivedData/bond_center_distance/
	for i in DerivedData/bond_center/*.csv; \
	do \
		echo $$i; \
		python Programs/distance_point_from_line.py DerivedData/bond_center_regression/`basename $$i` DerivedData/bond_center/`basename $$i` >DerivedData/bond_center_distance/`basename $$i`; \
	done
	touch DerivedData/bond_center_distance/__multifile__
