%define nuagekubemon_binary	nuagekubemon
%define nuagekubemon_datadir	/usr/share/%{nuagekubemon_binary}
%define nuagekubemon_yaml	nuagekubemon.yaml
%define nuagekubemon_yaml_path	%{nuagekubemon_datadir}/%{nuagekubemon_yaml}
%define nuagekubemon_logdir     /var/log/%{nuagekubemon_binary}

Name: nuagekubemon 
Version: 0.0
Release: 1%{?dist}
Summary: Nuage Kubernetes Monitor	
Group: System Environments/Daemons	
License: ALU EULA and ASL 2.0	
Source0: nuagekubemon-%{version}.tar.gz

BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

%prep
%setup -q

%build
godep go build
mv nuagekubemon-%{version} %{nuagekubemon_binary} 

%pre
if [ "$1" = "2" ]; then
	cp $RPM_BUILD_ROOT%{nuagekubemon_yaml_path} $RPM_BUILD_ROOT%{nuagekubemon_yaml_path}.orig
fi

%install
install --directory $RPM_BUILD_ROOT%{nuagekubemon_datadir}
install --directory $RPM_BUILD_ROOT%{nuagekubemon_logdir}
install --directory $RPM_BUILD_ROOT/usr/bin
install -m 755 %{nuagekubemon_binary} $RPM_BUILD_ROOT/usr/bin
install -m 644 %{nuagekubemon_yaml}.template  $RPM_BUILD_ROOT%{nuagekubemon_yaml_path}

%post
if [ "$1" = "2" ]; then
	cp $RPM_BUILD_ROOT%{nuagekubemon_yaml_path}.orig $RPM_BUILD_ROOT%{nuagekubemon_yaml_path}
fi

%postun
if [ "$1" = "0" ]; then
   rm -rf $RPM_BUILD_ROOT%{nuagekubemon_datadir}
   rm -rf $RPM_BUILD_ROOT%{nuagekubemon_logdir}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files

/usr/bin/%{nuagekubemon_binary}
%attr(755, root, nobody) %{nuagekubemon_logdir} 
%attr(755, root, nobody) %{nuagekubemon_datadir}
%attr(644, root, nobody) %{nuagekubemon_yaml_path} 
%doc

%changelog
