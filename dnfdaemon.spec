%global dnf_org org.baseurl.Dnf
%global dnf_version 2.0.0

Name:           dnfdaemon
Version:        0.3.16
Release:        1%{?dist}
Summary:        DBus daemon for dnf package actions
License:        GPLv2+
URL:            https://github.com/timlau/dnf-daemon
Source0:        https://github.com/timlau/dnf-daemon/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  systemd
Requires:       python3-gobject
Requires:       python3-dbus
Requires:       python3-dnf >= %{dnf_version}
Requires:       polkit

%if 0%{?fedora} >= 23
Requires(post):     policycoreutils-python-utils
Requires(postun):   policycoreutils-python-utils
%else
Requires(post):     policycoreutils-python
Requires(postun):   policycoreutils-python
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Dbus daemon for performing package actions with the dnf package manager

%prep
%setup -q

%build
# Nothing to build

%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIR=%{_datadir} SYSCONFDIR=%{_sysconfdir}

%package -n python3-%{name}
Summary:        Python 3 api for communicating with the dnf-daemon DBus service
Group:          Applications/System
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
Requires:       python3-gobject

%description -n python3-%{name}
Python 3 api for communicating with the dnf-daemon DBus service

%package -n python-%{name}
Summary:        Python 2 api for communicating with the dnf-daemon DBus service
Group:          Applications/System
BuildRequires:  python2-devel
Requires:       %{name} = %{version}-%{release}
Requires:       pygobject3

%description -n python-%{name}
Python 2 api for communicating with the dnf-daemon DBus service

# apply the right selinux file context
# http://fedoraproject.org/wiki/PackagingDrafts/SELinux#File_contexts

%post
semanage fcontext -a -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
restorecon -R %{_datadir}/%{name}/%{name}-system || :
%systemd_post %{name}.service

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
fi
%systemd_postun %{name}.service

%preun
%systemd_preun %{name}.service

%files
%doc README.md ChangeLog COPYING
%{_datadir}/dbus-1/system-services/%{dnf_org}*
%{_datadir}/dbus-1/services/%{dnf_org}*
%{_datadir}/%{name}/
%{_unitdir}/%{name}.service
%{_datadir}/polkit-1/actions/%{dnf_org}*
# this should not be edited by the user, so no %%config
%{_sysconfdir}/dbus-1/system.d/%{dnf_org}*
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/__*
%{python3_sitelib}/%{name}/server


%files -n  python-%{name}
%{python_sitelib}/%{name}

%files -n  python3-%{name}
%{python3_sitelib}/%{name}/client

%changelog
* Wed May 25 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.16-1
- bumped release

* Tue May 10 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.15-1
- bumped release

* Fri Apr 29 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.14-1
- bumped release

* Fri Apr 29 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.13-1
- bumped release

* Tue Dec 01 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.12-2
- require dnf-1.1.0

* Sat Nov 28 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.12-1
- added systemd service

* Wed Nov 18 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.11-1
- bumped release

* Wed Sep 30 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.10-2
- updated req. policycoreutils-python to policycoreutils-python-utils

* Wed Sep 30 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.10-1
- bumped release

* Wed May 27 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.9-1
- bumped release

* Wed May 06 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.8-1
- bumped release

* Sun Apr 26 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.7-1
- bumped release

* Wed Apr 15 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.6-1
- bumped release

* Wed Apr 15 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.5-1
- bumped release

* Sun Apr 12 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.4-1
- bumped release
- require dnf-0.6.3

* Fri Oct 17 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.3-1
- bumped release

* Wed Oct 15 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-3
- removed require python3-dnfdaemon from main package

* Wed Oct 15 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-2
- include python3-dnfdaemon in the dnfdaemon main package
- renamed python?-dnfdaemon-client to python?-dnfdaemon
- include dir ownerships in the right packages

* Sun Oct 12 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-1
- bumped release
- fedora review cleanups
- python-dnfdaemon-client should own %%{python_sitelib}/dnfdaemon/client
- group %%files sections
- use uploaded sources on github, not autogenerated ones.

* Sun Sep 21 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.1-1
- updated ChangeLog (timlau@fedoraproject.org)

* Sun Sep 21 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.0-1
- bumped release

* Mon Sep 01 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.5-1
- updated ChangeLog (timlau@fedoraproject.org)
- Hack for GObjects dont blow up (timlau@fedoraproject.org)

* Mon Sep 01 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.4-1
- updated ChangeLog (timlau@fedoraproject.org)
- Use GLib mainloop, instead of Gtk, there is crashing in F21
  (timlau@fedoraproject.org)
- use the same cache setup as dnf cli (timlau@fedoraproject.org)
- fix cachedir setup caused by upstream changes (timlau@fedoraproject.org)
- fix: show only latest updates (fixes : timlau/yumex-dnf#2)
  (timlau@fedoraproject.org)
- fix: only get latest upgrades (timlau@fedoraproject.org)

* Sun Jul 13 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.3-1
- fix cachedir setup for dnf 0.5.3 bump dnf dnf requirement
  (timlau@fedoraproject.org)

* Thu May 29 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.2-1
- build: require dnf 0.5.2 (timlau@fedoraproject.org)
- fix refactor issue (timlau@fedoraproject.org)
- api: merged GetPackages with GetPackageWithAttributes.
  (timlau@fedoraproject.org)


