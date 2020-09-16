def entrypoint(argv):
    assert argv[0] == 'message'
    assert argv[1] is not None
    str_name = "This is an operation in mesapy_printf_payload.py: " + argv[1]
    return str_name
    #return argv[1]
