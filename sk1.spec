%define oname	sK1

%define rel	1
%define svn	422
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%oname
%else
%define release		%mkrel %rel
%define distname	%oname-%version.tar.gz
%define dirname		%oname-%version
%endif

Name:		sk1
Summary:	Advanced vector graphics editor
Version:	0.9.0
Release:	%release
Source0:	http://sk1project.org/downloads/%{oname}/%{distname}
# From ALT: fixes installation of needed modules - AdamW 2008/05
Patch0:		sk1-0.9.0-modules.patch
Group:		Graphics
BuildRequires:	X11-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	python-devel
BuildRequires:	freetype2-devel
BuildRequires:	cairo-devel
BuildRequires:	libxext-devel
License:	GPLv2+ and LGPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	tkinter
Requires:	python-imaging
Requires:	python-lcms
Requires:	zenity
Provides:	sketch
Provides:	skencil
Obsoletes:	skencil < 0.6.19
URL:		http://sk1project.org/

%description
sK1 is an open source vector graphics editor similar to CorelDRAW,
Adobe Illustrator, or Freehand. sK1 is mainly oriented for PostScript
processing. It features CMYK colorspace support, CMYK support in
Postscript, a Cairo-based engine, color managment, universal CDR
importer (7-X3 versions), and a modern Ttk based (former Tile widgets)
user interface.

%prep
%setup -q -n %{dirname}
%patch0 -p0 -b .modules

%build
%{__python} ./setup.py build

%install
rm -fr %{buildroot}
%{__python} setup.py install --root=%{buildroot} --compile --optimize=2

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
for i in 16 32 48 64; do \
install -m 0644 src/share/icons/CrystalSVG/icon_sk1_$i.png %{buildroot}%{_iconsdir}/hicolor/$i\x$i/apps/%{name}.png; \
done

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=sK1
Comment=Vector drawing tool
Exec=%{_bindir}/%{name} %f
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=image/x-sk
Categories=Graphics;VectorGraphics;
EOF

%post
%update_icon_cache hicolor
%update_menus
%update_desktop_database
%postun
%clean_icon_cache hicolor
%clean_menus
%clean_desktop_database

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{py_platsitedir}/%{name}
%{_bindir}/%{name}
%{py_platsitedir}/%{oname}-%{version}-py%{pyver}.egg-info
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop