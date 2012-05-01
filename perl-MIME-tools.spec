# Note: MIME::tools > 5.420 require File::Temp >= 0.17, which is not available
# in Fedora prior to Fedora 9 (it's a core module)

Name:		perl-MIME-tools
Version:	5.427
Release:	4%{?dist}
Summary:	Modules for parsing and creating MIME entities in Perl
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/MIME-tools/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DONEILL/MIME-tools-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Path)	>= 1
BuildRequires:	perl(File::Spec)	>= 0.6
BuildRequires:	perl(File::Temp)	>= 0.18
BuildRequires:	perl(IO::File)		>= 1.13
BuildRequires:	perl(IO::Stringy)	>= 2.110
BuildRequires:	perl(MIME::Base64)	>= 3.03
BuildRequires:	perl-MailTools		>= 1.50
BuildRequires:	perl(MIME::QuotedPrint)
BuildRequires:	perl(Test::More), perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
MIME-tools is a collection of Perl5 MIME:: modules for parsing, decoding, and
generating single- or multipart (even nested multipart) MIME messages.

Yes, kids, that means you can send messages with attached GIF files.

%prep
%setup -q -n MIME-tools-%{version}

# Fix character encoding
/usr/bin/iconv -f iso-8859-1 -t utf-8 ChangeLog > ChangeLog.utf8
%{__mv} ChangeLog.utf8 ChangeLog

# The more useful examples will go in %{_bindir}
%{__mkdir} useful-examples
%{__mv} examples/mime{dump,encode,explode,postcard,send} useful-examples

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

# Put the more useful examples in %{_bindir}
%{__install} -d -m 755 %{buildroot}%{_bindir}
%{__install} -d -m 755 %{buildroot}%{_mandir}/man1
cd useful-examples
for ex in mime*
do
	%{__install} -p -m 755 ${ex} %{buildroot}%{_bindir}/
	/usr/bin/pod2man ${ex} > %{buildroot}%{_mandir}/man1/${ex}.1
done
cd -

%check
TEST_POD_COVERAGE=0 %{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
# Adding examples introduces additional deps, but these are all satisfied by
# perl, perl-MIME-tools, and perl-MailTools, which are all deps anyway.
%doc examples
%{perl_vendorlib}/MIME/
%{_bindir}/mime*
%{_mandir}/man1/mime*.1*
%{_mandir}/man3/MIME::*.3pm*

%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.427-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Paul Howarth <paul@city-fan.org> 5.427-1
- Update to 5.427
- Require and BuildRequire perl(IO::File) >= 1.13

* Wed Mar 19 2008 Paul Howarth <paul@city-fan.org> 5.426-1
- Update to 5.426
- Now require File::Temp >= 0.18
- Add POD tests, coverage disabled because of lack of coverage from upstream

* Tue Mar 11 2008 Paul Howarth <paul@city-fan.org> 5.425-1
- Update to 5.425
- Add note about File::Temp requirement
- New upstream maintainer -> updated URL for source
- Given that this package will not build on old distributions, don't cater
  for handling old versions of MIME::QuotedPrint in %%check and buildreq
  perl(MIME::Base64) >= 3.03
- Buildreq perl(File::Path) >= 1, perl(File::Spec) >= 0.6, and
  perl(IO::Stringy) >= 2.110
- Only include README as %%doc, not README*
- Dispense with provides filter, no longer needed

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.420-6
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.420-5
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 5.420-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Tue Apr 17 2007 Paul Howarth <paul@city-fan.org> 5.420-3
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug  8 2006 Paul Howarth <paul@city-fan.org> 5.420-2
- Install the more useful examples in %%{_bindir} (#201691)

* Wed Apr 19 2006 Paul Howarth <paul@city-fan.org> - 5.420-1
- 5.420
- Cosmetic changes reflecting new maintainer's preferences
- Examples remain executable since they don't introduce new dependencies
- Simplify provides filter

* Mon Jan 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 5.419-1
- 5.419.
- Don't provide perl(main).

* Tue Oct  4 2005 Paul Howarth <paul@city-fan.org> - 5.418-2
- License is same as perl (GPL or Artistic), not just Artistic

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 5.418-1
- 5.418.
- Cosmetic specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 5.417-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.417-1
- Update to 5.417.

* Wed Jan  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.416-0.fdr.1
- Update to 5.416.

* Thu Oct 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.415-0.fdr.1
- Update to 5.415.

* Thu Oct  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.414-0.fdr.1
- Update to 5.414.

* Wed Sep 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.413-0.fdr.1
- Update to 5.413, includes the mimedefang patches.
- Bring up to date with current fedora.us Perl spec template.

* Sat Feb  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.411-0.fdr.6.a
- Install into vendor dirs.
- BuildRequire perl-MailTools (bug 373).

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.5.a
- Hopefully fixed BuildRequires (for make test)
- rm-ing perllocal.pod instead of excluding it

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.4.a
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.3.a
- Changed Group tag value
- make test in build section
- Added missing directory

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.2.a
- Now using roaringpenguin tarball

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
