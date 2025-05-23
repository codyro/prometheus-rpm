%define debug_package %{nil}

%define  uid   prometheus
%define  gid   prometheus

Name:          prometheus
Summary:       Prometheus systems monitoring and alerting toolkit
Version:       3.4.0
Release:       4%{?dist}
License:       ASL 2.0

Source0:       https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.service
Source2:       https://raw.githubusercontent.com/lkiesow/prometheus-rpm/master/prometheus.env
URL:           https://prometheus.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
An open-source monitoring system with a dimensional data model, flexible query
language, efficient time series database and modern alerting approach.


%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# install binary
install -p -D -m 0755 prometheus %{buildroot}%{_bindir}/prometheus
install -p -D -m 0755 promtool %{buildroot}%{_bindir}/promtool

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
   prometheus.yml \
   %{buildroot}%{_sysconfdir}/%{name}/prometheus.yml

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
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/%{name}
%license LICENSE
%doc NOTICE


%changelog
* Sun May 18 2025 Lars Kiesow <lkiesow@uos.de> - 3.4.0-4
- Update to 3.4.0

* Sat May 03 2025 Lars Kiesow <lkiesow@uos.de> - 3.3.1-4
- Update to 3.3.1

* Sat Apr 19 2025 Lars Kiesow <lkiesow@uos.de> - 3.3.0-4
- Update to 3.3.0

* Wed Mar 19 2025 Lars Kiesow <lkiesow@uos.de> - 2.53.4-4
- Update to 2.53.4

* Thu Feb 27 2025 Lars Kiesow <lkiesow@uos.de> - 3.2.1-4
- Update to 3.2.1

* Tue Feb 18 2025 Lars Kiesow <lkiesow@uos.de> - 3.2.0-4
- Update to 3.2.0

* Sun Jan 05 2025 Lars Kiesow <lkiesow@uos.de> - 3.1.0-4
- Fix build (console files no longer exist)

* Fri Jan 03 2025 Lars Kiesow <lkiesow@uos.de> - 3.1.0-3
- Update to 3.1.0

* Fri Nov 29 2024 Lars Kiesow <lkiesow@uos.de> - 3.0.1-3
- Update to 3.0.1

* Fri Nov 15 2024 Lars Kiesow <lkiesow@uos.de> - 3.0.0-3
- Update to 3.0.0

* Thu Nov 07 2024 Lars Kiesow <lkiesow@uos.de> - 2.55.1-3
- Update to 2.55.1

* Wed Nov 06 2024 Lars Kiesow <lkiesow@uos.de> - 2.53.3-3
- Update to 2.53.3

* Wed Oct 23 2024 Lars Kiesow <lkiesow@uos.de> - 2.55.0-3
- Update to 2.55.0

* Wed Aug 28 2024 Lars Kiesow <lkiesow@uos.de> - 2.54.1-3
- Update to 2.54.1

* Sat Aug 10 2024 Lars Kiesow <lkiesow@uos.de> - 2.54.0-3
- Update to 2.54.0

* Thu Jul 11 2024 Lars Kiesow <lkiesow@uos.de> - 2.53.1-3
- Update to 2.53.1

* Sat Jun 22 2024 Lars Kiesow <lkiesow@uos.de> - 2.45.6-3
- Update to 2.45.6

* Thu Jun 20 2024 Lars Kiesow <lkiesow@uos.de> - 2.53.0-3
- Update to 2.53.0

* Thu May 09 2024 Lars Kiesow <lkiesow@uos.de> - 2.52.0-3
- Update to 2.52.0

* Fri May 03 2024 Lars Kiesow <lkiesow@uos.de> - 2.45.5-3
- Update to 2.45.5

* Tue Apr 16 2024 Lars Kiesow <lkiesow@uos.de> - 2.51.2-3
- Update to 2.51.2

* Fri Mar 29 2024 Lars Kiesow <lkiesow@uos.de> - 2.51.1-3
- Update to 2.51.1

* Thu Mar 21 2024 Lars Kiesow <lkiesow@uos.de> - 2.51.0%2Bdedupelabels-3
- Update to 2.51.0%2Bdedupelabels

* Wed Mar 20 2024 Lars Kiesow <lkiesow@uos.de> - 2.51.0-3
- Update to 2.51.0

* Tue Mar 19 2024 Lars Kiesow <lkiesow@uos.de> - 2.45.4-3
- Update to 2.45.4

* Tue Feb 27 2024 Lars Kiesow <lkiesow@uos.de> - 2.50.1-3
- Update to 2.50.1

* Fri Feb 23 2024 Lars Kiesow <lkiesow@uos.de> - 2.50.0-3
- Update to 2.50.0

* Thu Jan 25 2024 Lars Kiesow <lkiesow@uos.de> - 2.45.3-3
- Update to 2.45.3

* Tue Jan 16 2024 Lars Kiesow <lkiesow@uos.de> - 2.49.1-3
- Update to 2.49.1

* Wed Dec 20 2023 Lars Kiesow <lkiesow@uos.de> - 2.45.2-3
- Update to 2.45.2

* Sun Dec 10 2023 Lars Kiesow <lkiesow@uos.de> - 2.48.1-3
- Update to 2.48.1

* Fri Nov 17 2023 Lars Kiesow <lkiesow@uos.de> - 2.48.0-3
- Update to 2.48.0

* Mon Oct 16 2023 Lars Kiesow <lkiesow@uos.de> - 2.47.2-3
- Update to 2.47.2

* Thu Oct 05 2023 Lars Kiesow <lkiesow@uos.de> - 2.47.1-3
- Update to 2.47.1

* Sun Oct 01 2023 Lars Kiesow <lkiesow@uos.de> - 2.45.1-3
- Update to 2.45.1

* Thu Sep 07 2023 Lars Kiesow <lkiesow@uos.de> - 2.47.0-3
- Update to 2.47.0

* Sun Jul 30 2023 Lars Kiesow <lkiesow@uos.de> - 2.37.9-3
- Update to 2.37.9

* Wed Jul 26 2023 Lars Kiesow <lkiesow@uos.de> - 2.46.0-3
- Update to 2.46.0

* Sat Jun 24 2023 Lars Kiesow <lkiesow@uos.de> - 2.45.0-3
- Update to 2.45.0

* Wed May 31 2023 Lars Kiesow <lkiesow@uos.de> - 2.44.0-3
- Update to 2.44.0

* Tue May 30 2023 Lars Kiesow <lkiesow@uos.de> - 2.37.8-3
- Update to 2.37.8

* Mon May 15 2023 Lars Kiesow <lkiesow@uos.de> - 2.44.0-3
- Update to 2.44.0

* Sat May 06 2023 Lars Kiesow <lkiesow@uos.de> - 2.37.8-3
- Update to 2.37.8

* Fri Apr 28 2023 Lars Kiesow <lkiesow@uos.de> - 2.37.7-3
- Update to 2.37.7

* Wed Mar 22 2023 Lars Kiesow <lkiesow@uos.de> - 2.43.0%2Bstringlabels-3
- Update to 2.43.0%2Bstringlabels

* Tue Feb 21 2023 Lars Kiesow <lkiesow@uos.de> - 2.37.6-3
- Update to 2.37.6

* Thu Feb 02 2023 Lars Kiesow <lkiesow@uos.de> - 2.42.0-3
- Update to 2.42.0

* Wed Dec 21 2022 Lars Kiesow <lkiesow@uos.de> - 2.41.0-3
- Update to 2.41.0

* Thu Dec 15 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.7-3
- Update to 2.40.7

* Sat Dec 10 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.6-3
- Update to 2.40.6

* Fri Dec 02 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.5-3
- Update to 2.40.5

* Wed Nov 30 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.4-3
- Update to 2.40.4

* Fri Nov 25 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.3-3
- Update to 2.40.3

* Thu Nov 24 2022 Lars Kiesow <lkiesow@uos.de> - 2.37.3-3
- Update to 2.37.3

* Fri Nov 18 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.2-3
- Update to 2.40.2

* Thu Nov 10 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.1-3
- Update to 2.40.1

* Wed Nov 09 2022 Lars Kiesow <lkiesow@uos.de> - 2.40.0-3
- Update to 2.40.0

* Sat Nov 05 2022 Lars Kiesow <lkiesow@uos.de> - 2.37.2-3
- Update to 2.37.2

* Sat Oct 08 2022 Lars Kiesow <lkiesow@uos.de> - 2.39.1-3
- Update to 2.39.1

* Thu Oct 06 2022 Lars Kiesow <lkiesow@uos.de> - 2.39.0-3
- Update to 2.39.0

* Tue Sep 13 2022 Lars Kiesow <lkiesow@uos.de> - 2.37.1-3
- Update to 2.37.1

* Wed Aug 17 2022 Lars Kiesow <lkiesow@uos.de> - 2.38.0-3
- Update to 2.38.0

* Fri Jul 15 2022 Lars Kiesow <lkiesow@uos.de> - 2.37.0-3
- Update to 2.37.0

* Tue Jun 21 2022 Lars Kiesow <lkiesow@uos.de> - 2.36.2-3
- Update to 2.36.2

* Fri Jun 10 2022 Lars Kiesow <lkiesow@uos.de> - 2.36.1-3
- Update to 2.36.1

* Tue May 31 2022 Lars Kiesow <lkiesow@uos.de> - 2.36.0-3
- Update to 2.36.0

* Thu May 12 2022 Lars Kiesow <lkiesow@uos.de> - 2.35.0-3
- Update to 2.35.0

* Wed May 11 2022 Lars Kiesow <lkiesow@uos.de> - 2.34.0-3
- Update to 2.34.0

* Fri Apr 22 2022 Lars Kiesow <lkiesow@uos.de> - 2.35.0-3
- Update to 2.35.0

* Wed Mar 16 2022 Lars Kiesow <lkiesow@uos.de> - 2.34.0-3
- Update to 2.34.0

* Wed Mar 09 2022 Lars Kiesow <lkiesow@uos.de> - 2.33.5-3
- Update to 2.33.5

* Wed Feb 23 2022 Lars Kiesow <lkiesow@uos.de> - 2.33.4-3
- Update to 2.33.4

* Sat Feb 12 2022 Lars Kiesow <lkiesow@uos.de> - 2.33.3-3
- Update to 2.33.3

* Thu Feb 03 2022 Lars Kiesow <lkiesow@uos.de> - 2.33.1-3
- Update to 2.33.1

* Sun Jan 30 2022 Lars Kiesow <lkiesow@uos.de> - 2.33.0-3
- Update to 2.33.0

* Sun Dec 19 2021 Lars Kiesow <lkiesow@uos.de> - 2.32.1-3
- Update to 2.32.1

* Wed Dec 15 2021 Lars Kiesow <lkiesow@uos.de> - 2.32.0-3
- Update to 2.32.0

* Sat Nov 06 2021 Lars Kiesow <lkiesow@uos.de> - 2.31.1-3
- Update to 2.31.1

* Wed Nov 03 2021 Lars Kiesow <lkiesow@uos.de> - 2.31.0-3
- Update to 2.31.0

* Thu Oct 07 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.3-3
- Update to 2.30.3

* Sat Oct 02 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.2-3
- Update to 2.30.2

* Wed Sep 29 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.1-3
- Update to 2.30.1

* Wed Sep 15 2021 Lars Kiesow <lkiesow@uos.de> - 2.30.0-3
- Update to 2.30.0

* Sat Aug 28 2021 Lars Kiesow <lkiesow@uos.de> - 2.29.2-3
- Update to 2.29.2

* Thu Aug 12 2021 Lars Kiesow <lkiesow@uos.de> - 2.29.1-3
- Update to 2.29.1

* Fri Jul 02 2021 Lars Kiesow <lkiesow@uos.de> - 2.28.1-3
- Update to 2.28.1

* Tue Jun 22 2021 Lars Kiesow <lkiesow@uos.de> - 2.28.0-3
- Update to 2.28.0

* Wed May 19 2021 Lars Kiesow <lkiesow@uos.de> - 2.27.1-3
- Update to 2.27.1

* Thu May 13 2021 Lars Kiesow <lkiesow@uos.de> - 2.27.0-3
- Update to 2.27.0

* Thu Apr 01 2021 Lars Kiesow <lkiesow@uos.de> - 2.26.0-3
- Update to 2.26.0

* Wed Mar 17 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.2-3
- Update to 2.25.2

* Mon Mar 15 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.1-3
- Update to 2.25.1

* Thu Feb 18 2021 Lars Kiesow <lkiesow@uos.de> - 2.25.0-3
- Update to 2.25.0

* Thu Jan 21 2021 Lars Kiesow <lkiesow@uos.de> - 2.24.1-3
- Update to 2.24.1

* Thu Jan 07 2021 Lars Kiesow <lkiesow@uos.de> - 2.24.0-3
- Update to 2.24.0

* Fri Nov 27 2020 Lars Kiesow <lkiesow@uos.de> - 2.23.0-3
- Update to 2.23.0

* Tue Nov 17 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.2-3
- Update to 2.22.2

* Fri Nov 06 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.1-3
- Update to 2.22.1

* Sun Nov 01 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-3
- Allow setting additional parameters

* Sun Oct 25 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-2
- Fix systemd actions

* Mon Oct 19 2020 Lars Kiesow <lkiesow@uos.de> - 2.22.0-1
- Update to 2.22.0

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-3
- By default, listen to 127.0.0.1 only

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-2
- Removed tsdb binary

* Mon Oct 12 2020 Lars Kiesow <lkiesow@uos.de> - 2.21.0-1
- Update to 2.21.0

* Tue May 26 2020 Lars Kiesow <lkiesow@uos.de> - 2.18.1-1
- Initial build
