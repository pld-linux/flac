#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Free Lossless Audio Codec
Summary(pl.UTF-8):	Free Lossless Audio Codec - Wolnodostępny bezstratny kodek audio
Name:		flac
Version:	1.4.2
Release:	1
License:	BSD (libFLAC/libFLAC++), GPL v2+ (programs and plugins)
Group:		Libraries
Source0:	https://downloads.xiph.org/releases/flac/%{name}-%{version}.tar.xz
# Source0-md5:	ca9140f37b286d2571e37d66aae50f92
URL:		https://xiph.org/flac/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	doxygen
# for AM_ICONV
BuildRequires:	gettext-tools
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	xmms-input-flac < 1.4.2
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
Requires:	libstdc++-devel

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

%prep
%setup -q

%{__rm} m4/ogg.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc in -devel
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.Xiph README.md
%attr(755,root,root) %{_bindir}/flac
%attr(755,root,root) %{_bindir}/metaflac
%attr(755,root,root) %{_libdir}/libFLAC.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFLAC.so.12
%{_mandir}/man1/flac.1*
%{_mandir}/man1/metaflac.1*

%files devel
%defattr(644,root,root,755)
%doc doc/api/*.{html,png} doc/images/logo*.{gif,svg}
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
%attr(755,root,root) %ghost %{_libdir}/libFLAC++.so.10

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
