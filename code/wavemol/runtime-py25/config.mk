ARCH=x86_64-apple-darwin10
RUNTIME_DIR=/Users/sbo/runtimes/wavemol-py25

#ARCH=x86_64-redhat-linux
#RUNTIME_DIR=$$HOME/runtimes/wavemol


THIS_DIR=$(PWD)
HOME_DIR=$$HOME
PATCH_DIR=$(THIS_DIR)/patch
TMP_DIR=$(RUNTIME_DIR)/__tmp
UNPACK_DIR=$(RUNTIME_DIR)/__unpack
BUILD_FLAGS_DIR=$(RUNTIME_DIR)/buildflags
BUILD_LOGS_DIR=$(RUNTIME_DIR)/buildlogs
DOWNLOAD_DIR=$(RUNTIME_DIR)/download
OPT_DIR=$(RUNTIME_DIR)/opt
MANUAL_INSTALL=$(RUNTIME_DIR)/manual_install

LIBS=-L$(RUNTIME_DIR)/lib
INCLUDES=-I$(RUNTIME_DIR)/include

