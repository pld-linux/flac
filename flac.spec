Summary: 	Free Lossless Audio Codec
Summary(pl):	Free Lossless Audio Codec - Darmowy Ma³ostratny Kodek Audio.
Name:		flac
Version:	1.0.3
Release:	1
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
FLAC jest OpenSourcoweo± ma³ostratnym kodekiem audio rozwijanym
przez Josh'a Coalsona.

%package devel
Summary:	FLAC - development files.
Summary(pl):	FLAC - bilbioteki rozwojowe.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Package contains a development header files and libraries.

%description devel -l pl
Paczka zawiera pliki nag³ówkowe oraz biblioteki.

%package static
Summary:	FLAC - static libraries.
Summary(pl):	FLAC - biblioteki statyczne.
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Package contains a static libraries.

%description static -l pl
Paczka zawiera biblioteki statyczne.

%package -n xmms-input-flac
Summary: 	Free Lossless Audio Codec	
License:	GPL/LGPL
Group:		Libraries
Requires:	%{name} = %{version}
Requires:	xmms

%description -n xmms-input-flac
FLAC input plugin for XMMS.

%description -l pl -n xmms-input-flac
Wtyczka umo¿liwiaj±ca odtwarzanie plikow w formacie FLAC.

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
%doc doc/*
%defattr(644,root,root,755)
%{_bindir}/*
%{_libdir}/lib*.so.*.* 
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n xmms-input-flac
%defattr(644,root,root,755)
%{_xmms_input_path}/*
