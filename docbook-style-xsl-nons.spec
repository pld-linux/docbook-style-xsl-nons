Summary:	DocBook XSL NONS (non-namespaced) Stylesheets
Summary(pl.UTF-8):	Arkusze stylów XSL NONS (bez przestrzeni nazw) dla DocBooka
Name:		docbook-style-xsl-nons
Version:	1.79.2
Release:	2
License:	MIT-like
Group:		Applications/Publishing/XML
#Source0Download: https://github.com/docbook/xslt10-stylesheets/releases
Source0:	https://github.com/docbook/xslt10-stylesheets/releases/download/release/%{version}/docbook-xsl-nons-%{version}.tar.bz2
# Source0-md5:	2666d1488d6ced1551d15f31d7ed8c38
# https://anonscm.debian.org/cgit/collab-maint/docbook-xsl.git/plain/debian/patches/765567_non-recursive_string_subst.patch
Patch0:		docbook-style-xsl-non-recursive-string-subst.patch
URL:		https://github.com/docbook/xslt10-stylesheets
BuildRequires:	libxml2-progs
BuildRequires:	unzip
AutoReqProv:	no
Requires(post,postun):	/etc/xml/catalog
Requires(post,postun):	/usr/bin/xmlcatalog
# workaround for rpm/poldek
Requires:	/etc/xml/catalog
Requires:	libxml2-progs
Requires:	sgml-common >= 0.5
Conflicts:	docbook-style-xsl < 1.79.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		xsl_path	%{_datadir}/sgml/docbook/xsl-nons-stylesheets
%define		catalog		%{xsl_path}/catalog.xml

%description
This package contains a release of XSL stylesheets for processing
non-namespaced DocBook documents (DocBook 5 or later). The stylesheets
are the same as the concurrent stylesheet release except that the
templates match on elements without the DocBook namespace.

%description -l pl.UTF-8
Ten pakiet zawiera wydanie arkuszy stylów XSL do przetwarzania
dokumentów DocBooka bez przestrzeni nazw (DocBook 5 lub późniejszy).
Arkusze są takie same jak zwykłe wydanie z tą różnicą, że szablony są
dopasowywane po elementach bez przestrzeni nazw DocBooka.

%prep
%setup -q -n docbook-xsl-nons-%{version}
%patch0 -p2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{xsl_path}

cp -a $(find . -mindepth 1 -maxdepth 1 -type d -a ! -name extensions) $RPM_BUILD_ROOT%{xsl_path}
cp -p VERSION.xsl $RPM_BUILD_ROOT%{xsl_path}

%xmlcat_create $RPM_BUILD_ROOT%{catalog}

%xmlcat_add_rewrite http://cdn.docbook.org/release/xsl-nons/%{version} file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}
%xmlcat_add_rewrite http://cdn.docbook.org/release/xsl-nons/current file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}
# backward compat
%xmlcat_add_rewrite http://docbook.sourceforge.net/release/xsl/%{version} file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}
%xmlcat_add_rewrite http://docbook.sourceforge.net/release/xsl/current file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q %{catalog} %{_sysconfdir}/xml/catalog ; then
	%xmlcat_add %{catalog}
fi

%preun
if [ "$1" = "0" ] ; then
	%xmlcat_del %{catalog}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING NEWS README RELEASE-NOTES.{html,txt} TODO
%{xsl_path}
