DerivedData/accurate_single_bond_length/__multifile__: $(wildcard SourceData/atom_position/*.csv)
	-mkdir -p DerivedData/accurate_single_bond_length/
	for i in SourceData/atom_position/*.csv; \
	do \
		echo $$i; \
		python Programs/accurate_single_bond_length.py $$i >DerivedData/accurate_single_bond_length/`basename $$i`; \
	done

