Summary:	MiniSSDPd - daemon keeping track of UPnP devices up
Summary(pl.UTF-8):	MiniSSDPd - demon śledzący czynne urządzenia UPnP
Name:		minissdpd
Version:	1.5
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	be556df1550f49aedd39172ca0a68f48
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://miniupnp.tuxfamily.org/minissdpd.html
BuildRequires:	libnfnetlink-devel
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
CFLAGS="%{rpmcflags}" \
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT

# replace init script by PLD specific one
%{__rm} -r $RPM_BUILD_ROOT/etc/init.d
install -Dp %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -Dp %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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
%lang(fr) %doc README.fr
%attr(755,root,root) %{_sbindir}/minissdpd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man1/minissdpd.1*
