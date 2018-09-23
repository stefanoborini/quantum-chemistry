DerivedData/bond_center/__multifile__: $(wildcard SourceData/atom_position/*.csv)
	-mkdir -p DerivedData/bond_center/
	for i in SourceData/atom_position/*.csv; \
	do \
		echo $$i; \
		python Programs/bond_center.py $$i >DerivedData/bond_center/`basename $$i`; \
	done
	touch DerivedData/bond_center/__multifile__

