import cfg
import dev
import tip

def chip(x, y, lchip, dy):

  ch = cfg.sch * 0.5

  y1 = y + ch
  y2 = y - ch
  
  idev = len(cfg.data)

  x1, y3 = dev.sbend(x, y1, 20, dy * 0.5 - ch)
  x1, y4 = dev.sbend(x, y2, 20, ch - dy * 0.5)
  x3, y1 = dev.sbend(x1, y3, 20, ch - dy * 0.5)
  x3, y2 = dev.sbend(x1, y4, 20, dy * 0.5 - ch)

  x5, x6, ltip = dev.center(idev, x, x3, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'DC-' + str(round(dy, 1))
  dev.texts(t1, y, s, 0.4, 'lc')
  dev.texts(t2, y, s, 0.4, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  for dy in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size, dy)

  return x + cfg.size, y

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(1.2, 3.2, 0.2))

  dev.saveas(cfg.work + 'dc')