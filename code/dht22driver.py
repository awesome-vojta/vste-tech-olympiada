import dhtreader

def read(pin):
  i = 0
  while i<10:
    try:
      dhtreader.init()
      t, h = dhtreader.read(22, pin)
      if t and h:
          t = float("{0:.2f}".format(t))
          h = float("{0:.2f}".format(h))
          return t, h, True
    finally:
      i = i + 1
  return False
