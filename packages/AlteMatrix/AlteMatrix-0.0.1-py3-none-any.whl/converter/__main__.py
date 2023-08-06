import argparse

if __name__ == 'converter.__main__':
    import binary, decimal, hexadecimal, octal ,user_defined
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="CTFtools is used to perform some basic conversions and networking analysis functions for CTFs or pentesting."
    )
    parser.add_argument('operation', help='''Function to be implemented.
                        [b2o, bin-oct | b2d, bin-dec | b2h, bin-hex | b2t, bin-txt | d2b, dec-bin | d2o, dec-oct |
                        d2h, dec-hex | d2t, dec-txt | b2o, oct-bin | b2d, oct-dec | b2h, oct-hex | b2t, oct-txt |
                        b2o, hex-bin | b2d, hex-oct | b2h, hex-dec | b2t, hex-txt | udf, user-defined | udt, udef-text] 
                        NOTE: You do need to use the optional argument [-x] when conveting to or from text or using the 
                        user-defined functions!''')
    parser.add_argument('-x','--data', metavar='', help="Number or text to be converted.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true', help='Print silently.')
    group.add_argument('-v', '--verbose', action='store_true', help='Print detailed information.')

    # Parse arguments
    args = parser.parse_args()
    data = args.data

    if args.operation == 'b2o' or args.operation == 'bin-oct':
        if args.quiet:binary.binary_to_octal_s(data)
        else:binary.binary_to_octal(data)
    elif args.operation == 'b2d' or args.operation == 'bin-dec':
        if args.quiet:binary.binary_to_decimal_s(data)
        else:binary.binary_to_decimal(data)
    elif args.operation == 'b2h' or args.operation == 'bin-hex':
        if args.quiet:binary.binary_to_hexadecimal_s(data)
        else:binary.binary_to_hexadecimal(data)
    elif args.operation == 'b2t' or args.operation == 'bin-txt':
        if args.quiet:binary.binary_to_text_s()
        else:binary.binary_to_text()
    elif args.operation == 'd2b' or args.operation == 'dec-bin':
        if args.quiet:decimal.decimal_to_binary_s(data)
        else:decimal.decimal_to_binary(data)
    elif args.operation == 'd2o' or args.operation == 'dec-oct':
        if args.quiet:decimal.decimal_to_octal_s(data)
        else:decimal.decimal_to_binary(data)
    elif args.operation == 'd2h' or args.operation == 'dec-hex':
        if args.quiet:decimal.decimal_to_hexadecimal_s(data)
        else:decimal.decimal_to_hexadecimal(data)
    elif args.operation == 'd2t' or args.operation == 'dec-txt':
        if args.quiet:decimal.decimal_to_text_s()
        else:decimal.decimal_to_text()
    elif args.operation == 'o2b' or args.operation == 'oct-bin':
        if args.quiet:octal.octal_to_binary_s(data)
        else:octal.octal_to_binary(data)
    elif args.operation == 'o2d' or args.operation == 'oct-dec':
        if args.quiet:octal.octal_to_decimal_s(data)
        else:octal.octal_to_decimal(data)
    elif args.operation == 'o2h' or args.operation == 'oct-hex':
        if args.quiet:octal.octal_to_hexadecimal_s(data)
        else:octal.octal_to_hexadecimal(data)
    elif args.operation == 'o2t' or args.operation == 'oct-txt':
        if args.quiet:octal.octal_to_text_s()
        else:octal.octal_to_text()
    elif args.operation == 'h2b' or args.operation == 'hex-bin':
        if args.quiet:hexadecimal.hexadecimal_to_binary_s(data)
        else:hexadecimal.hexadecimal_to_binary(data)
    elif args.operation == 'h2o' or args.operation == 'hex-oct':
        if args.quiet:hexadecimal.hexadecimal_to_octal_s(data)
        else:hexadecimal.hexadecimal_to_octal(data)
    elif args.operation == 'h2d' or args.operation == 'hex-dec':
        if args.quiet:hexadecimal.hexadecimal_to_decimal_s(data)
        else:hexadecimal.hexadecimal_to_decimal(data)
    elif args.operation == 'h2t' or args.operation == 'hex-txt':
        if args.quiet:hexadecimal.hexadecimal_to_text_s()
        else:hexadecimal.hexadecimal_to_text()
    elif args.operation == 'udf' or args.operation == 'user-defined':
        if args.quiet:user_defined.udf_s()
        else:user_defined.udf()
    elif args.operation == 'udt' or args.operation == 'udef-text':
        if args.quiet:user_defined.udt_s()
        else:user_defined.udt()
    else:
        raise ValueError("Function does not exist!")
