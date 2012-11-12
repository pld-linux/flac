#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	xmms		# don't build XMMS plugin

Summary:	Free Lossless Audio Codec
Summary(pl.UTF-8):	Free Lossless Audio Codec - Wolnodostępny bezstratny kodek audio
Name:		flac
Version:	1.2.1
Release:	7
License:	BSD (libFLAC/libFLAC++), GPL (programs and plugins)
Group:		Libraries
Source0:	http://dl.sourceforge.net/flac/%{name}-%{version}.tar.gz
# Source0-md5:	153c8b15a54da428d1f0fadc756c22c7
Patch0:		%{name}-without_xmms.patch
Patch1:		%{name}-lt.patch
Patch2:		%{name}-gcc44.patch
Patch3:		crbug-111390.patch
URL:		http://flac.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
# for AM_ICONV
BuildRequires:	gettext-devel
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d-3
%{?with_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel >= 0.9.5.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

%description -l pl.UTF-8
FLAC jest bezstratnym kodekiem audio z otwartymi źródłami, rozwijanym
przez Josha Coalsona.

%package devel
Summary:	FLAC - development files
Summary(pl.UTF-8):	FLAC - pliki nagłówkowe
License:	BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel >= 2:1.0
# for -c++ only
#Requires:	libstdc++-devel

%description devel
The package contains the development header files for FLAC libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe bibliotek FLAC.

%package static
Summary:	FLAC - static libraries
Summary(pl.UTF-8):	FLAC - biblioteki statyczne
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The package contains FLAC static libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne FLAC.

%package c++
Summary:	FLAC++ - C++ API for FLAC codec
Summary(pl.UTF-8):	FLAC++ - API C++ do kodeka FLAC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
FLAC++ - C++ API for FLAC codec.

%description c++ -l pl.UTF-8
FLAC++ - API C++ do kodeka FLAC.

%package c++-devel
Summary:	Header files for FLAC++ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FLAC++
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description c++-devel
Header files for FLAC++ library.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FLAC++.

%package c++-static
Summary:	Static FLAC++ library
Summary(pl.UTF-8):	Statyczna biblioteka FLAC++
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static FLAC++ library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka FLAC++.

%package -n xmms-input-flac
Summary:	Free Lossless Audio Codec - XMMS plugin
Summary(pl.UTF-8):	Wtyczka FLAC dla XMMS
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-flac
FLAC input plugin for XMMS.

%description -n xmms-input-flac -l pl.UTF-8
Wtyczka dla XMMS umożliwiająca odtwarzanie plików w formacie FLAC.

%prep
%setup -q
%{!?with_xmms:%patch0 -p1}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__rm} m4/ogg.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no makefiles in doc dirs
rm -f doc/html/{Makefile*,images/Makefile*,images/hw/Makefile*,ru/Makefile*}
rm -f $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.Xiph README doc/html/{*.html,images}
%lang(ru) %doc doc/html/ru
%attr(755,root,root) %{_bindir}/flac
%attr(755,root,root) %{_bindir}/metaflac
%attr(755,root,root) %{_libdir}/libFLAC.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFLAC.so.8
%{_mandir}/man1/flac.1*
%{_mandir}/man1/metaflac.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libFLAC.so
%{_libdir}/libFLAC.la
%{_includedir}/FLAC
%{_pkgconfigdir}/flac.pc
%{_aclocaldir}/libFLAC.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libFLAC.a
%endif

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libFLAC++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFLAC++.so.6

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libFLAC++.so
%{_libdir}/libFLAC++.la
%{_includedir}/FLAC++
%{_pkgconfigdir}/flac++.pc
%{_aclocaldir}/libFLAC++.m4

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libFLAC++.a
%endif

%if %{with xmms}
%files -n xmms-input-flac
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/libxmms-flac.so
%endif
