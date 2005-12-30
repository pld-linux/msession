%define		_pver	030117E
%define		ppfx	R1_2
Summary:	msession daemon - pseudo-database memory cache
Summary(pl):	Demon msession - pseudo-bazodanowe cache
Name:		msession
Version:	030130
Release:	3
Epoch:		1
License:	GPL
Group:		Networking/Daemons
#Source0Download:	http://devel.mohawksoft.com/downloads.html
Source0:	http://devel.mohawksoft.com/%{name}-%{version}.tar.gz
# Source0-md5:	68504332e95eca522f1aef59422b7e6c
#Source1Download:	http://devel.mohawksoft.com/downloads.html
Source1:	http://devel.mohawksoft.com/phoenix-%{ppfx}_%{_pver}.tar.gz
# Source1-md5:	098704fa107d5199f2ea1ac3371c0fc3
Patch0:		%{name}-plugindir.patch
Patch1:		%{name}-gcc4.patch
URL:		http://devel.mohawksoft.com/msession.html
BuildRequires:	libstdc++-devel
BuildRequires:	postgresql-devel
BuildRequires:	unixODBC-devel
Requires:	phoenix = %{epoch}:%{_pver}-%{release}
Obsoletes:	msession-pgsql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%define		specflags	-fno-strict-aliasing

%description
This is the msession daemon. It is a pseudo-database memory cache.
It is was originally designed for multiple web servers to share data.

%description -l pl
Ten pakiet zawiera demona msession. Udostêpnia on pseudo-bazodanowe
cache przechowywane w pamiêci. Oryginalnie by³ projektowany w celu
wspó³dzielenia danych przez wiele serwerów WWW.

%package -n phoenix
Summary:	phoenix - a library comprised of routines for various projects
Summary(pl):	phoenix - biblioteka ze zbiorem procedur dla ró¿nych projektów
Version:	%{_pver}
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
Version:	%{_pver}
License:	LGPL
Group:		Development/Libraries
Requires:	phoenix = %{epoch}:%{_pver}-%{release}

%description -n phoenix-devel
Header files for phoenix library.

%description -n phoenix-devel -l pl
Pliki nag³ówkowe biblioteki phoenix.

%package -n phoenix-static
Summary:	Static phoenix library
Summary(pl):	Statyczna biblioteka phoenix
Version:	%{_pver}
License:	LGPL
Group:		Development/Libraries
Requires:	phoenix-devel = %{epoch}:%{_pver}-%{release}

%description -n phoenix-static
Static version of phoenix library.

%description -n phoenix-static -l pl
Statyczna wersja biblioteki phoenix.

%prep
%setup -q -b1 -n phoenix
%patch0 -p1
%patch1 -p1

%build
[ ! -d lib ] && mkdir lib
cd src
ln -sf Linux.mak config.mak

%{__make} \
	GCC="%{__cxx} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcxxflags}"

%{__make} install
rm -f *.o

%{__make} phoenix.so \
	GCC="%{__cxx} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcxxflags} -fPIC" \
	LARGS="-Wl,-soname=libphoenix.so" \
	CENDLIB="-lm -lpthread -lpq -lodbc"

install phoenix.so ../lib/libphoenix.so

cd -

%{__make} -C msession \
	GCC="%{__cxx} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcxxflags}" \
	CENDLIB="-L../lib -lphoenix"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/msession,%{_sbindir},%{_includedir}/phoenix,%{_sysconfdir}}

install lib/libphoenix.* $RPM_BUILD_ROOT%{_libdir}

install src/{[!bmpstu]*,m[!befi]*,memheap,metadef,mf[!as]*,session}.h \
	$RPM_BUILD_ROOT%{_includedir}/phoenix

install msession/msession{d,rc} $RPM_BUILD_ROOT%{_sbindir}
install msession/*.so $RPM_BUILD_ROOT%{_libdir}/msession

install msession/msessiond.cfg $RPM_BUILD_ROOT%{_sysconfdir}/msessiond.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n phoenix -p /sbin/ldconfig
%postun	-n phoenix -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc msession/plugin.cpp msession/{PLUGINS,README}
%attr(755,root,root) %{_sbindir}/msession*
%dir %{_libdir}/msession
%attr(755,root,root) %{_libdir}/msession/*.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/msessiond.conf

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
