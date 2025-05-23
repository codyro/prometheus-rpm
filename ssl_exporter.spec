%define debug_package %{nil}

%define  uid   sslexporter
%define  gid   sslexporter
%define  nuid  7973
%define  ngid  7973

Name:          ssl_exporter
Summary:       SSL Certificate Exporter
Version:       2.4.3
Release:       5%{?dist}
License:       ASL 2.0

Source0:       https://github.com/ribbybibby/ssl_exporter/releases/download/v%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.env
Source3:       https://raw.githubusercontent.com/ribbybibby/ssl_exporter/v%{version}/examples/%{name}.yaml
URL:           https://github.com/ribbybibby/ssl_exporter
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
Exports Prometheus metrics for SSL certificates


%prep
%setup -c

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
   %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

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
%doc README.md


%changelog
* Mon Apr 29 2024 Lars Kiesow <lkiesow@uos.de> - 2.4.3-5
- Update to 2.4.3

* Sat Jul 16 2022 Lars Kiesow <lkiesow@uos.de> - 2.4.2-5
- Update to 2.4.2

* Sun May 08 2022 Lars Kiesow <lkiesow@uos.de> - 2.4.1-5
- Update to 2.4.1

* Fri Dec 24 2021 Lars Kiesow <lkiesow@uos.de> - 2.4.0-5
- Update to 2.4.0

* Tue Aug 24 2021 Lars Kiesow <lkiesow@uos.de> - 2.3.1-5
- Update to 2.3.1

* Thu Jun 24 2021 Lars Kiesow <lkiesow@uos.de> - 2.2.1-5
- Update to 2.2.1

* Fri Feb 12 2021 Lars Kiesow <lkiesow@uos.de> - 2.2.0-5
- Update to 2.2.0

* Sun Nov 01 2020 Lars Kiesow <lkiesow@uos.de> - 2.1.1-5
- Better support configuring different arguments

* Mon Oct 26 2020 Lars Kiesow <lkiesow@uos.de> - 2.1.1-3
- Fix configuration

* Mon Oct 26 2020 Lars Kiesow <lkiesow@uos.de> - 2.1.1-2
- Uppded default configuration file

* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 2.1.1-1
- Initial build
