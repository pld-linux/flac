# TODO: split (c++, ogg?)
#
# Conditional build:
#  _without xmms
Summary:	Free Lossless Audio Codec
Summary(pl):	Free Lossless Audio Codec - Darmowy Bezstratny Kodek Audio
Name:		flac
Version:	1.1.0
Release:	3
License:	GPL/LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	19b456a27b5fcf502c76cc33f33e1490
Patch0:		%{name}-lt.patch
Patch1:		%{name}-without_xmms.patch
URL:		http://flac.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libogg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{!?_without_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{!?_without_xmms:BuildRequires:	xmms-devel}
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
Requires:	%{name} = %{version}

%description devel
The package contains the development header files for flac.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki flac.

%package static
Summary:	FLAC - static libraries
Summary(pl):	FLAC - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
The package contains flac static libraries.

%description static -l pl
Ten pakiet zawiera biblioteki statyczne flac.

%package -n xmms-input-flac
Summary:	Free Lossless Audio Codec - XMMS plugin
Summary(pl):	Wtyczka FLAC dla XMMS
License:	GPL/LGPL
Group:		Libraries
Requires:	%{name} = %{version}
Requires:	xmms

%description -n xmms-input-flac
FLAC input plugin for XMMS.

%description -n xmms-input-flac -l pl
Wtyczka dla XMMS umo¿liwiaj±ca odtwarzanie plików w formacie FLAC.

%prep
%setup -q
%patch0 -p1
%{?_without_xmms:%patch1 -p1}

%build
rm -f missing
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

%if %{!?_without_xmms:1}0
%files -n xmms-input-flac
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%{xmms_input_plugindir}/*.la
%endif
