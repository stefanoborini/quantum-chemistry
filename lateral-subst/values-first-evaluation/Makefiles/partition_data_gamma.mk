DerivedData/partition_data/gamma_3_double_NO2_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_double.csv |grep NO2 | grep -v NH2 >"$@"

DerivedData/partition_data/gamma_3_double_NH2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_double.csv |grep NH2 | grep -v NO2 >"$@"

DerivedData/partition_data/gamma_3_double_NO2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_double.csv |grep NH2 | grep NO2 >"$@"

DerivedData/partition_data/gamma_6_double_NO2_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_double.csv |grep NO2 | grep -v NH2 >"$@"

DerivedData/partition_data/gamma_6_double_NH2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_double.csv |grep NH2 | grep -v NO2 >"$@"

DerivedData/partition_data/gamma_6_double_NO2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_double.csv |grep NH2 | grep NO2 >"$@"

DerivedData/partition_data/gamma_9_double_NO2_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_double.csv |grep NO2 | grep -v NH2 >"$@"

DerivedData/partition_data/gamma_9_double_NH2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_double.csv |grep NH2 | grep -v NO2 >"$@"

DerivedData/partition_data/gamma_9_double_NO2_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_double.csv |grep NH2 | grep NO2 >"$@"

DerivedData/partition_data/gamma_3_single_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_single.csv |grep NO2 >"$@"

DerivedData/partition_data/gamma_3_single_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_single.csv |grep NH2 >"$@"

DerivedData/partition_data/gamma_3_single_H.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_3_single.csv |grep -v NH2 |grep -v NO2 >"$@"

DerivedData/partition_data/gamma_6_single_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_single.csv |grep NO2 >"$@"

DerivedData/partition_data/gamma_6_single_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_single.csv |grep NH2 >"$@"

DerivedData/partition_data/gamma_6_single_H.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_6_single.csv |grep -v NH2 |grep -v NO2 >"$@"

DerivedData/partition_data/gamma_9_single_NO2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_single.csv |grep NO2 >"$@"

DerivedData/partition_data/gamma_9_single_NH2.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_single.csv |grep NH2 >"$@"

DerivedData/partition_data/gamma_9_single_H.csv: $(wildcard SourceData/raw/*.csv)
	-mkdir -p DerivedData/partition_data/
	cat SourceData/raw/gamma_9_single.csv |grep -v NH2 |grep -v NO2 >"$@"

