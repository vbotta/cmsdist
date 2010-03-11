### RPM external python-ldap 2.3.5
Source: http://voxel.dl.sourceforge.net/sourceforge/python-ldap/python-ldap-%{realversion}.tar.gz
Patch0: python-ldap-2.3.5-gcc44
Requires: python
Requires: openssl
Requires: openldap

%prep
%setup -q -n %n-%{realversion}
pwd
%patch0 -p1

%build
pwd

mkdir -p sasl2lib
ln -s /usr/lib/libsasl2.so.2.0.19 sasl2lib/libsasl2.so

perl -p -i -e 's|/usr/local/openldap-2.3/|$ENV{OPENLDAP_ROOT}/|; s|(library_dirs = .*)|$1 /usr/lib/sasl2 %{_builddir}/%n-%{realversion}/sasl2lib $ENV{OPENSSL_ROOT}/lib|;' setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://python-ldap.sourceforge.net/"></info>
<Client>
 <Environment name=PYTHON_LDAP_BASE default="%i"></Environment>
 <Environment name=PYTHON_LDAP_PYPATH default="$PYTHON_LDAP_BASE/lib/python@PYTHONV@/site-packages"></Environment>
</Client>
<use name=openssl>
<use name=openldap>
<use name=python>
<Runtime name=PYTHONPATH value="$PYTHON_LDAP_PYPATH" type=path>
</Tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

%post
%{relocateConfig}etc/scram.d/%n
