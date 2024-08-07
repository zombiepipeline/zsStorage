import imp

try:
    import transferShader
    imp.reload(transferShader)
except Exception as error:
    print(error)