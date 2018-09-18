include config.mk
# collects all the runtime targets one by one.
ALL_RUNTIME_TARGETS=
ALL_DOWNLOAD_TARGETS=

default: all

include Makefiles/init.mk
# compiler suite
include Makefiles/gmp-4.2.4.mk
include Makefiles/mpfr-2.3.1.mk
include Makefiles/gcc-4.3.4.mk
# support C libs
include Makefiles/lapack-3.2.0.mk
include Makefiles/fftw-3.2.2.mk
include Makefiles/umfpack-5.2.mk
include Makefiles/readline-5.2.mk
include Makefiles/libpng-1.2.40.mk
include Makefiles/freetype-2.3.11.mk
# python 
include Makefiles/python-2.4.6.mk
include Makefiles/ipython-0.10.mk
include Makefiles/setuptools-0.6c9.mk
include Makefiles/numpy-1.3.0.mk
include Makefiles/scipy-0.7.1.mk
include Makefiles/matplotlib-0.99.0.mk
include Makefiles/unum-4.0.mk
include Makefiles/simplejson-2.0.9.mk
#other
include Makefiles/openbabel-2.2.3.mk
include Makefiles/graphviz-2.24.0.mk
include Makefiles/mysqldb-1.2.3c1.mk

clean:
	-rm -rf $(TMP_DIR) $(UNPACK_DIR)

all: $(ALL_RUNTIME_TARGETS)
download-all: $(ALL_DOWNLOAD_TARGETS)

distclean: clean
	-rm -rf $(RUNTIME_DIR)
packageclean: 
	-rm -rf $(DOWNLOAD_DIR)
