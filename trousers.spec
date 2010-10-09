# TODO: tcsd init script (see dist/fedora/fedora.initrd.tcsd)
#
# Conditional build:
%bcond_with	gtk	# use GTK+ popups instead of openssl
#
Summary:	TrouSerS - The open-source TCG Software Stack
Summary(pl.UTF-8):	TrouSerS - programowy stos TCG o otwartych źródłach
Name:		trousers
Version:	0.3.6
Release:	1
License:	CPL v1.0
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/trousers/%{name}-%{version}.tar.gz
# Source0-md5:	f4609e6446099e1403e23bb671df87f4
Patch0:		%{name}-nouser.patch
URL:		http://trousers.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.6
%{?with_gtk:BuildRequires:	gtk+2-devel >= 1:2.0.0}
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(tss)
Provides:	user(tss)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TrouSerS is an open-source TCG Software Stack (TSS), released under
the Common Public License. TrouSerS aims to be compliant with the 1.1b
and 1.2 TSS specifications available from the Trusted Computing Group
website: <http://www.trustedcomputinggroup.org/>.

%description -l pl.UTF-8
TrouSerS to programowy stos TCG (TSS, czyli TCG Software Stack) o
otwartych źródłach wydany na licencji Common Public License. Celem
projektu jest zgodność ze specyfikacjami TSS 1.1b i 1.2 dostępnymi na
stronie Trusted Computing Group:
<http://www.trustedcomputinggroup.org/>.

%package libs
Summary:	TrouSerS shared library
Summary(pl.UTF-8):	Biblioteka współdzielona TrouSerS
Group:		Libraries

%description libs
TrouSerS shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona TrouSerS.

%package devel
Summary:	Header files for TrouSerS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki TrouSerS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_gtk:Requires:	gtk+2-devel >= 1:2.0.0}
Requires:	openssl-devel

%description devel
Header files for TrouSerS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki TrouSerS.

%package static
Summary:	Static TrouSerS library
Summary(pl.UTF-8):	Statyczna biblioteka TrouSerS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static TrouSerS library.

%description static -l pl.UTF-8
Statyczna biblioteka TrouSerS.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-static \
	%{?with_gtk:--with-gui=gtk}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 139 tss
%useradd -u 139 -d %{_localstatedir}/lib/tpm -s /bin/false -c "TrouSerS user" -g tss tss

%postun
if [ "$1" = "0" ]; then
	%userremove tss
	%groupremove tss
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE NICETOHAVES README README.selinux TODO
%attr(755,root,root) %{_sbindir}/tcsd
%attr(640,root,tss) %{_sysconfdir}/tcsd.conf
%attr(700,tss,tss) %{_localstatedir}/lib/tpm
%{_mandir}/man5/tcsd.conf.5*
%{_mandir}/man8/tcsd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtspi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtspi.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/{LTC-TSS_LLD_08_r2.pdf,TSS_programming_SNAFUs.txt}
%attr(755,root,root) %{_libdir}/libtspi.so
%{_libdir}/libtspi.la
%{_libdir}/libtddl.a
%{_includedir}/trousers
%{_includedir}/tss
%{_mandir}/man3/Tspi_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtspi.a
