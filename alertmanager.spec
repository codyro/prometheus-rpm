%define debug_package %{nil}

%define  uid   alertmanager
%define  gid   alertmanager
%define  nuid  7972
%define  ngid  7972

Name:          alertmanager
Summary:       Prometheus Alertmanager
Version:       0.28.1
Release:       4%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/alertmanager/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
The Alertmanager handles alerts sent by client applications such as the
Prometheus server. It takes care of deduplicating, grouping, and routing them
to the correct receiver integrations such as email, PagerDuty, or OpsGenie. It
also takes care of silencing and inhibition of alerts.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# install binary
install -p -D -m 0755 alertmanager %{buildroot}%{_bindir}/alertmanager
install -p -D -m 0755 amtool %{buildroot}%{_bindir}/amtool

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
   alertmanager.yml \
   %{buildroot}%{_sysconfdir}/%{name}/alertmanager.yml

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
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/%{name}
%license LICENSE
%doc NOTICE


%changelog
* Sat Mar 08 2025 Lars Kiesow <lkiesow@uos.de> - 0.28.1-4
- Update to 0.28.1

* Thu Jan 16 2025 Lars Kiesow <lkiesow@uos.de> - 0.28.0-4
- Update to 0.28.0

* Thu Feb 29 2024 Lars Kiesow <lkiesow@uos.de> - 0.27.0-4
- Update to 0.27.0

* Fri Aug 25 2023 Lars Kiesow <lkiesow@uos.de> - 0.26.0-4
- Update to 0.26.0

* Sat Dec 24 2022 Lars Kiesow <lkiesow@uos.de> - 0.25.0-4
- Update to 0.25.0

* Sat Mar 26 2022 Lars Kiesow <lkiesow@uos.de> - 0.24.0-4
- Update to 0.24.0

* Thu Aug 26 2021 Lars Kiesow <lkiesow@uos.de> - 0.23.0-4
- Update to 0.23.0

* Thu Jun 03 2021 Lars Kiesow <lkiesow@uos.de> - 0.22.2-4
- Update to 0.22.2

* Fri May 28 2021 Lars Kiesow <lkiesow@uos.de> - 0.22.1-4
- Update to 0.22.1

* Tue May 25 2021 Lars Kiesow <lkiesow@uos.de> - 0.22.0-4
- Update to 0.22.0

* Sun Nov 01 2020 Lars Kiesow <lkiesow@uos.de> - 0.21.0-4
- Allow setting additional parameters

* Thu Oct 29 2020 Lars Kiesow <lkiesow@uos.de> - 0.21.0-3
- Fixed source references

* Thu Oct 29 2020 Lars Kiesow <lkiesow@uos.de> - 0.21.0-2
- Fixed service file

* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 0.21.0-1
- Initial build
