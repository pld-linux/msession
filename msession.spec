Summary:	msession daemon - pseudo-database memory cache
Summary(pl):	Demon msession - pseudo-bazodanowe cache
Name:		msession
Version:	020415
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.mohawksoft.com/phoenix/%{name}-%{version}.tgz
Source1:	http://www.mohawksoft.com/phoenix/phoenix-%{version}.tgz
URL:		http://www.mohawksoft.com/phoenix/
BuildRequires:	gcc-c++
BuildRequires:	postgresql-devel
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
cd lib
ln -sf Linux.mak config.mak

%{__make} \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags}"

rm -f *.o

%{__make} libphoenix.so \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags} -fPIC" \
	LINK_DLL="%{__cc} -shared -Wl,-soname=libphoenix.so -lm -lpthread"

cd ../msession

%{__make} \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags}"

%{__make} pgplug.so \
	GCC="%{__cc} -DLINUX -DGCC -DPOSIX" \
	CCOPT="%{rpmcflags}" \
	PGSQL_LIB="-lpq"
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_includedir}/phoenix}

install lib/libphoenix.* $RPM_BUILD_ROOT%{_libdir}

rm -f lib/{*tbl,mbitmap,metacore,mfamort,mfserial,misalpha,ndxfile,primes,unixcom}.h
install lib/*.h $RPM_BUILD_ROOT%{_includedir}/phoenix

install msession/msessiond $RPM_BUILD_ROOT%{_sbindir}
install msession/{flexplug,fnplug,pgplug,protplug}.so $RPM_BUILD_ROOT%{_libdir}

gzip -9nf lib/README msession/{PLUGINS,README}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n phoenix -p /sbin/ldconfig
%postun	-n phoenix -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc msession/*.gz msession/plugin.cpp
%attr(755,root,root) %{_sbindir}/msessiond
%attr(755,root,root) %{_libdir}/flexplug.so
%attr(755,root,root) %{_libdir}/fnplug.so
%attr(755,root,root) %{_libdir}/protplug.so

%files pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pgplug.so

%files -n phoenix
%defattr(644,root,root,755)
%doc lib/*.gz
%attr(755,root,root) %{_libdir}/libphoenix.so

%files -n phoenix-devel
%defattr(644,root,root,755)
%{_includedir}/phoenix

%files -n phoenix-static
%defattr(644,root,root,755)
%{_libdir}/libphoenix.a
