import teplotaEspdriver

def getEspteplota():
    global teplota
    try:
        teplota = teplotaEspdriver.readEsp()
        return True
    except:
        return False

Esp = getEspteplota(teplota)
print(Esp)