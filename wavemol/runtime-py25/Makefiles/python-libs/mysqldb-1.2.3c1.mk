MYSQLDB_VERSION=1.2.3c1
MYSQLDB_TARGET=$(BUILD_FLAGS_DIR)/mysqldb
MYSQLDB_PACKAGE=MySQL-python-$(MYSQLDB_VERSION).tar.gz
MYSQLDB_PACKAGE_URL=http://downloads.sourceforge.net/project/mysql-python/mysql-python-test/$(MYSQLDB_VERSION)/$(MYSQLDB_PACKAGE)

.PHONY: mysqldb mysqldb-download
mysqldb: $(MYSQLDB_TARGET)
mysqldb-download: $(DOWNLOAD_DIR)/$(MYSQLDB_PACKAGE)

$(MYSQLDB_TARGET): $(INIT_TARGET) $(MYSQLDB_DEPS) $(DOWNLOAD_DIR)/$(MYSQLDB_PACKAGE)
	-rm -rf $(UNPACK_DIR)/MySQL-python-$(MYSQLDB_VERSION)
	tar -m -C $(UNPACK_DIR) -xzvf $(DOWNLOAD_DIR)/$(MYSQLDB_PACKAGE)
	-cd $(UNPACK_DIR)/MySQL-python-$(MYSQLDB_VERSION); \
	for patch in $(PATCH_DIR)/mysqldb-$(MYSQLDB_VERSION)_$(ARCH)_*; \
		do patch -p1 < $$patch; \
	done
	cd $(UNPACK_DIR)/MySQL-python-$(MYSQLDB_VERSION); export CC="gcc -m64" FC="g95 -m64" CPPFLAGS="-I$(RUNTIME_DIR)/include" CFLAGS="-m64 -I$(RUNTIME_DIR)/include" LD_LIBRARY_PATH=$(RUNTIME_DIR)/lib64:$(RUNTIME_DIR)/lib:$$LD_LIBRARY_PATH PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; $(RUNTIME_DIR)/bin/python2.5 setup.py install --prefix=$(RUNTIME_DIR)
	touch $(MYSQLDB_TARGET)

$(DOWNLOAD_DIR)/$(MYSQLDB_PACKAGE): $(INIT_TARGET)
	for package in $(MYSQLDB_PACKAGE_URL); \
	do \
		echo -n "Downloading $$package... ";  \
		cd $(DOWNLOAD_DIR); curl -L -O $$package; \
		echo "done"; \
	done
	touch $@

ALL_RUNTIME_TARGETS+=$(MYSQLDB_TARGET)
ALL_DOWNLOAD_TARGETS+=$(DOWNLOAD_DIR)/$(MYSQLDB_PACKAGE)
