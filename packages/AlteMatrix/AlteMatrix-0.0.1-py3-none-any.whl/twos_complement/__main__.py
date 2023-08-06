import argparse

if __name__ == 'twos_complement.__main__':
    import twos_complement as c2
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="CTFtools is used to perform some basic conversions and networking analysis functions for CTFs or pentesting."
    )
    parser.add_argument('com2', help='The function to be called for this program.')
    parser.add_argument('x', help="Number to be tested.")
    parser.add_argument('y', help="Number to use as multiplier.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true', help='Print silently.')
    group.add_argument('-v', '--verbose', action='store_true', help='Print detailed information.')

    # Parse arguments
    args = parser.parse_args()
    l = int(args.x)
    m = int(args.y)

    if args.com2:
        if args.quiet:c2.com2_s(l,m)
        else:c2.com2(l,m)
