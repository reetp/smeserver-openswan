%define name smeserver-openswan
%define version 0.6
%define release 7
Summary: Plugin to enable IPSEC connections
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: GNU GPL version 2
URL: http://libreswan.org/
Group: SMEserver/addon
Source: %{name}-%{version}.tar.gz
Patch1: smeserver-openswan-fix-masq-templates.patch
Patch2: smeserver-openswan-move-logfile.patch
Patch3: smeserver-openswan-add-debug-key.patch
Patch4: smeserver-openswan-fix-rsa-id.patch
Patch5: smeserver-openswan-fix-createlinks.patch
BuildRoot: /var/tmp/%{name}-%{version}
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
Requires:  e-smith-release >= 8.0
Requires:  openswan >= 2.6.38
AutoReqProv: no

%description
Openswan is a free software implementation of the most widely supported and standarised VPN protocol based on ("IPsec") and the Internet Key Exchange ("IKE")

%changelog
* Sat Apr 23 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-7.sme
- Fix typo in createlinks for sysctl.conf

* Mon Apr 04 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-6.sme
- Fix ID in ipsec.secrets if ID is set
- Fix xfrm_larval_drop setting in ipsec-update

* Thu Mar 24 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-5.sme
- Add debug db key to /etc/ipsec.conf
- Remove setting public/private keys as they won't affect unless templates are re-expanded
- Set xfrm_larval_drop drop correctly
- minor formatting

* Thu Mar 24 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-4.sme
- split patch file to match libreswan

* Tue Mar 22 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-3.sme
- Fix masq templates for missing db keys on install
- Move pluto.log to /var/log/pluto
- regenerate masq template on ipsec-update
- change wiki location page
- add sysctl.conf template
- modify masq templates for ipsec status enabled/disabled
- only load ipsec.conf rather than *.conf to avoid loading v6neighbor-hole.conf

* Wed Mar 09 2016 JP Pialasse <tests@pialasse.com> 0.6-2.sme
- first import in SME buildsys

* Sat Dec 05 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.6-1
- New Branch for openswan on v8

* Wed Nov 25 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-9
- Copied code to openswan contrib as libreswan contrib is now LibreSwan specific

* Wed Nov 25 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-8
- Revised masq templates - disable on ipsec disable
- Template ipsec.secrets so Terry won't break it again
- Set requires e-smith >=9 and libreswan >=3.14

* Wed Nov 18 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-7
- add 90adjustESP

* Tue Nov 17 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-6
- more update to masq firewalls - change -p 50 to -p ESP

* Tue Nov 17 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-5
- update masq firewall rules
- document clean up

* Wed May 27 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-4
- set dpd actions off if ipsec is 'add'
- add salifetime key and rename ikelifetime and keylife
- change defaults for salifetime and ikelifetime
- add in rsasig support

* Wed Apr 22 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-3
- change default ike from aes-sha to aes-sha1

* Tue Mar 24 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-2
- More minor fixes - should work OK with xl2tpd

* Thu Mar 19 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.5-1
- Remove templates2expand and added to createlinks
- modified ipsec.secret template
- various other fixes

* Fri Mar 13 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.4-5
- Big changes again - now have PreviousState to detect changes
- Createlinks to S10 to run after expand-templates

* Thu Mar 5 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.4-4
- Changed lots. Removed sysctl.conf template
- Changed firewall template

* Tue Mar 3 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.4-3
- Load of code tidying and prep from xl2tpd

* Fri Feb 27 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.4-2
- Update action script and allow for system not in gateway mode
- add ike and phase2alg db settings

* Tue Feb 24 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.4-1
- New ipsec-action script
- Numerous template changes

* Fri Jan 16 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.3-1
- remove debugging lines
- remove expand templates from spec file
- add status check for ipsec.conf
- add comment to masq template
- updated db defaults
- ipsec.conf not expanded on install
- missed auto=start

* Fri Jan 16 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.2-1
- remove rc.local modifications
- add /etc/sysctl.conf patches

* Thu Jan 15 2015 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-1
- initial release

%prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist


%clean
cd ..
rm -rf %{name}-%{version}

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%pre
%preun
%post

/sbin/e-smith/expand-template /etc/rc.d/init.d/masq
/sbin/e-smith/expand-template /etc/inittab
/sbin/init q


echo "see http://wiki.contribs.org/VPN"

%postun
/sbin/e-smith/expand-template /etc/rc.d/init.d/masq
/sbin/e-smith/expand-template /etc/inittab
/sbin/init q
