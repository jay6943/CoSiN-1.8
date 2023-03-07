import cfg
import dev
import tip
import numpy as np

def device(x, y, angle, dy, sign):

  arg = np.abs(angle - cfg.targ)

  x1, y1 = x, y - dy
  x2, y2 = dev.bends(x1, y1, arg, angle * 3, -1, -sign)

  l = (dy - y2 + y1) / np.sin(cfg.targ * np.pi / 180)

  x3, y3 = dev.tilts(x2, y2, -l, cfg.wg, -cfg.targ)
  x4, y4 = dev.sline(x3, y, x1 - x3)

  return x4, y4

def chip(x, y, lchip):

  idev = len(cfg.data)
  # x1, _ = device(x, y, 90, cfg.ch, 1)
  x1, _ = device(x, y, 0, cfg.sch, -1)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y, ltip, -1)
  x8, t2 = tip.fiber(x6, y - cfg.sch, ltip, 1)
  x8, t2 = tip.fiber(x6, y, ltip, 1)

  s = 'TAP-' + str(round(cfg.targ, 1))
  dev.texts(t1, y - cfg.sch * 0.5, s, 0.4, 'lc')
  dev.texts(t2, y - cfg.sch * 0.5, s, 0.4, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  var = cfg.targ
  for cfg.targ in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.targ = var

  return x + cfg.size, y

if __name__ == '__main__':
  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(33, 37, 1))

  dev.saveas(cfg.work + 'tap')