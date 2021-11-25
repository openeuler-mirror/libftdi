Name:		libftdi
Version:	1.4
Release:	1
Summary:	Library to program and control the FTDI USB controller
License:	LGPL-2.0-only
URL:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/en/developer/%{name}/download/%{name}1-%{version}.tar.bz2

# Swig requirements have changed in newer versions of CMake.
# This has been reported to the mailing list
Patch0:         libftdi-cmake_swig.patch

BuildRequires:	cmake3 gcc-c++ doxygen boost-devel libconfuse-devel libusbx-devel python3-devel swig
Requires:	systemd

%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%package devel
Summary:	Header files and static libraries for libftdi
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and static libraries for libftdi

%package -n python3-libftdi
%{?python_provide:%python_provide python3-libftdi}
Summary:	Libftdi library Python 3 binding
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python3-libftdi
Libftdi Python 3 Language bindings.

%package c++
Summary:	Libftdi library C++ binding
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description c++
Libftdi library C++ language binding.

%package c++-devel
Summary:	Libftdi library C++ binding development headers and libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-c++ = %{version}-%{release}

%description c++-devel
Libftdi library C++ binding development headers and libraries
for building C++ applications with libftdi.

%prep
%autosetup -p1 -n %{name}1-%{version}

# switch to uaccess control
sed -i -e 's/GROUP="plugdev"/TAG+="uaccess"/g' packages/99-libftdi.rules

%build
export CMAKE_PREFIX_PATH=%{_prefix}

mkdir build-py3 && pushd build-py3
%{cmake3} -DPython_ADDITIONAL_VERSIONS=%{python3_version} ..
%make_build
popd

# Fix python sheband lines
find python/examples -type f -exec sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

%install
pushd build-py3
%make_install
popd

mkdir -p %{buildroot}/lib/udev/rules.d/
install -pm 0644 packages/99-libftdi.rules %{buildroot}/lib/udev/rules.d/69-libftdi.rules

find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

#no man install
mkdir -p %{buildroot}%{_mandir}/man3
install -pm 0644 build-py3/doc/man/man3/*.3 %{buildroot}%{_mandir}/man3

# Cleanup examples
rm -f %{buildroot}%{_bindir}/simple
rm -f %{buildroot}%{_bindir}/bitbang
rm -f %{buildroot}%{_bindir}/bitbang2
rm -f %{buildroot}%{_bindir}/bitbang_ft2232
rm -f %{buildroot}%{_bindir}/bitbang_cbus
rm -f %{buildroot}%{_bindir}/find_all
rm -f %{buildroot}%{_bindir}/find_all_pp
rm -f %{buildroot}%{_bindir}/baud_test
rm -f %{buildroot}%{_bindir}/serial_read
rm -f %{buildroot}%{_bindir}/serial_test
rm -rf %{buildroot}%{_libdir}/cmake*
rm -rf %{buildroot}%{_datadir}/doc/libftdi1/example.conf

%check
#make check

%files
%license COPYING.LIB
%doc AUTHORS ChangeLog README
%{_libdir}/libftdi1.so.2*
/lib/udev/rules.d/69-libftdi.rules

%files devel
%doc build-py3/doc/html
%doc %{_datadir}/libftdi/examples
%{_bindir}/ftdi_eeprom
%{_bindir}/libftdi1-config
%{_libdir}/libftdi1.so
%{_includedir}/libftdi1
%{_libdir}/pkgconfig/libftdi1.pc
%{_mandir}/man3/*

%files -n python3-libftdi
%{python3_sitearch}/*

%files c++
%{_libdir}/libftdipp1.so.2*
%{_libdir}/libftdipp1.so.3

%files c++-devel
%{_libdir}/libftdipp1.so
%{_includedir}/libftdi1/*hpp
%{_libdir}/pkgconfig/libftdipp1.pc

%ldconfig_scriptlets
%ldconfig_scriptlets c++

%changelog
* Fri Dec 10 2021 zhangshaoning <zhangshaoning@uniontech.com> - 1.4-1
- init package
