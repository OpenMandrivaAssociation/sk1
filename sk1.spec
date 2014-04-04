%define oname sK1

# https://sk1.svn.sourceforge.net/svnroot/sk1/trunk/sK1
%define svn 737

Summary:	Advanced vector graphics editor
Name:		sk1
Version:	0.9.1
Release:	0.%{svn}.2
License:	GPLv2+ and LGPLv2+
Group:		Graphics
Url:		http://sk1project.org/
Source0:	http://sk1project.org/downloads/%{oname}/%{name}-%{svn}.tar.lzma
# Fix / kludge for Tcl 8.6 (good old interp->result) - AdamW 2008/12
Patch0:		sk1-601-tcl86.patch
Patch1:		sk1-0.9.1-linkage.patch
BuildRequires:	tcl
BuildRequires:	tk
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
Requires:	tkinter
Requires:	python-imaging
Requires:	python-lcms
Requires:	zenity
Provides:	sketch = %{EVRD}
Provides:	skencil = %{EVRD}

%description
sK1 is an open source vector graphics editor similar to CorelDRAW,
Adobe Illustrator, or Freehand. sK1 is mainly oriented for PostScript
processing. It features CMYK colorspace support, CMYK support in
Postscript, a Cairo-based engine, color managment, universal CDR
importer (7-X3 versions), and a modern Ttk based (former Tile widgets)
user interface.

%files
%{py_platsitedir}/%{name}
%{_bindir}/%{name}
%{py_platsitedir}/%{oname}-%{version}pre-py%{py_ver}.egg-info
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}
%patch0 -p1 -b .tcl86
%patch1 -p1 -b .linkage
sed -i -e 's,tcl8.5,tcl%{tcl_version},g' setup.py
sed -i -e 's,tk8.5,tk%{tcl_version},g' setup.py

%build
python ./setup.py build

%install
python setup.py install --root=%{buildroot} --compile --optimize=2

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
for i in 16 32 48 64; do \
install -m 0644 src/share/icons/CrystalSVG/icon_sk1_$i.png %{buildroot}%{_iconsdir}/hicolor/$i\x$i/apps/%{name}.png; \
done

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
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

