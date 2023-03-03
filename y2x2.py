import cfg
import dxf
import dev
import tip

def device(x, y):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x1, _ = dxf.srect('core', x, y1, 50 - cfg.ltpr * 2, cfg.wg)
  x1, _ = dxf.srect('core', x, y2, 50 - cfg.ltpr * 2, cfg.wg)
  x2, _ = dxf.taper('core', x1, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
  x2, _ = dxf.taper('core', x1, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
  x3, _ = dxf.srect('core', x2, y, cfg.l2x2, cfg.w2x2)
  x4, _ = dxf.taper('core', x3, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
  x4, _ = dxf.taper('core', x3, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  x5, _ = dxf.srect('core', x4, y1, 50 - cfg.ltpr * 2, cfg.wg)
  x5, _ = dxf.srect('core', x4, y2, 50 - cfg.ltpr * 2, cfg.wg)

  dxf.srect('edge', x, y, x5 - x, cfg.w2x2 + cfg.eg)
  dxf.srect('sio2', x, y, x5 - x, cfg.w2x2 + cfg.sg)

  return x5, y1, y2

def chip(x, y, lchip):

  ch = 50
  dh = ch - cfg.d2x2

  y1 = y + ch
  y2 = y - ch
  
  idev = len(cfg.data)

  x1, y1 = dev.sbend(x, y1, 20, -dh)
  x1, y2 = dev.sbend(x, y2, 20,  dh)
  x2, y3, y4 = device(x1, y)
  x3, y1 = dev.sbend(x2, y3, 20,  dh)
  x3, y2 = dev.sbend(x2, y4, 20, -dh)
  
  x5, x6, ltip = dev.center(idev, x, x3, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = '2x2-' + str(round(cfg.l2x2, 1))
  dev.texts(t1, y, s, 0.4, 'lc')
  dev.texts(t2, y, s, 0.4, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  var = cfg.l2x2
  for cfg.l2x2 in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.l2x2 = var

  return x + cfg.size, y + cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(49, 53, 1))

  dev.saveas(cfg.work + '2x2')