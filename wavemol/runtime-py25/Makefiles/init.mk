INIT_TARGET=$(BUILD_FLAGS_DIR)/init

.PHONY: init
init: $(INIT_TARGET)

$(INIT_TARGET): 
	-mkdir -p $(DOWNLOAD_DIR)
	-mkdir -p $(UNPACK_DIR)
	-mkdir -p $(RUNTIME_DIR)
	-mkdir -p $(BUILD_FLAGS_DIR)
	-mkdir -p $(BUILD_LOGS_DIR)
	-mkdir -p $(OPT_DIR)
	touch $(INIT_TARGET)


