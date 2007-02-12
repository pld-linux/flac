# TODO: separate c++
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	xmms		# don't build XMMS plugin
#
Summary:	Free Lossless Audio Codec
Summary(pl.UTF-8):	Free Lossless Audio Codec - Wolnodostępny bezstratny kodek audio
Name:		flac
Version:	1.1.3
Release:	1
License:	BSD (libFLAC/libFLAC++), GPL (programs and plugins)
Group:		Libraries
Source0:	http://dl.sourceforge.net/flac/%{name}-%{version}.tar.gz
# Source0-md5:	b084603948b60ee338e0c29978cc580c
Patch0:		%{name}-link.patch
Patch1:		%{name}-without_xmms.patch
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
%patch0 -p1
%{!?with_xmms:%patch1 -p1}

%build
%{__libtoolize}
%{__aclocal}
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
rm -f doc/html/{Makefile*,images/Makefile*,ru/Makefile*}
rm -f $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.Xiph README doc/html/{*.html,images}
%lang(ru) %doc doc/html/ru
%attr(755,root,root) %{_bindir}/flac
%attr(755,root,root) %{_bindir}/metaflac
%attr(755,root,root) %{_libdir}/libFLAC.so.*.*.*
%attr(755,root,root) %{_libdir}/libFLAC++.so.*.*.*
%{_mandir}/man1/flac.1*
%{_mandir}/man1/metaflac.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libFLAC.so
%attr(755,root,root) %{_libdir}/libFLAC++.so
%{_libdir}/libFLAC.la
%{_libdir}/libFLAC++.la
%{_includedir}/FLAC
%{_includedir}/FLAC++
%{_aclocaldir}/libFLAC.m4
%{_aclocaldir}/libFLAC++.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libFLAC.a
%{_libdir}/libFLAC++.a
%endif

%if %{with xmms}
%files -n xmms-input-flac
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/libxmms-flac.so
%endif
