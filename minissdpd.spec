Summary:	MiniSSDPd - daemon keeping track of UPnP devices up
Summary(pl.UTF-8):	MiniSSDPd - demon śledzący czynne urządzenia UPnP
Name:		minissdpd
Version:	1.2
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	3f831d9586861ba5548dc2142049cb46
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://miniupnp.tuxfamily.org/minissdpd.html
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
minissdpd listen for SSDP traffic and keeps track of what are the UPnP
devices up on the network. The list of the UPnP devices is accessed by
programs looking for devices, skipping the UPnP discovery process.

%description -l pl.UTF-8
minissdpd nasłuchuje ruchu SSDP i śledzi, które urządzenia UPnP są
aktywne w sieci. Programy w poszukiwaniu urządzeń mogą odwoływać się
do listy urządzeń UPnP, pomijając proces wykrywania UPnP.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing -Wall -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/rc.d/init.d,/etc/sysconfig}

install minissdpd $RPM_BUILD_ROOT%{_sbindir}
cp -p minissdpd.1 $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc Changelog.txt LICENSE README
%attr(755,root,root) %{_sbindir}/minissdpd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man1/minissdpd.1*
