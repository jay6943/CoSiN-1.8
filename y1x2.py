import cfg
import dxf
import dev
import tip

def device(x, y, sign):
  
  y1 = y + cfg.d1x2
  y2 = y - cfg.d1x2
  
  if sign > 0:
    x2, _ = dxf.taper('core', x, y, cfg.ltpr, cfg.wg, cfg.wtpr)
    x3, _ = dxf.srect('core', x2, y, cfg.l1x2, cfg.w1x2)
    x5, _ = dxf.taper('core', x3, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
    x5, _ = dxf.taper('core', x3, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  else:
    x2, _ = dxf.taper('core', x, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
    x2, _ = dxf.taper('core', x, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
    x3, _ = dxf.srect('core', x2, y, cfg.l1x2, cfg.w1x2)
    x5, _ = dxf.taper('core', x3, y, cfg.ltpr, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x5 - x, cfg.w1x2 + cfg.eg)
  dxf.srect('sio2', x, y, x5 - x, cfg.w1x2 + cfg.sg)

  return x5, y1, y2

def chip(x, y, lchip):

  ch, x9 = cfg.sch * 0.5, x

  idev = len(cfg.data)

  for i in range(5):
    x1, y1, y2 = device(x9, y, 1)
    x2, y3 = dev.sbend(x1, y1, 20,  ch)
    x2, y4 = dev.sbend(x1, y2, 20, -ch)
    x3, y1 = dev.sbend(x2, y3, 20, -ch)
    x3, y2 = dev.sbend(x2, y4, 20,  ch)
    x9, y1, y2 = device(x3, y, -1)
    if i < 4: x9, _ = dev.sline(x9, y, 50)
  
  x5, x6, ltip = dev.center(idev, x, x9, lchip)

  x7, t1 = tip.fiber(x5, y, ltip, -1)
  x8, t2 = tip.fiber(x6, y, ltip,  1)

  s = '1x2-' + str(round(cfg.l1x2 - cfg.dw, 1))
  dev.texts(t1, y - 50, s, 0.4, 'lc')
  dev.texts(t2, y - 50, s, 0.4, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  var = cfg.l1x2
  for cfg.l1x2 in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.l1x2 = var

  return x + cfg.size, y

if __name__ == '__main__':

  # chip(0, 0, xsize)
  
  chips(0, 0, dev.arange(16, 20, 1))

  dev.saveas(cfg.work + '1x2')