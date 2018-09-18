RDFLIB_VERSION=2.4.2
RDFLIB_TARGET=$(BUILD_FLAGS_DIR)/rdflib

rdflib: $(RDFLIB_TARGET)

$(RDFLIB_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(RDFLIB_PACKAGE)
	export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.5/site-packages/; \
	$(RUNTIME_DIR)/bin/easy_install-2.5 --prefix=$(RUNTIME_DIR) rdflib==$(RDFLIB_VERSION)
	touch $(RDFLIB_TARGET)


ALL_RUNTIME_TARGETS+=$(RDFLIB_TARGET)
