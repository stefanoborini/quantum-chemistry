SIMPLEJSON_VERSION=2.0.9
SIMPLEJSON_TARGET=$(BUILD_FLAGS_DIR)/simplejson

simplejson: $(SIMPLEJSON_TARGET)

$(SIMPLEJSON_TARGET): $(INIT_TARGET) $(DOWNLOAD_DIR)/$(SIMPLEJSON_PACKAGE)
	export PATH=$(RUNTIME_DIR)/bin:$$PATH PYTHONPATH=$(RUNTIME_DIR)/lib/python2.4/site-packages/; \
	$(RUNTIME_DIR)/bin/easy_install-2.4 --prefix=$(RUNTIME_DIR) simplejson==2.0.9
	touch $(SIMPLEJSON_TARGET)


ALL_RUNTIME_TARGETS+=$(SIMPLEJSON_TARGET)