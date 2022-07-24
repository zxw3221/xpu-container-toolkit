Name: xpu-container-toolkit
Version: %{version}
Release: %{release}
Group: Development Tools

Vendor: NVIDIA CORPORATION
Packager: NVIDIA CORPORATION <cudatools@nvidia.com>

Summary: NVIDIA container runtime hook
URL: https://github.com/zxw3221/xpu-container-runtime
License: Apache-2.0

Source0: xpu-container-toolkit
Source1: xpu-container-runtime
Source2: xpu-ctk
Source3: config.toml
Source4: oci-xpu-hook
Source5: oci-xpu-hook.json
Source6: LICENSE

Obsoletes: xpu-container-runtime <= 3.5.0-1, xpu-container-runtime-hook
Provides: xpu-container-runtime
Provides: xpu-container-runtime-hook
Requires: libxpu-container-tools >= %{libnvidia_container_tools_version}, libxpu-container-tools < 2.0.0

%if 0%{?suse_version}
Requires: libseccomp2
Requires: libapparmor1
%else
Requires: libseccomp
%endif

%description
Provides a OCI hook to enable GPU support in containers.

%prep
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} .

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 -t %{buildroot}%{_bindir} xpu-container-toolkit
install -m 755 -t %{buildroot}%{_bindir} xpu-container-runtime
install -m 755 -t %{buildroot}%{_bindir} xpu-ctk

mkdir -p %{buildroot}/etc/xpu-container-runtime
install -m 644 -t %{buildroot}/etc/xpu-container-runtime config.toml

mkdir -p %{buildroot}/usr/libexec/oci/hooks.d
install -m 755 -t %{buildroot}/usr/libexec/oci/hooks.d oci-xpu-hook

mkdir -p %{buildroot}/usr/share/containers/oci/hooks.d
install -m 644 -t %{buildroot}/usr/share/containers/oci/hooks.d oci-xpu-hook.json

%posttrans
ln -sf %{_bindir}/xpu-container-toolkit %{_bindir}/xpu-container-runtime-hook

%postun
rm -f %{_bindir}/xpu-container-runtime-hook

%files
%license LICENSE
%{_bindir}/xpu-container-toolkit
%{_bindir}/xpu-container-runtime
%{_bindir}/xpu-ctk
%config /etc/xpu-container-runtime/config.toml
/usr/libexec/oci/hooks.d/oci-xpu-hook
/usr/share/containers/oci/hooks.d/oci-xpu-hook.json

%changelog
# As of 1.10.0-1 we generate the release information automatically
* %{release_date} NVIDIA CORPORATION <cudatools@nvidia.com> %{version}-%{release}
- See https://gitlab.com/nvidia/container-toolkit/container-toolkit/-/blob/%{git_commit}/CHANGELOG.md
- Bump libxpu-container dependency to libxpu-container-tools >= %{libnvidia_container_tools_version}
