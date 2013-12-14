#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	gtk		# disable GTK at all
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x
%bcond_without	ldap		# without Evolution Data Sources LDAP backend
%bcond_without	static_libs	# don't build static libraries

Summary:	MateConf configuration database system
Summary(pl.UTF-8):	MateConf - system bazy danych konfiguracji
Name:		mate-conf
Version:	1.4.0
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	a4b4de4a6d6753f58e9f5f98ee73d18b
URL:		http://wiki.mate-desktop.org/mate-conf
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.9.5
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	rpmbuild(macros) >= 1.527
%if %{with gtk}
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.14.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
%endif
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-corba-devel
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
%if %{with gtk}
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.14.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MateConf is a configuration database system, functionally similar to
the Windows registry but lots better. :-) It's being written for the
MATE desktop but does not require MATE.

%description -l pl.UTF-8
MateConf to system bazy danych konfiguracji, funkcjonalnie podobny do
rejestru Windows, ale o wiele lepszy :-). Jest tworzony dla środowiska
graficznego MATE, ale nie wymaga MATE.

%package libs
Summary:	Shared MateConf library
Summary(pl.UTF-8):	Biblioteka współdzielona MateConf
Group:		Libraries
Requires:	glib2 >= 1:2.26.0

%description libs
Shared MateConf library.

%description libs -l pl.UTF-8
Biblioteka współdzielona MateConf.

%package devel
Summary:	Header files for MateConf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MateConf
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
Requires:	mate-corba-devel

%description devel
Header files for MateConf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MateConf.

%package static
Summary:	Static MateConf library
Summary(pl.UTF-8):	Statyczna biblioteka MateConf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MateConf library.

%description static -l pl.UTF-8
Statyczna biblioteka MateConf.

%package apidocs
Summary:	MateConf API documentation
Summary(pl.UTF-8):	Dokumentacja API MateConf
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
MateConf API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API MateConf.

%package backend-evoldap
Summary:	Evolution Data Sources LDAP backend for MetaConf
Summary(pl.UTF-8):	Backend LDAP źródeł danych Evolution dla MetaConfa
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description backend-evoldap
This is a special-purpose backend for MetaConf which enables default
mail accounts, addressbooks and calendars for Evolution to be
configured using each user's LDAP entry. By setting each user's mail
address, incoming/outgoing mail server addresses and
addressbook/calendar addresses in the user's LDAP entry, Evolution
will be automatically configured to use these addresses.

%description backend-evoldap -l pl.UTF-8
To jest backend MateConfa specjalnego przeznaczenia, pozwalający na
konfigurowanie domyślnych kont pocztowych, książek adresowych i
kalendarzy dla Evolution przy użyciu wpisu LDAP dla każdego
użytkownika. Poprzez ustawienie każdemu użytkownikowi adres pocztowy,
adresy serwerów poczty przychodzącej/wychodzącej oraz adresy książki
adresowej i kalendarza w jego wpisie LDAP, Evolution zostanie
automatycznie skonfigurowane do używania tych adresów.

%prep
%setup -q

%build
%{__intltoolize}
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-defaults-service \
	--enable-gsettings-backend=yes \
	%{?with_gtk:--enable-gtk %{?with_gtk3:--with-gtk=3.0}} \
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}} \
	--enable-introspection \
	%{__with_without ldap openldap} \
	%{__disable static_libs static} \
	%{nil}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/MateConf/2/lib*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gio/modules/lib*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/MateConf/2/lib*.a
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/lib*.a
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmateconf-2.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules || :

%postun
umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules || :

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mateconf-gsettings-data-convert
%attr(755,root,root) %{_bindir}/mateconf-gsettings-schema-convert
%attr(755,root,root) %{_bindir}/mateconf-merge-tree
%attr(755,root,root) %{_bindir}/mateconftool-2
%attr(755,root,root) %{_libdir}/mateconf-defaults-mechanism
%attr(755,root,root) %{_libdir}/mateconf-sanity-check-2
%attr(755,root,root) %{_libdir}/mateconfd-2
%attr(755,root,root) %{_libdir}/gio/modules/libgsettingsmateconfbackend.so
%dir %{_libdir}/MateConf
%dir %{_libdir}/MateConf/2
%attr(755,root,root) %{_libdir}/MateConf/2/libmateconfbackend-oldxml.so
%attr(755,root,root) %{_libdir}/MateConf/2/libmateconfbackend-xml.so
/etc/dbus-1/system.d/org.mate.MateConf.Defaults.conf
%dir %{_sysconfdir}/mateconf
%dir %{_sysconfdir}/mateconf/2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mateconf/2/path
%dir %{_sysconfdir}/mateconf/mateconf.xml.defaults
%dir %{_sysconfdir}/mateconf/mateconf.xml.mandatory
%dir %{_sysconfdir}/mateconf/mateconf.xml.system
%{_sysconfdir}/xdg/autostart/mateconf-gsettings-data-convert.desktop
%{_datadir}/dbus-1/services/org.mate.MateConf.service
%{_datadir}/dbus-1/system-services/org.mate.MateConf.Defaults.service
%{_datadir}/polkit-1/actions/org.mate.mateconf.defaults.policy
%{_datadir}/sgml/mateconf
%{_mandir}/man1/mateconf-gsettings-data-convert.1*
%{_mandir}/man1/mateconf-gsettings-schema-convert.1*
%{_mandir}/man1/mateconftool-2.1*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmateconf-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmateconf-2.so.4
%{_libdir}/girepository-1.0/MateConf-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmateconf-2.so
%{_includedir}/mateconf
%{_datadir}/gir-1.0/MateConf-2.0.gir
%{_pkgconfigdir}/mateconf-2.0.pc
%{_aclocaldir}/mateconf-2.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmateconf-2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mateconf
%endif

%if %{with ldap}
%files backend-evoldap
%defattr(644,root,root,755)
%doc backends/README.evoldap
%attr(755,root,root) %{_libdir}/MateConf/2/libmateconfbackend-evoldap.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mateconf/2/evoldap.conf
%dir %{_datadir}/MateConf
%dir %{_datadir}/MateConf/schema
%{_datadir}/MateConf/schema/evoldap.schema
%endif
