%define		_pver	030117
Summary:	msession daemon - pseudo-database memory cache
Summary(pl):	Demon msession - pseudo-bazodanowe cache
Name:		msession
Version:	030130
Release:	2
License:	GPL
Group:		Networking/Daemons
#Source0Download:	http://devel.mohawksoft.com/downloads.html
Source0:	http://devel.mohawksoft.com/%{name}-%{version}.tar.gz
#Source1Download:	http://devel.mohawksoft.com/downloads.html
Source1:	http://devel.mohawksoft.com/phoenix-%{_pver}.tar.gz
URL:		http://devel.mohawksoft.com/msession.html
BuildRequires:	gcc-c++
BuildRequires:	postgresql-devel
BuildRequires:	unixODBC-devel
Requires:	phoenix = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description
This is the msession daemon. It is a pseudo-database memory cache.
It is was originally designed for multiple web servers to share data.

%description -l pl
Ten pakiet zawiera demona msession. Udostêpnia on pseudo-bazodanowe
cache przechowywane w pamiêci. Oryginalnie by³ projektowany w celu
wspó³dzielenia danych przez wiele serwerów WWW.

%package pgsql
Summary:	PostgreSQL plugin for msession daemon
Summary(pl):	Wtyczka PostgreSQL do demona msession
Group:		Libraries
Requires:	%{name} = %{version}

%description pgsql
This is a PostgreSQL function-only plugin that implements
serialize and restore functionality for the flex plugin.

%description pgsql -l pl
To jest wtyczka funkcyjna PostgreSQL, implementuj±ca funkcjonalno¶æ
serialize/restore dla wtyczki flex.

%package -n phoenix
Summary:	phoenix - a library comprised of routines for various projects
Summary(pl):	phoenix - biblioteka ze zbiorem procedur dla ró¿nych projektów
License:	LGPL
Group:		Libraries
URL:		http://www.mohawksoft.com/devel/phoenix/

%description -n phoenix
This is phoenix, it is a library comprised of routines written for
various projects. There is no underlying purpose or string that binds
them together, it is just a collection of nifty routines.

%description -n phoenix -l pl
Ten pakiet zawiera phoenix - bibliotekê zawieraj±c± zbiór procedur
napisanych dla ró¿nych projektów.

%package -n phoenix-devel
Summary:	Header files for phoenix library
Summary(pl):	Pliki nag³ówkowe biblioteki phoenix
License:	LGPL
Group:		Development/Libraries
Requires:	phoenix = %{version}

%description -n phoenix-devel
Header files for phoenix library.

%description -n phoenix-devel -l pl
Pliki nag³ówkowe biblioteki phoenix.

%package -n phoenix-static
Summary:	Static phoenix library
Summary(pl):	Statyczna biblioteka phoenix
License:	LGPL
Group:		Development/Libraries
Requires:	phoenix-devel = %{version}

%description -n phoenix-static
Static version of phoenix library.

%description -n phoenix-static -l pl
Statyczna wersja biblioteki phoenix.

%prep
%setup -q -b1 -n phoenix

%build
mkdir lib
cd src
ln -sf Linux.mak config.mak

%{__make} \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags}"

%{__make} install
rm -f *.o

%{__make} phoenix.so \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags} -fPIC" \
	LINK_DLL="%{__cc} -shared -Wl -lm -lpthread" \

cd -

%{__make} -C msession \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_includedir}/phoenix}

install lib/libphoenix.* $RPM_BUILD_ROOT%{_libdir}
install src/phoenix.so $RPM_BUILD_ROOT%{_libdir}/libphoenix.so

install src/{[!bmpstu]*,m[!befi]*,memheap,metadef,mf[!as]*,session}.h \
    $RPM_BUILD_ROOT%{_includedir}/phoenix

install msession/msession{d,rc} $RPM_BUILD_ROOT%{_sbindir}
install msession/*.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n phoenix -p /sbin/ldconfig
%postun	-n phoenix -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc msession/plugin.cpp msession/{PLUGINS,README}
%attr(755,root,root) %{_sbindir}/msession*
%attr(755,root,root) %{_libdir}/[!ls]*.so

%files pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sql*.so

%files -n phoenix
%defattr(644,root,root,755)
%doc src/README
%attr(755,root,root) %{_libdir}/libphoenix.so

%files -n phoenix-devel
%defattr(644,root,root,755)
%{_includedir}/phoenix

%files -n phoenix-static
%defattr(644,root,root,755)
%{_libdir}/libphoenix.a
