Summary: 	Free Lossless Audio Codec
Summary(pl):	Free Lossless Audio Codec - Darmowy Bezstratny Kodek Audio
Name:		flac
Version:	1.0.3
Release:	3
License:	GPL/LGPL
Group:		Libraries
Source0:	http://prdownloads.sourceforge.net/flac/flac-1.0.3.tar.gz
Patch0:		%{name}-configure.in-aclocal.patch
URL:		http://flac.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	xmms-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xmms_input_path	%(xmms-config --input-plugin-dir)

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

%description -l pl
FLAC jest bezstratnym kodekiem audio z otwartymi ¼ród³ami, rozwijanym
przez Josha Coalsona.

%package devel
Summary:	FLAC - development files
Summary(pl):	FLAC - bilbioteki rozwojowe
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Package contains the development header files for flac.

%description devel -l pl
Paczka zawiera pliki nag³ówkowe flac.

%package static
Summary:	FLAC - static libraries
Summary(pl):	FLAC - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Package contains flac static libraries.

%description static -l pl
Paczka zawiera biblioteki statyczne flac.

%package -n xmms-input-flac
Summary: 	Free Lossless Audio Codec - XMMS plugin
Summary(pl):	Wtyczka FLAC dla XMMS
License:	GPL/LGPL
Group:		Libraries
Requires:	%{name} = %{version}
Requires:	xmms

%description -n xmms-input-flac
FLAC input plugin for XMMS.

%description -n xmms-input-flac -l pl
Wtyczka umo¿liwiaj±ca odtwarzanie plików w formacie FLAC.

%prep
%setup -q
%patch0 -p0

%build
rm -f missing
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.* 
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n xmms-input-flac
%defattr(644,root,root,755)
%{_xmms_input_path}/*
