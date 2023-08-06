from base64 import b64encode, b64decode
from glob import glob
import os
import posixpath
import socket
import sys
from raft import task
import yaml
from boto3 import Session
from sewer.client import Client
from sewer.dns_providers.route53 import Route53Dns


def new_cert(hostname, alt_domains, email=None, profile=None):
    """
    :param str hostname:
        the fqdn of the local host for which we are creating the cert

    :param str alt_domains:
        a comma-separated list of alternative domains to also
        requests certs for.

    :param str email:
        the email of the contact on the cert

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials
    """
    if profile:
        os.environ['AWS_PROFILE'] = profile
    alt_domains = alt_domains.split(',') if alt_domains else []
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(), ACME_AUTH_STATUS_WAIT_PERIOD=5,
        ACME_AUTH_STATUS_MAX_CHECKS=180, ACME_REQUEST_TIMEOUT=60)
    certificate = client.cert()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def get_certificate(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        ssm = session.client('ssm')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'account_key' ])
        account_key = get_chunked_ssm_parameter(name, profile=profile)
        print('account key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'key' ])
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        key = response['Parameter']['Value']
        print('private key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'cert' ])
        certificate = get_chunked_ssm_parameter(name, profile=profile)
        print('public cert retrieved')
    except:  # noqa: E722, pylint: disable=bare-except
        account_key = None
        key = None
        certificate = None
    return certificate, account_key, key


def get_certificate_from_s3(bucket, ns, hostname, profile=None):
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        s3 = session.client('s3')
        key = posixpath.join(ns, f'{hostname}.account_key')
        print(f'retrieving s3://{bucket}/{key}')
        response = s3.get_object(Bucket=bucket, Key=key)
        account_key = response['Body'].read().decode('utf-8')
        print('account key retrieved')
        key = posixpath.join(ns, f'{hostname}.key')
        print(f'retrieving s3://{bucket}/{key}')
        response = s3.get_object(Bucket=bucket, Key=key)
        key_content = response['Body'].read().decode('utf-8')
        print('private key retrieved')
        key = posixpath.join(ns, f'{hostname}.crt')
        print(f'retrieving s3://{bucket}/{key}')
        response = s3.get_object(Bucket=bucket, Key=key)
        certificate = response['Body'].read().decode('utf-8')
        print('public cert retrieved')
    except Exception as ex:  # noqa: E722, pylint: disable=bare-except
        account_key = None
        key_content = None
        certificate = None
        print(f'exception retrieving keys: {ex}')
    return certificate, account_key, key_content


def get_chunked_ssm_parameter(name, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    rg = []
    for n in range(1, 10):
        try:
            st = f'{name}{n}'
            print(f'[ssm]  getting {st}')
            response = ssm.get_parameter(Name=st, WithDecryption=True)
            rg.append(response['Parameter']['Value'])
        except:  # noqa: E722, pylint: disable=bare-except
            break
    data = ''.join(rg)
    return data


def get_pfx(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    name = '/'.join([ ns, 'apps_keystore', hostname, 'pfx' ])
    pfx_data = get_chunked_ssm_parameter(name, profile=profile)
    pfx_data = b64decode(pfx_data.encode('utf-8'))
    print(f'[pfx]  decoded {len(pfx_data)} bytes')
    return pfx_data


def renew_cert(
        ns, hostname, alt_domains=None,
        email=None, profile=None, **kwargs):
    if profile:
        os.environ['AWS_PROFILE'] = profile
    bucket = kwargs.get('bucket')
    alt_domains = alt_domains.split(',') if alt_domains else []
    if bucket:
        _, account_key, key = get_certificate_from_s3(bucket, ns, hostname, profile)
    else:
        _, account_key, key = get_certificate(ns, hostname, profile)
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(), account_key=account_key,
        certificate_key=key, ACME_AUTH_STATUS_WAIT_PERIOD=60,
        ACME_AUTH_STATUS_MAX_CHECKS=15, ACME_REQUEST_TIMEOUT=60)
    certificate = client.renew()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def pfx(ctx, certificate, key):
    f1, f2, f3 = '/tmp/p1.cert', '/tmp/p1.crt', '/tmp/p1.pfx'
    with open(f1, 'w') as f:
        f.write(certificate)
    with open(f2, 'w') as f:
        f.write(key)
    os.chmod(f1, 0o644)
    os.chmod(f2, 0o600)
    ctx.run(
        f'/usr/bin/openssl pkcs12 -export -in {f1} -inkey {f2}'
        f' -out {f3} -passout pass:')
    with open(f3, 'rb') as f:
        data = f.read()
    data = b64encode(data).decode('utf-8')
    os.remove(f1)
    os.remove(f2)
    os.remove(f3)
    return rg


def full_pfx(ctx, certificate, key):
    f1, f2, f3 = '/tmp/p1.cert', '/tmp/p1.crt', '/tmp/p1.pfx'
    with open(f1, 'w') as f:
        f.write(certificate)
    with open(f2, 'w') as f:
        f.write(key)
    os.chmod(f1, 0o644)
    os.chmod(f2, 0o600)
    ctx.run(
        f'/usr/bin/openssl pkcs12 -export -in {f1} -inkey {f2}'
        f' -out {f3} -passout pass:')
    with open(f3, 'rb') as f:
        data = f.read()
    os.remove(f1)
    os.remove(f2)
    os.remove(f3)
    return data


@task
def renew_all(ctx, dir_name=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str dir_name:
        the config directory

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(dir_name, 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    dir_name = os.path.join(dir_name, '*.yml')
    files = glob(dir_name)
    for filename in files:
        if filename.endswith('defaults.yml'):
            continue
        request_cert(ctx, filename, profile, defaults)


def request_cert(ctx, filename, profile, defaults):
    print(f'processing {filename}')
    with open(filename, 'r') as f:
        values = yaml.load(f, Loader=yaml.SafeLoader)
    for key, value in defaults.items():
        values.setdefault(key, value)
    namespaces = values.pop('namespaces', [])
    profile = profile or values.pop('profile', None)
    ns = namespaces[0]
    certificate, account_key, key = renew_cert(
        **values, ns=ns, profile=profile)
    tmp_dir = values.pop('tmp_dir', None)
    bucket = values.pop('bucket', None)
    for x in namespaces:
        if tmp_dir:
            save_to_file(
                ctx, tmp_dir, values['hostname'],
                certificate, account_key, key)

        save_to_s3(
            ctx, bucket, x, values['hostname'], certificate,
            account_key, key, profile=profile)
        save_to_ssm(ctx, x, values['hostname'], certificate, account_key, key)


@task
def request(ctx, filename=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str filename:
        the config file

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(os.path.dirname(filename), 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    request_cert(ctx, filename, profile, defaults)


def save_to_file(ctx, tmp_dir, hostname, certificate, account_key, key):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    contents = [
        ('.crt', certificate),
        ('.account_key', account_key),
        ('.key', key),
    ]
    for extension, content in contents:
        filename = f'{hostname}{extension}'
        filename = os.path.join(tmp_dir, filename)
        print(f'saving {filename}')
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir, 0o755, True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)


def save_to_s3(ctx, bucket, ns, hostname, certificate, account_key, key,
               profile=None):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    pfx = full_pfx(ctx, certificate, key)
    contents = [
        ('.crt', certificate),
        ('.account_key', account_key),
        ('.key', key),
        ('.pfx', pfx),
    ]
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    for extension, content in contents:
        filename = f'{hostname}{extension}'
        filename = posixpath.join(ns, filename)
        print(f'saving s3://{bucket}/{filename}')
        if isinstance(content, str):
            content = content.encode('utf-8')
        s3.put_object(Bucket=bucket, Key=filename, Body=content)


def save_to_ssm(ctx, ns, hostname, certificate, account_key, key, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pfx_data = pfx(ctx, certificate, key)
    hostname = hostname.replace('*', 'star')
    prefix = ns
    if not prefix.startswith('/'):
        prefix = f'/{prefix}'
    prefix = os.path.join(prefix, 'apps_keystore', hostname)
    contents = [
        ('account_key', account_key),
        ('cert', certificate),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        print(f'saving {name}')
        save_chunked_ssm_parameter(ns, name, content, 'String', profile)

    contents = [
        ('key', key),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        print(f'saving {name}')
        try:
            ssm.put_parameter(
                Name=name,
                Description=f'sewer / certbot {suffix}',
                Value=content,
                Overwrite=True,
                Type='SecureString',
                KeyId=f'alias/{ns}')
        except Exception as ex:
            print(f'exception saving to ssm: {ex}')

    name = os.path.join(prefix, 'pfx')
    save_chunked_ssm_parameter(ns, name, pfx_data, 'SecureString', profile)


def save_chunked_ssm_parameter(ns, name, value, type_, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pieces = []
    while value:
        pieces.append(value[:4096])
        value = value[4096:]
    for n, x in enumerate(pieces, 1):
        st = f'{name}{n}'
        print(f'saving {st}')
        try:
            if type_ == 'SecureString':
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_,
                    KeyId=f'alias/{ns}')
            else:
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_)
        except Exception as ex:
            print(f'exception saving to ssm: {ex}')


@task
def install_cert(ctx, config, hostname=None):
    """
    installs a cert on the local system:

        on linux to /etc/ssl/certs
        on windows to cert:/localmachine/my
    """
    with open(config, 'r') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    ns = conf['namespace']
    profile = conf.get('profile')
    owner = conf.get('owner', 'root')
    group = conf.get('group', owner)
    cert_filename = conf.get('certificate')
    key_filename = conf.get('key')
    hostname = hostname or conf.get('hostname')
    bucket = conf.get('bucket')
    if not hostname:
        hostname = get_hostname(ctx)
    if is_linux():
        install_cert_on_linux(
            ctx, ns, hostname, profile,
            cert_filename, key_filename, owner, group, bucket=bucket)
    elif is_windows():
        install_cert_on_windows(
            ctx, ns, hostname, profile)


def get_hostname(ctx):
    if is_linux():
        result = ctx.run('/bin/hostname')
        return result.stdout.strip()
    if is_windows():
        result = socket.getfqdn()
        return result
    return None


def install_cert_on_linux(
        ctx, ns, hostname, profile, cert_filename, key_filename,
        owner, group, bucket=None):
    if bucket:
        certificate, _, key = get_certificate_from_s3(bucket, ns, hostname, profile)
    else:
        certificate, _, key = get_certificate(ns, hostname, profile)
    if not cert_filename:
        st = f'{hostname}.bundled.crt'
        cert_filename = os.path.join('/etc/ssl/certs', st)
    if not key_filename:
        key_filename = os.path.join('/etc/ssl/private', f'{hostname}.key')
    with open(cert_filename, 'w') as f:
        f.write(certificate)
    ctx.run(f'chmod 0644 {cert_filename}')
    ctx.run(f'chown {owner}:{group} {cert_filename}')
    with open(key_filename, 'w') as f:
        f.write(key)
    ctx.run(f'chmod 0600 {key_filename}')
    ctx.run(f'chown {owner}:{group} {key_filename}')


@task
def install_cert_on_windows(ctx, ns, hostname, profile):
    """
    not yet implemented -- have to find a good, cost-effective way
    to generate the pfx file and store to ssm
    """
    pfx_data = get_pfx(ns, hostname, profile)
    c = 'powershell.exe -command "[System.IO.Path]::GetTempFileName()"'
    result = ctx.run(c)
    filename = result.stdout.strip()
    with open(filename, 'wb') as f:
        f.write(pfx_data)
    c = (
        'powershell.exe -command "'
        'Import-PfxCertificate '
        r'  -CertStoreLocation cert:\localmachine\my'
        f' -filepath {filename}'
        f'"'
    )
    ctx.run(c)
    os.remove(filename)


def is_linux():
    return sys.platform == 'linux'


def is_windows():
    return sys.platform == 'win32'
