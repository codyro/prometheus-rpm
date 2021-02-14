%define debug_package %{nil}

%define  uid   nodeexporter
%define  gid   nodeexporter
%define  nuid  7971
%define  ngid  7971

Name:          node_exporter
Summary:       Node exporter for Prometheus
Version:       1.1.1
Release:       2%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/node_exporter.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/node_exporter.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels,
written in Go with pluggable metric collectors.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

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
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%license LICENSE
%doc NOTICE


%changelog
* Sun Feb 14 2021 Lars Kiesow <lkiesow@uos.de> - 1.1.1-2
- Update to 1.1.1

* Sun Feb 07 2021 Lars Kiesow <lkiesow@uos.de> - 1.1.0-2
- Update to 1.1.0

* Sun Nov 01 2020 Lars Kiesow <lkiesow@uos.de> - 1.0.1-2
- Allow specifying command line arguments

* Sat Oct 24 2020 Lars Kiesow <lkiesow@uos.de> - 1.0.1-1
- Initial build
