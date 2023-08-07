# This Makefile is to compile SRW with optional compilation of FFTW-2.1.5.

root_dir = $(realpath .)
fftw_lib_dir = $(root_dir)/ext_lib
gcc_dir = $(root_dir)/gcc

fftw2_version = fftw-2.1.5
fftw2_dir = $(fftw2_version)
fftw2_file = $(fftw2_version).tar.gz
fftw3_version = fftw-3.3.8
fftw3_dir = $(fftw3_version)
fftw3_file = $(fftw3_version).tar.gz

nofftw: core

all: clean fftw core

fftw:
	cd $(fftw_lib_dir); \
	tar -zxf $(fftw2_file); \
	cd $(fftw2_dir); \
	./configure --enable-float --with-pic; \
	sed 's/^CFLAGS = /CFLAGS = -fPIC /' -i Makefile; \
	make -j8 && cp fftw/.libs/libfftw.a $(gcc_dir); \
	cd $(fftw_lib_dir); \
	rm -rf $(fftw2_dir); \
	if [ -d "$(fftw3_dir)" ]; then \
	    rm -rf $(fftw3_dir); \
	fi; \
	tar -zxf $(fftw3_file); \
	cd $(fftw3_dir); \
	./configure --enable-float --with-pic; \
	sed 's/^CFLAGS = /CFLAGS = -fPIC /' -i Makefile; \
	make -j8 && cp .libs/libfftw3f.a $(gcc_dir); \
	cd $(fftw_lib_dir); \
	rm -rf $(fftw3_dir); \
	tar -zxf $(fftw3_file); \
	cd $(fftw3_dir); \
	./configure --with-pic; \
	sed 's/^CFLAGS = /CFLAGS = -fPIC /' -i Makefile; \
	make -j8 && cp .libs/libfftw3.a $(gcc_dir); \
	rm -rf $(fftw3_dir); \
	cd $(root_dir);

core:
	cd $(gcc_dir) && make -j8 lib;

clean:
	rm -f $(gcc_dir)/libfftw3f.a $(gcc_dir)/libfftw3.a $(gcc_dir)/libsrw.a && \
	rm -rf $(fftw_lib_dir)/$(fftw2_dir)/ rm -rf $(fftw_lib_dir)/$(fftw3_dir)/

.PHONY: all clean core fftw nofftw
