import argparse
import ipv4_address_analyzer, ipv6_address_analyzer

if __name__ == 'ipanalyzer.__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="CTFtools is used to perform some basic conversions and networking analysis functions for CTFs or pentesting."
    )

    parser.add_argument('operation', help='''Function to be implemented.
                        [ipv4, ipv6]''')

    parser.add_argument('-d','--address', metavar='', help="The IP address.")
    parser.add_argument('-n','--mask', metavar='', help="The subnet or CIDR mask.")
    parser.add_argument('-s','--subnet', metavar='', help="The Subnet address.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true', help='Print silently.')
    group.add_argument('-v', '--verbose', action='store_true', help='Print detailed information.')

    v6 = parser.add_mutually_exclusive_group()
    v6.add_argument('-a', '--abbreviate', action='store_true', help='Abbreviate long IPv6 address.')
    v6.add_argument('-e', '--expand', action='store_true', help='Expand short form IPv6 address')

    # Parse arguments
    args = parser.parse_args()
    IP = args.address
    Subnet = args.subnet
    Mask = args.mask
    
    if args.operation == 'ipv6':
        if args.quiet:
            if args.abbreviate:ipv6_address_analyzer.abbreviate_s(IP,Mask)
            elif args.expand:ipv6_address_analyzer.expand_s(IP,Mask)
            else:ipv6_address_analyzer.ipv6_s(IP)
        else:
            if args.abbreviate:ipv6_address_analyzer.abbreviate(IP,Mask)
            elif args.expand:ipv6_address_analyzer.expand(IP,Mask)
            else:ipv6_address_analyzer.ipv6(IP,Mask)
    elif args.operation == 'ipv4':
        if args.quiet:ipv4_address_analyzer.ipv4_s(IP,Mask,Subnet)
        else:ipv4_address_analyzer.ipv4(IP,Mask,Subnet)
