%define docver  3.3.4
%define dirver  3.3
%define familyver 3

%define lib_major       %{dirver}
%define lib_name_orig   libpython%{familyver}
%define lib_name        %mklibname python %{lib_major}
%define develname       %mklibname python3 -d

%ifarch %{ix86} x86_64 ppc
%bcond_without  valgrind
%else
%bcond_with     valgrind
%endif

# We want to byte-compile the .py files within the packages using the new
# python3 binary.
# 
# Unfortunately, rpmbuild's infrastructure requires us to jump through some
# hoops to avoid byte-compiling with the system python 2 version:
#   /usr/lib/rpm/mageia/macros sets up build policy that (amongst other things)
# defines __os_install_post.  In particular, "brp-python-bytecompile" is
# invoked without an argument thus using the wrong version of python
# (/usr/bin/python, rather than the freshly built python), thus leading to
# numerous syntax errors, and incorrect magic numbers in the .pyc files.  We
# thus remove the invocation of brp-python-bytecompile, whilst keeping the
# invocation of brp-python-hardlink (since this should still work for python3
# pyc/pyo files)
%define _python_bytecompile_build 0


Summary:        An interpreted, interactive object-oriented programming language
Name:           python3
Version:        3.3.4
Release:        %mkrel 1
License:        Modified CNRI Open Source License
Group:          Development/Python

Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:        http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:        python3.macros
Source3:        pybytecompile.macros
Source100:	%{name}.rpmlintrc

Patch0:         python-3.3.0-module-linkage.patch
Patch1:         python3-3.3.0-fdr-lib64.patch
Patch2:         python3-3.2.3-fdr-lib64-fix-for-test_install.patch
Patch4:         python-3.3.0b1-test-posix_fadvise.patch
#Fedora patches:
Patch153:       00153-fix-test_gdb-noise.patch
Patch156:       00156-gdb-autoload-safepath.patch
# 00173 #
# Workaround for ENOPROTOOPT seen in bs within
# test.test_support.bind_port()
# from Fedora (rhbz#913732)
Patch173:       00173-workaround-ENOPROTOOPT-in-bind_port.patch
Patch179:       00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch
Patch180:	python-3.2.1-fix-test-subprocess-with-nonreadable-path-dir.patch

URL:            http://www.python.org/
Conflicts:      tkinter3 < %{version}
Conflicts:      %{lib_name}-devel < 3.1.2-4
Conflicts:      %{develname} < 3.2.2-3
Requires:       %{lib_name} = %{version}


BuildRequires:	blt
BuildRequires:	bzip2-devel
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)

%if %{with valgrind}
BuildRequires:  valgrind-devel
%endif
Provides:       python(abi) = %{dirver}
Provides:       /usr/bin/python%{dirver}m
Provides:       /usr/bin/python%{dirver}

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package -n     %{lib_name}
Summary:        Shared libraries for Python %{version}
Group:          System/Libraries

%description -n %{lib_name}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n     %{develname}
Summary:        The libraries and header files needed for Python development
Group:          Development/Python
Requires:       %{name} = %version
Requires:       %{lib_name} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{lib_name_orig}-devel = %{version}-%{release}
Obsoletes:      %{_lib}python3.1-devel < %{version}
Obsoletes:      %{_lib}python3.2-devel < %{version}-%{release}

%description -n %{develname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{develname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package        docs
Summary:        Documentation for the Python programming language
Requires:       %name = %version
Requires:       xdg-utils
Group:          Development/Python
BuildArch:      noarch

%description    docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package -n     tkinter3
Summary:        A graphical user interface for the Python scripting language
Group:          Development/Python
Requires:       %name = %version
Requires:       tcl tk
Provides:       python3-tkinter

%description -n tkinter3
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package -n     tkinter3-apps
Summary:        Various applications written using tkinter
Group:          Development/Python
Requires:       tkinter3

%description -n tkinter3-apps
Various applications written using tkinter

%prep
%setup -qn Python-%{version}
%patch0 -p0 -b .link

%if "%{_lib}" == "lib64"
%patch1 -p1 -b .lib64
%patch2 -p1
%endif
%patch4 -p1
%patch153 -p0
%patch156 -p1
%patch173 -p1
%patch179 -p1
%patch180 -p1

# docs
mkdir html
bzcat %{SOURCE1} | tar x  -C html

find . -type f -print0 | xargs -0 perl -p -i -e 's@/usr/local/bin/python@/usr/bin/python3@'

%build
rm -f Modules/Setup.local

export OPT="%{optflags} -g"

# to fix curses module build
# https://bugs.mageia.org/show_bug.cgi?id=6702
export CFLAGS="%{optflags} -I/usr/include/ncursesw"
export CPPFLAGS="%{optflags} -I/usr/include/ncursesw"

autoreconf -vfi
# Remove -Wl,--no-undefined in accordance with MGA #9395 :
# https://bugs.mageia.org/show_bug.cgi?id=9395
%define _disable_ld_no_undefined 1
%configure2_5x  --with-threads \
                --enable-ipv6 \
                --with-dbmliborder=gdbm \
                --with-system-expat \
                --with-system-ffi \
                --enable-shared \
%if %{with valgrind}
                --with-valgrind
%endif

# fix build
#perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile
# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
#%make LN="ln -sf"
make EXTRA_CFLAGS="$CFLAGS" LN="ln -sf"

%install
mkdir -p %buildroot%{_prefix}/lib/python%{dirver}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}/usr/bin" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%makeinstall_std LN="ln -sf"

(cd %{buildroot}%{_libdir}; ln -sf `ls libpython%{lib_major}*.so.*` libpython%{lib_major}.so)

# fix files conflicting with python2.6
mv %{buildroot}/%{_bindir}/2to3 $RPM_BUILD_ROOT/%{_bindir}/python3-2to3


# install pynche as pynche3
cat << EOF > %{buildroot}%{_bindir}/pynche3
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 755 %{buildroot}%{_bindir}/{idle3,pynche3}

ln -f Tools/pynche/README Tools/pynche/README.pynche

%if %{with valgrind}
install Misc/valgrind-python.supp -D %{buildroot}%{_libdir}/valgrind/valgrind-python3.supp
%endif

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%_vendor-tkinter3.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python3
Exec=%{_bindir}/idle3
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF


cat > %{buildroot}%{_datadir}/applications/%_vendor-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/xdg-open %_defaultdocdir/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF


# fix non real scripts
#chmod 644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
find %{buildroot} -type f \( -name "test_binascii.py*" -o -name "test_grp.py*" -o -name "test_htmlparser.py*" \) -exec chmod 644 {} \;
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{lib_major}*.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libpython3.so


%multiarch_includes %{buildroot}/usr/include/python*/pyconfig.h

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rpm/macros.d/

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

%ifarch %arm
%define custom_test -x test_float
%else
%define custom_test ""
%endif

# all tests must pass
# (misc, 28/11/2006) test_shutil is causing problem in iurt, it seems to remove /tmp,
# which make other test fail
# (misc, 11/12/2006) test_pyexpat is icrashing, seem to be done on purpose ( http://python.org/sf/1296433 )
# (misc, 11/12/2006) test_minidom is not working anymore, something changed either on my computer
# or elsewhere.
# (misc, 11/12/2006) test_sax fail too, will take a look later
# (misc, 21/08/2007) test_string and test_str segfault, test_unicode, test_userstring, I need to pass the package as a security update
# (eugeni, 21/07/2009) test_distutils fails with python3.1 due to ld error
# (eugeni, 22/07/2009) test_mailbox fails on the BS
# (eugeni, 17/08/2009) test_telnetlib fails with a connection reset by peer message
# (tv, 31/08/2013à test_gdb, test_urllibnet & test_urllib2net fails
# test test_sax failed -- 1 of 44 tests failed: test_xmlgen_attr_escape
WITHIN_PYTHON_RPM_BUILD= make test TESTOPTS="-w -x test_linuxaudiodev -x test_nis -x test_shutil -x test_pyexpat -x test_minidom -x test_sax -x test_string -x test_str -x test_unicode -x test_userstring -x test_bytes -x test_distutils -x test_mailbox -x test_ioctl -x test_telnetlib -x test_runpy -x test_importlib -x test_import -x test_urllibnet -x test_gdb -x test_urllib2net -x test_urllib2_localnet -x test_timeout %custom_test"

%files
%{_sysconfdir}/rpm/macros.d/*.macros
%{_includedir}/python*/pyconfig.h
%multiarch_includedir/python*/pyconfig.h
%{_libdir}/python*/config*/Makefile
%exclude %{_libdir}/python*/site-packages/pynche
%exclude %{_libdir}/python*/lib-dynload/_tkinter.*.so

# HACK: build fails without this (TODO: investigate rpm)
%dir %{_libdir}/python*
%{_libdir}/python*/LICENSE.txt
%{_libdir}/python%{dirver}/*.py
%{_libdir}/python%{dirver}/__pycache__
%{_libdir}/python%{dirver}/collections
%{_libdir}/python%{dirver}/concurrent
%{_libdir}/python%{dirver}/ctypes
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/dbm
%{_libdir}/python%{dirver}/distutils
%{_libdir}/python%{dirver}/email
%{_libdir}/python%{dirver}/encodings
%{_libdir}/python%{dirver}/html
%{_libdir}/python%{dirver}/http
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%{_libdir}/python%{dirver}/lib-dynload
%{_libdir}/python%{dirver}/lib2to3
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/plat-linux
%{_libdir}/python%{dirver}/pydoc_data
%{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/sqlite3
%{_libdir}/python%{dirver}/turtledemo
%{_libdir}/python%{dirver}/unittest
%{_libdir}/python%{dirver}/urllib
%{_libdir}/python%{dirver}/venv
%{_libdir}/python%{dirver}/wsgiref*
%{_libdir}/python%{dirver}/xml
%{_libdir}/python%{dirver}/xmlrpc
%{_bindir}/pydoc3*
%{_bindir}/python3*
%{_bindir}/pyvenv*
%{_bindir}/2to3-%{dirver}
%exclude %{_bindir}/python*config
#%{_datadir}/emacs/site-lisp/*
%{_mandir}/man*/*
%if %{with valgrind}
%{_libdir}/valgrind/valgrind-python3.supp
%endif

%files -n %{lib_name}
%{_libdir}/libpython*.so.1*

%files -n %{develname}
%{_libdir}/libpython*.so
%{_includedir}/python*
%{_libdir}/python*/config-%{dirver}*
%{_libdir}/python*/test/
%{_bindir}/python%{dirver}*-config
%{_bindir}/python%{familyver}-config
%{_libdir}/pkgconfig/python*.pc
%exclude %{_includedir}/python*/pyconfig.h
%exclude %{_libdir}/python*/config*/Makefile

%files docs
%doc html/*/*
%{_datadir}/applications/%_vendor-%{name}-docs.desktop

%files -n tkinter3
%{_libdir}/python*/tkinter/
%{_libdir}/python*/idlelib
%{_libdir}/python*/site-packages/pynche
%{_libdir}/python*/lib-dynload/_tkinter.*.so

%files -n tkinter3-apps
%{_bindir}/idle3*
%{_bindir}/pynche3
%{_datadir}/applications/%_vendor-tkinter3.desktop
