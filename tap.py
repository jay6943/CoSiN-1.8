import cfg
import dxf
import dev
import tip

def device(x, y):

  x5, _ = dev.sline(x, y, 200)

  x8, y8 = dev.taper(x5, y, cfg.ltpr, cfg.wg, 0.1)

  return x5, x8, y8

def chip(x, y, lchip):
  
  ch = cfg.sch * 0.5

  y1 = y + ch
  y2 = y - ch
  y3 = y1 + cfg.spacing - cfg.tapping

  idev = len(cfg.data)

  x1, _ = dev.sline(x, y, 100)

  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'tap-' + str(round(cfg.tapping, 2))
  dev.texts(t1, y, s, 0.4, 'lc')
  dev.texts(t2, y, s, 0.4, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  var = cfg.tapping
  for cfg.tapping in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.tapping = var

  return x + cfg.size, y + cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(2.4, 2.7, 0.1))

  dev.saveas(cfg.work + 'tap')