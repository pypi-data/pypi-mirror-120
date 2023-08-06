# -- metadata ---------------

Name:      igwn-accounting
Version:   1.3.0
Release:   1%{?dist}

BuildArch: noarch
Group:     Development/Libraries
License:   ASL 2.0
Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Prefix:    %{_prefix}
Source0:   %pypi_source
Summary:   IGWN Computing accounting tools
Url:       https://accounting.ligo.org
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

# -- build requirements -----

# macros
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build
BuildRequires: python3 >= 3.5
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-setuptools >= 30.3.0
BuildRequires: python%{python3_pkgversion}-wheel

# testing
BuildRequires: python3-condor >= 8.8.0
BuildRequires: python%{python3_pkgversion}-dateutil
BuildRequires: python%{python3_pkgversion}-pytest

# man pages (only on rhel8 or later)
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-argparse-manpage
%endif

# -- packages ---------------

#%% package -n igwn-accounting
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
%description
IGWN Computing Accounting tools

%package -n python%{python3_pkgversion}-%{name}
Summary: %{summary}
Requires: python%{python3_pkgversion}-dateutil
Requires: python3-condor >= 8.8.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The Python %{python3_version} IGWN Accounting library.

# -- build ------------------

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel igwn_accounting-%{version}-*.whl

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
export PATH="%{buildroot}%{_bindir}:${PATH}"
# run test suite
%{__python3} -m pytest --pyargs igwn_accounting
# test entry point
igwn-accounting-report --help

%clean
rm -rf $RPM_BUILD_ROOT

# -- files ------------------

%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%files
%license LICENSE
%doc README.md
%{_bindir}/*
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
%{_mandir}/man1/*.1*
%endif

# -- changelog --------------

%changelog
* Mon Sep 20 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.0-1
- update for 1.3.0

* Thu Apr 15 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.1-2
- use wheels to install, gives better metadata
- add checks

* Thu Apr 01 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.1-1
- update for 1.2.1

* Tue Mar 30 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.0-1
- update for 1.2.0

* Thu Jan 28 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.0-1
- update for 1.1.0

* Tue Jan 19 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.0-1
- initial release
