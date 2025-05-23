%define debug_package %{nil}

%define  uid   nginxexporter
%define  gid   nginxexporter

Name:          nginx-prometheus-exporter
Summary:       NGINX Prometheus Exporter
Version:       
Release:       3%{?dist}
License:       ASL 2.0

Source0:       https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v%{version}/nginx-prometheus-exporter_%{version}_linux_amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/nginx-prometheus-exporter.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/nginx-prometheus-exporter.env
Source3:       https://raw.githubusercontent.com/nginxinc/nginx-prometheus-exporter/v%{version}/LICENSE
URL:           https://github.com/nginxinc/nginx-prometheus-exporter
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
NGINX Prometheus exporter makes it possible to monitor NGINX or NGINX Plus
using Prometheus.


%prep
%setup -c

%build

%install
rm -rf %{buildroot}

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

# license
cp %{SOURCE3} .

%clean
rm -rf %{buildroot}


%pre
# Create user and group if nonexistent
if [ ! $(getent passwd %{uid}) ]; then
   useradd -M -r -g %{gid} %{uid} > /dev/null 2>&1 || :
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
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%license LICENSE


%changelog
* Thu Jan 09 2025 Lars Kiesow <lkiesow@uos.de> - -3
- Update to 

* Sun Jan 05 2025 Lars Kiesow <lkiesow@uos.de> - 1.4.0-3
- Fix release filename

* Thu Dec 05 2024 Lars Kiesow <lkiesow@uos.de> - 1.4.0-2
- Update to 1.4.0

* Sat Aug 03 2024 Lars Kiesow <lkiesow@uos.de> - 1.3.0-2
- Update to 1.3.0

* Sun Mar 14 2021 Lars Kiesow <lkiesow@uos.de> - 0.8.0-2
- Fixed service file and configuration

* Sun Mar 14 2021 Lars Kiesow <lkiesow@uos.de> - 0.8.0-1
- Initial build
