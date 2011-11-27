Name:           cal10n
Version:        0.7.4
Release:        7
Summary:        Compiler assisted localization library (CAL10N)

Group:          Development/Java
License:        MIT
URL:            http://cal10n.qos.ch
Source0:        http://cal10n.qos.ch/dist/cal10n-%{version}.tar.gz
Patch0:         %{name}-fix-maven.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: junit4
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: maven2
BuildRequires: maven-assembly-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit4

Requires:      java
Requires(post):   jpackage-utils >= 1.7.3
Requires(postun): jpackage-utils >= 1.7.3

%description
Compiler Assisted Localization, abbreviated as CAL10N (pronounced as "calion") 
is a java library for writing localized (internationalized) messages.
Features:
    * java compiler verifies message keys used in source code
    * tooling to detect errors in message keys
    * native2ascii tool made superfluous, as you can directly encode bundles 
      in the most convenient charset, per locale.
    * good performance (300 nanoseconds per key look-up)
    * automatic reloading of resource bundles upon change


%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%package -n maven-cal10n-plugin
Summary:    CAL10N maven plugin
Group:      Development/Java
Requires:   maven2
Requires:   %{name} = %{version}-%{release}

%description -n maven-cal10n-plugin
Maven plugin verifying that the codes defined in
an enum type match those in the corresponding resource bundles. 

%prep
%setup -q 
find . -name "*.jar" | xargs rm
%patch0

%build
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.test.failure.ignore=true \
        install javadoc:aggregate

%install

# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}
install -m 644 cal10n-api/target/cal10n-api-%{version}.jar \
        %{buildroot}%{_javadir}/%{name}/cal10n-api.jar
install -m 644 maven-cal10n-plugin/target/maven-cal10n-plugin-%{version}.jar \
        %{buildroot}%{_javadir}/%{name}/maven-cal10n-plugin.jar


%add_to_maven_depmap ch.qos.cal10n cal10n-parent %{version} JPP/%{name} cal10n-parent
%add_to_maven_depmap ch.qos.cal10n cal10n-api %{version} JPP/%{name} cal10n-api
%add_to_maven_depmap ch.qos.cal10n maven-cal10n-plugin %{version} JPP/%{name} maven-cal10n-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-parent.pom
install -pm 644 cal10n-api/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-api.pom
install -pm 644 maven-cal10n-plugin/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-cal10n-plugin.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug 646523
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%defattr(-,root,root,-)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}*.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-parent*
%{_mavenpomdir}/JPP.%{name}-%{name}-api*
%{_mavendepmapfragdir}/%{name}

%files -n maven-cal10n-plugin
%defattr(-,root,root,-)
%{_javadir}/%{name}/maven*.jar
%{_mavenpomdir}/JPP.%{name}-maven*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

