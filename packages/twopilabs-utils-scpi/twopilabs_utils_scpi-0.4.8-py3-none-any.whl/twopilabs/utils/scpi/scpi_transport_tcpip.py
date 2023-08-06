import socket
import logging
import re
import itertools
from urllib.parse import urlparse
from typing import *
from .scpi_transport_base import ScpiTransportBase
from .scpi_resource import ScpiResource
from .scpi_exceptions import ScpiTransportException


class ScpiTcpIpTransport(ScpiTransportBase):
    DEFAULT_PORT: int = 5025

    _transport_class = 'ScpiTcpIpTransport'
    _transport_info = 'TCP/IP SCPI Transport'
    _transport_type = 'TCP/IP'

    _sock: Optional[socket.socket] = None

    @classmethod
    def discover(cls,
                 dnssd_services: List[str] = ('_scpi-raw._tcp.local.',),
                 dnssd_domains: List[str] = ('local',),
                 dnssd_names: List[str] = ('.*',),
                 dnssd_ipversions: str = '',
                 dnssd_timeout: float = 0.5) -> List[ScpiResource]:
        from zeroconf import Zeroconf, ServiceListener, ServiceBrowser, IPVersion
        import time

        class Listener(ServiceListener):
            def __init__(self):
                self.services = {}

            def remove_service(self, zeroconf, zc_type, zc_name):
                self.services.pop(zc_name)

            def add_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})


            def update_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})

        # Generate fully qualified service names by permuting given services with given domains
        dnssd_services_fq = [f'{s}.{d}' + ('.' if not d.endswith('.') else '')
                             for s, d in itertools.product(dnssd_services, dnssd_domains)]

        # Find devices via zeroconf mDNS
        # TODO: Implement DNS-SD for non-.local domains
        ip_version = IPVersion.All if '4' in dnssd_ipversions and '6' in dnssd_ipversions else \
            IPVersion.V4Only if '4' in dnssd_ipversions else IPVersion.V6Only if '6' in dnssd_ipversions else None

        listener = Listener()
        zc = Zeroconf(ip_version=ip_version)
        ServiceBrowser(zc, dnssd_services_fq, listener=listener)

        # Wait for some time to get answers
        time.sleep(dnssd_timeout)

        # Patterns to check name against
        patterns = [re.compile(pattern) for pattern in dnssd_names]

        return [ScpiResource(transport=ScpiTcpIpTransport,
                             location=f'dnssd:{service.name}',
                             address=(parsed_address, int(service.port)),
                             name=service.get_name(),
                             manufacturer=service.properties[b'Manufacturer'].decode(
                                 'utf-8') if b'Manufacturer' in service.properties else None,
                             model=service.properties[b'Model'].decode(
                                 'utf-8') if b'Model' in service.properties else None,
                             serialnum=service.properties[b'SerialNumber'].decode(
                                 'utf-8') if b'SerialNumber' in service.properties else None,
                             info=service
                             ) for service in listener.services.values() for parsed_address in service.parsed_scoped_addresses()
                if any([pattern.fullmatch(service.get_name()) for pattern in patterns])]

    @classmethod
    def from_resource_name(cls, resource_name: str) -> Optional[ScpiResource]:
        m = re.match((
            r'^(?P<prefix>(?P<type>TCPIP)(?P<board>\d+)?)'
            r'::((?P<host_address>[^:]+)|(\[(?P<host_address6>.+)\]))'
            r'::(?P<host_port>([0-9]+))'
            r'(::(?P<suffix>SOCKET))?$'
        ), resource_name, re.IGNORECASE)

        if m is None:
            # Does not match the regex
            return None

        groupdict = m.groupdict()

        # Get either IPv4 or IPv6 address
        host_address = groupdict['host_address'] if groupdict['host_address'] is not None else groupdict['host_address6']
        host_port = groupdict['host_port']

        return ScpiResource(
            transport=ScpiTcpIpTransport,
            address=(host_address, host_port)
        )

    @classmethod
    def to_resource_name(cls, resource: ScpiResource) -> str:
        host_address = resource.address[0] if not ':' in resource.address[0] else f'[{resource.address[0]}]'
        host_port = resource.address[1] if len(resource.address) > 1 else cls.DEFAULT_PORT

        return f'TCPIP::{host_address}::{host_port}::SOCKET'

    def __init__(self, address: Union[tuple, str], timeout: float = 5, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._sock = None

        if isinstance(address, str):
            # Convert from string to tuple first
            addr = urlparse('//' + address)
            if (addr.hostname is None):
                raise ScpiTransportException(f'{address} is not a valid hostname')
            address = (addr.hostname, addr.port) if addr.port is not None else (addr.hostname, self.DEFAULT_PORT)

        try:
            # Get address info
            addr_info = socket.getaddrinfo(address[0], address[1], type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        except socket.gaierror as e:
            raise ScpiTransportException(e) from e

        try:
            # Try to connect
            self._sock = socket.socket(addr_info[0][0], addr_info[0][1], addr_info[0][2])
            self._sock.settimeout(timeout)
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._sock.connect(addr_info[0][4])

            # Make a file interface for easier handling
            self._io = self._sock.makefile('rwb', buffering=0)
            self._io.flush()
        except OSError as e:
            raise ScpiTransportException(e) from e

    def close(self) -> None:
        # Do regular closing
        super().close()

        # Close socket as well
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        self._sock = None
