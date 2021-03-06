#global         rel_tag      .20120615gitcdab110

Name:           bombono-dvd
Version:        1.2.2
Release:        11%{?rel_tag}%{?dist}
Summary:        DVD authoring program with nice and clean GUI
                # License breakdown in README.
License:        GPLv2 and GPLv2+ and Boost and Python and LGPLv2+
Group:          Applications/Productivity
Url:            http://www.bombono.org
# To create source tarball:
# git clone https://git.gitorious.org/bombono-dvd/bombono-dvd.git bombono-dvd
# tag=.20120616gitcdab110; cd bombono-dvd;  git reset --hard ${tag##*git}; cd ..
# tar czf bombono-dvd-1.2.0$tag.tar.gz --exclude .git bombono-dvd
#Source:         bombono-dvd-%%{version}%%{?rel_tag}.tar.gz
Source:         http://sourceforge.net/projects/bombono/files/bombono-dvd/1.2/bombono-dvd-1.2.2.tar.bz2
Patch0:         filesys-include-path.patch
                # https://sourceforge.net/apps/trac/bombono/ticket/98
Patch1:         0001-ffmpeg-has-renamed-CodecID-AVCodecID.patch

# needs to match TBB - from adobe-source-libraries
ExclusiveArch:  i686 x86_64 ia64

BuildRequires:  adobe-source-libraries-devel
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  gtkmm24-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libxml++-devel
BuildRequires:  mjpegtools-devel
BuildRequires:  pkgconfig
BuildRequires:  scons
Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       enca
Requires:       ffmpeg
Requires:       mjpegtools
#Suggests:      totem, gvfs, scons, twolame

# http://lists.rpmfusion.org/pipermail/rpmfusion-developers/2012-January/011438.html
Provides:       bundled(boost-logging) = 0.22.7.20120126svn76686

%global  boost_flags \\\
    -DBOOST_SYSTEM_NO_DEPRECATED -DBOOST_FILESYSTEM_VERSION=3
%global warn_flags  \
    -Wno-reorder -Wno-unused-variable
%global  scons       \
    scons  %{?jobs:-j%{jobs}}                              \\\
    BUILD_CFG=debug                                        \\\
    BUILD_BRIEF=false                                      \\\
    BUILD_QUICK=false                                      \\\
    CC="%__cc"                                             \\\
    CXX="%__cxx"                                           \\\
    CFLAGS=""                                              \\\
    CPPFLAGS="%{optflags} %{warn_flags} %{boost_flags}"    \\\
    PREFIX=%{_prefix}                                      \\\
    TEST=false                                             \\\
    TEST_BUILD=false                                       \\\
    USE_EXT_BOOST=true                                     \\\
    USE_EXT_ASL=true

%description
Bombono DVD is an easy to use program for making DVD-Video. The main features
are an excellent MPEG viewer with time line, a real WYSIWYG menu editor with
live thumbnails and monitor, and comfortable Drag-N-Drop support. Authoring
to folder, making an ISO-image or burning directly to DVD as well as
re-authoring by importing video from DVD discs is also supported.

%prep
%setup -q
%if %{fedora} > 17
%patch0 -p1
%patch1 -p1
%endif
sed -i '\;#![ ]*/usr/bin/env;d'  $(find . -name SCons\*)
rm -r debian libs/boost-lib src/mlib/tests libs/mpeg2dec ./libs/asl/adobe

%build
%scons build

%install
rm config.opts
%scons DESTDIR=%{buildroot} install
rm -rf docs/man docs/TechTasks docs/Atom.planner
%find_lang %{name}
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/bombono-dvd.desktop

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%post
/usr/bin/update-desktop-database  &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f  bombono-dvd.lang
%doc README COPYING docs
%{_bindir}/*
%{_datadir}/bombono
%{_datadir}/applications/bombono-dvd.desktop
%{_datadir}/pixmaps/bombono-dvd.png
%{_datadir}/icons/hicolor/*/apps/bombono-dvd.png
%{_datadir}/mime/packages/bombono.xml
%{_mandir}/man1/*

%changelog
* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 1.2.2-11
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-10
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1.2.2-9
- Rebuilt for ffmpeg-2.3

* Sat Aug 02 2014 Sérgio Basto <sergio@serjux.com> - 1.2.2-8
- Rebuilt for boost-1.55

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 1.2.2-7
- Rebuilt for ffmpeg-2.2

* Fri Dec 27 2013 leamas@nowhere.net - 1.2.2-6
- Rebuild after F20 branching

* Thu May 26 2013 Alec Leamas <leamas@nowhere.net> - 1.2.2-5
- Build problems for f20.

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-2
- Rebuilt for x264/FFmpeg

* Sat Mar 9 2013 Alec Leamas <alec@nowhere.com> - 1.2.2-1
- Rebuilt for new upstream release

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-8.20120615gitcdab110
- Rebuilt for FFmpeg 1.0

* Wed Oct 24 2012 Alec Leamas <leamas@nowhere.net>    - 1.2.0-7.20120616gitcdab110
- Typos in spec file, stepping rel #
- Added patch for current boost available but not merged upstream.
- Fixed build flags (new patch)
- Removed insane release # from source filename.

* Mon Jul 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-4.20120616gitcdab110.2
- Add ExclusiveArch - inherited from TBB

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-4.20120616gitcdab110.1
- Rebuilt for FFmpeg

* Sat Jun 16 2012 Alec Leamas <alec@nowhere.com> 1.2.0-4.20120616gitcdab110
- Updating to git HEAD, solving build problems w ffmpeg 11.1

* Thu Apr 12 2012 Alec Leamas <alec@nowhere.com> 1.2.0-3.20120412gite9390e7
- Fixing source name error
- Updating to latest git (fixing f17 compile error).

* Thu Apr 12 2012 Alec Leamas <alec@nowhere.com> 1.2.0-2.20120412gite9390e7
- Bad version, not built

* Sun Apr 01 2012 Alec Leamas <alec@nowhere.com> 1.2.0-1.20120401git2278251
- New version-release scheme
- Minor fixes
* Sat Mar 28 2012 Alec Leamas <alec@nowhere.com> 1.2.0.20120128gitf39d5d5-1
- Adding BR: adobe-source-libraries-devel
- Removing copyright notices after email discussion with Ilya.
- Updating to latest git
- The upstream version unbundles adobe-source-libraries
* Sat Jan 28 2012 Alec Leamas <alec@nowhere.com> 1.2.0.20120128gitf39d5d5-1
- Adding  bundling exception for boost-logging.
* Wed Jan 25 2012 Alec Leamas <alec@nowhere.com> 1.2.0.20120125git3f4adbb-1
- Removing irrelevant files in docs/
- Updating deps to reflect bb7f789 "twolame is optional..."
- Removing bundled libmpeg2
* Sat Jan 21 2012 Alec Leamas <alec@nowhere.com>   1.2.0.20101210git2840c3a-1
- Updating to latest git source. Many patches accepted.
- Removing %%defattr.
* Sat Jan 14 2012 Alec Leamas <alec@nowhere.com>             1.2.0-4
- Refactoring scons parameters to rpm macro %%scons.
- Adding virtual provide for bundled mpeg lib.
- Use of Boost license, was BSD, handling license file.
* Sun Jan 8 2012 Alec Leamas <alec@nowhere.com>              1.2.0-3
- Using external boost lib, removing bundled one.
- Feeding standard rpm build flags to scons.
- Cleaning up post/posttrans snippets and deps.
- Restoring execute permissions on some scripts in %%prep
* Fri Jan 6 2012 Alec Leamas <alec@nowhere.com>              1.2.0-2
- Using manpages from debian dir, remove debian stuff.
* Tue Jan 4 2012 Alec Leamas <alec@nowhere.com>              1.2.0-1
- First attempt to modify Ilya Murav'jo's spec file for Fedora.
- Adding changelog
- Added find_lang handling of .mo files.
- Adjusted source URL, Fedora wants a complete public one.
- Adjusted License: tag to reflect README.
- Removed things not used and/or deprecated in Fedora.
- Added scriptlets handling icons and mime types.
- Added %%doc
- Modified arguments to scons build and install.
- Fixed various rpmlint warnings
- Adjusted dependencies after mock build test.
* Mon Jan 1 2007  Ilya Murav'jov <muravev@yandex.ru>         1.0.2-0
- Faked entry by Alec leamas to reflect initial packager.

# vim: set expandtab ts=4 sw=4:
