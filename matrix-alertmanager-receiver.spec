%define debug_package %{nil}

%define  uid   matrixalert

Name:          matrix-alertmanager-receiver
Summary:       Send Alertmanager alerts to Matrix rooms
Version:       2025.5.21
Release:       1%{?dist}
License:       GPL-3+

Source0:       https://github.com/metio/%{name}/releases/download/%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/%{name}.service
Source2:       https://raw.githubusercontent.com/metio/%{name}/%{version}/config.sample.yaml
Source3:       https://raw.githubusercontent.com/metio/%{name}/%{version}/LICENSE
URL:           https://github.com/metio/matrix-alertmanager-receiver
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
Alertmanager client that forwards alerts to a Matrix room.


%prep
%setup -c

%build

%install
rm -rf %{buildroot}

# install binary
# binary name is s.th. like matrix-alertmanager-receiver_v2024.7.3
install -p -D -m 0755 %{name}_v%{version} %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service

# install configuration file
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/%{name}.yml

# license
cp %{SOURCE3} .

%clean
rm -rf %{buildroot}


%pre
# Create user if nonexistent
if [ ! $(getent passwd %{uid}) ]; then
	useradd --system %{uid} > /dev/null 2>&1 || :
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
%config(noreplace) %{_sysconfdir}/%{name}.yml
%{_unitdir}/%{name}.service
%license LICENSE


%changelog
* Thu May 22 2025 Lars Kiesow <lkiesow@uos.de> - 2025.5.21-1
- Update to 2025.5.21

* Thu Apr 24 2025 Lars Kiesow <lkiesow@uos.de> - 2025.4.23-1
- Update to 2025.4.23

* Thu Apr 17 2025 Lars Kiesow <lkiesow@uos.de> - 2025.4.16-1
- Update to 2025.4.16

* Thu Mar 27 2025 Lars Kiesow <lkiesow@uos.de> - 2025.3.26-1
- Update to 2025.3.26

* Thu Mar 20 2025 Lars Kiesow <lkiesow@uos.de> - 2025.3.19-1
- Update to 2025.3.19

* Thu Mar 13 2025 Lars Kiesow <lkiesow@uos.de> - 2025.3.12-1
- Update to 2025.3.12

* Thu Mar 06 2025 Lars Kiesow <lkiesow@uos.de> - 2025.3.5-1
- Update to 2025.3.5

* Thu Feb 27 2025 Lars Kiesow <lkiesow@uos.de> - 2025.2.26-1
- Update to 2025.2.26

* Thu Feb 20 2025 Lars Kiesow <lkiesow@uos.de> - 2025.2.19-1
- Update to 2025.2.19

* Thu Feb 13 2025 Lars Kiesow <lkiesow@uos.de> - 2025.2.12-1
- Update to 2025.2.12

* Mon Feb 10 2025 Lars Kiesow <lkiesow@uos.de> - 2025.2.9-1
- Update to 2025.2.9

* Thu Dec 19 2024 Lars Kiesow <lkiesow@uos.de> - 2024.12.18-1
- Update to 2024.12.18

* Thu Dec 12 2024 Lars Kiesow <lkiesow@uos.de> - 2024.12.11-1
- Update to 2024.12.11

* Thu Nov 28 2024 Lars Kiesow <lkiesow@uos.de> - 2024.11.27-1
- Update to 2024.11.27

* Thu Nov 21 2024 Lars Kiesow <lkiesow@uos.de> - 2024.11.20-1
- Update to 2024.11.20

* Thu Oct 31 2024 Lars Kiesow <lkiesow@uos.de> - 2024.10.30-1
- Update to 2024.10.30

* Thu Oct 24 2024 Lars Kiesow <lkiesow@uos.de> - 2024.10.23-1
- Update to 2024.10.23

* Thu Oct 17 2024 Lars Kiesow <lkiesow@uos.de> - 2024.10.16-1
- Update to 2024.10.16

* Thu Oct 03 2024 Lars Kiesow <lkiesow@uos.de> - 2024.10.2-1
- Update to 2024.10.2

* Thu Sep 19 2024 Lars Kiesow <lkiesow@uos.de> - 2024.9.18-1
- Update to 2024.9.18

* Thu Sep 12 2024 Lars Kiesow <lkiesow@uos.de> - 2024.9.11-1
- Update to 2024.9.11

* Thu Sep 05 2024 Lars Kiesow <lkiesow@uos.de> - 2024.9.4-1
- Update to 2024.9.4

* Thu Aug 29 2024 Lars Kiesow <lkiesow@uos.de> - 2024.8.28-1
- Update to 2024.8.28

* Thu Aug 22 2024 Lars Kiesow <lkiesow@uos.de> - 2024.8.21-1
- Update to 2024.8.21

* Fri Aug  2 2024 Lars Kiesow <lkiesow@uos.de> - 2024.7.3-1
- Initial build
