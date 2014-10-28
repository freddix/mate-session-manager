Summary:	MATE session manager
Name:		mate-session-manager
Version:	1.8.1
Release:	3
License:	LGPL
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	b19b9e585f7343e34bff9b58c4f1d963
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	caja >= 1.8.0
Requires:	marco >= 1.8.0
Requires:	mate-desktop >= 1.8.0
Requires:	mate-panel >= 1.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE session manager and several other session management
related utilities.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--disable-upower	\
	--enable-ipv6		\
	--with-default-wm=marco
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,ha,ig,tk,ps}

%find_lang %{name}

%clean
rm -fr $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-*
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/mate-session-manager
%{_datadir}/xsessions/mate.desktop
%{_desktopdir}/mate*.desktop
%{_iconsdir}/hicolor/*/apps/*.*
%{_mandir}/man[15]/*

