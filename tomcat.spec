Name: tomcat
Version: 7.0.23
Release: 1
Summary: Open source software implementation of the Java Servlet and JavaServer Pages technologies.
Group: Productivity/Networking/Web/Servers 
License: Apache Software License.
Url: http://tomcat.apache.org 
Source0: http://archive.apache.org/dist/tomcat/tomcat-7/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
Source1: http://archive.apache.org/dist/tomcat/tomcat-7/v%{version}/src/apache-tomcat-%{version}-src.tar.gz.md5
Source2: https://raw.github.com/lolaent/tapache-tomcat-rpm/master/tomcat-initscript

BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: ant
BuildRequires: ant-trax
Requires: java
BuildArch: x86_64


%define install_path /opt/tomcat

%description
Apache Tomcat is an open source software implementation of the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed under the Java Community Process.

%package manager
Summary: The management web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description manager
The management web application of Apache Tomcat.

%package ROOT
Summary: The ROOT web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description ROOT
The ROOT web application of Apache Tomcat.

%package docs
Summary: The docs web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description docs
The docs web application of Apache Tomcat.

%package examples
Summary: The examples web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description examples
The examples web application of Apache Tomcat.

%package host-manager
Summary: The host-manager web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description host-manager
The host-manager web application of Apache Tomcat.

%prep
cd %{_sourcedir}/
md5sum -c apache-tomcat-%{version}-src.tar.gz.md5 || (echo "Source archive failed m5sum check" && exit 1)
cd -

tar -zxf %{_sourcedir}/apache-tomcat-%{version}-src.tar.gz --transform s/apache-tomcat-%{version}/%{name}-%{version}/

cd %{name}-%{version}-src
#chown -R root.root .
chmod -R a+rX,g-w,o-w .

# This tells ant to install software in a specific directory.
cat << EOF >> build.properties
base.path=%{buildroot}%{install_path}
EOF

%build
cd %{_builddir}/%{name}-%{version}-src
ant

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{install_path}/pid
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/var/run/%{name}
cd %{_builddir}/%{name}-%{version}-src
ls -l
%{__cp} -Rip ./output/build/{bin,conf,lib,logs,temp,webapps} %{buildroot}%{install_path}
%{__cp} %{SOURCE2} %{buildroot}/etc/init.d/%{name}

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}

%pre
getent group tomcat > /dev/null || groupadd -r tomcat
getent passwd tomcat > /dev/null || useradd -r -g tomcat tomcat

%post
chkconfig --add %{name}

%preun
if [ "$1" = "0" ] ; then
 service %{name} stop > /dev/null 2>&1
 chkconfig --del %{name}
fi

%files
%defattr(640,tomcat,tomcat,750)
%dir %{install_path}
%config %{install_path}/conf/*
%{install_path}/bin
%{install_path}/lib
%{install_path}/logs
%{install_path}/temp
%{install_path}/pid
%dir %{install_path}/webapps
/var/run/%{name}
%attr(0750,tomcat,tomcat) %{install_path}/bin/*.sh
%attr(0755,root,root) /etc/init.d/%{name}

%files manager
%{install_path}/webapps/manager

%files ROOT
%{install_path}/webapps/ROOT

%files docs
%{install_path}/webapps/docs

%files examples
%{install_path}/webapps/examples

%files host-manager
%{install_path}/webapps/host-manager

%changelog
* Tue Jan 21 2014 - Sean Burlington <sean@practicalweb.co.uk> 70.0.23-1
 - backport to older version using archive URL
* Wed Feb 27 2013 - Trenton D. Adams <trenton.d.adams@gmail.com> 7.0.37-1
 - update to latest tomcat version
* Sat Jan 5 2013 - Trenton D. Adams <trenton.d.adams@gmail.com> 7.0.34-9
 - Initial github release
 - added md5sum checking
 - change a few file permissions
 - add Source0 and Source1 urls for the source package and md5 sum of said
   package.  "spectool -R -g apache-tomcat.spec" can retrieve required 
   source files.
* Mon Jul 4 2011 - robert (at) meinit.nl
- Initial release.
