%define debug_package %{nil}

%define  uid   blackboxexporter
%define  gid   blackboxexporter
%define  nuid  7974
%define  ngid  7974

Name:          blackbox_exporter
Summary:       Blackbox exporter
Version:       0.26.0
Release:       2%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS,
DNS, TCP and ICMP.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

# install binary
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service

# install systemd environment file
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/default/%{name}

# install configuration
install -p -D -m 0644 \
   blackbox.yml \
   %{buildroot}%{_sysconfdir}/%{name}/blackbox.yml

%clean
rm -rf %{buildroot}


%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -u %{nuid} -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%license LICENSE
%doc NOTICE


%changelog
* Thu Feb 27 2025 Lars Kiesow <lkiesow@uos.de> - 0.26.0-2
- Update to 0.26.0

* Wed Apr 10 2024 Lars Kiesow <lkiesow@uos.de> - 0.25.0-2
- Update to 0.25.0

* Wed May 17 2023 Lars Kiesow <lkiesow@uos.de> - 0.24.0-2
- Update to 0.24.0

* Sat Dec 03 2022 Lars Kiesow <lkiesow@uos.de> - 0.23.0-2
- Update to 0.23.0

* Wed Aug 03 2022 Lars Kiesow <lkiesow@uos.de> - 0.22.0-2
- Update to 0.22.0

* Fri Jun 24 2022 Lars Kiesow <lkiesow@uos.de> - 0.21.1-2
- Update to 0.21.1

* Tue May 31 2022 Lars Kiesow <lkiesow@uos.de> - 0.21.0-2
- Update to 0.21.0

* Thu Mar 17 2022 Lars Kiesow <lkiesow@uos.de> - 0.20.0-2
- Update to 0.20.0

* Thu Jun 24 2021 Lars Kiesow <lkiesow@uos.de> - 0.19.0-2
- Fixed port

* Tue May 11 2021 Lars Kiesow <lkiesow@uos.de> - 0.19.0-1
- Update to 0.19.0

* Sat Oct 24 2020 Lars Kiesow <lkiesow@uos.de> - 1.0.1-1
- Initial build
