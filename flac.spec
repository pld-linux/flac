# maybe TODO: split (c++, ogg?)
#
# Conditional build:
%bcond_without	xmms	# don't build XMMS plugin
#
Summary:	Free Lossless Audio Codec
Summary(pl):	Free Lossless Audio Codec - Wolnodostêpny bezstratny kodek audio
Name:		flac
Version:	1.1.1
Release:	1
License:	GPL/LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/flac/%{name}-%{version}.tar.gz
# Source0-md5:	c6ccddccf8ad344065698047c2fc7280
Patch0:		%{name}-without_xmms.patch
URL:		http://flac.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d-3
%{?with_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel >= 0.9.5.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

%description -l pl
FLAC jest bezstratnym kodekiem audio z otwartymi ¼ród³ami, rozwijanym
przez Josha Coalsona.

%package devel
Summary:	FLAC - development files
Summary(pl):	FLAC - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The package contains the development header files for FLAC libraries.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe bibliotek FLAC.

%package static
Summary:	FLAC - static libraries
Summary(pl):	FLAC - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The package contains FLAC static libraries.

%description static -l pl
Ten pakiet zawiera biblioteki statyczne FLAC.

%package -n xmms-input-flac
Summary:	Free Lossless Audio Codec - XMMS plugin
Summary(pl):	Wtyczka FLAC dla XMMS
License:	GPL/LGPL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-flac
FLAC input plugin for XMMS.

%description -n xmms-input-flac -l pl
Wtyczka dla XMMS umo¿liwiaj±ca odtwarzanie plików w formacie FLAC.

%prep
%setup -q
%{!?with_xmms:%patch0 -p1}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

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
%doc AUTHORS README doc/html/{*.html,images}
%lang(ru) %doc doc/html/ru
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with xmms}
%files -n xmms-input-flac
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%endif
