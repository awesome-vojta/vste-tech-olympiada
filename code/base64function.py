import base64

def toBase64(s):
	return base64.b64encode(str(s))
	
def fromBase64(s):
	return base64.b64decode(str(s))
