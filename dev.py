import os
import cfg
import dxf
import elr

def srect(x, y, length, width):

  x1, y1 = dxf.srect('edge', x, y, length, cfg.eg)
  x1, y1 = dxf.srect('core', x, y, length, width)
  x1, y1 = dxf.srect('sio2', x, y, length, cfg.sg)

  return x1, y1

def sline(x, y, length):

  x1, y1 = dxf.srect('edge', x, y, length, cfg.eg)
  x1, y1 = dxf.srect('core', x, y, length, cfg.wg)
  x1, y1 = dxf.srect('sio2', x, y, length, cfg.sg)

  return x1, y1

def tline(x, y, length):

  w = cfg.wg * 0.5
  d = cfg.eg * 0.5
  s = cfg.sg * 0.5

  x1, y1 = dxf.crect('edge', x - d, y, x + d, y + length)
  x1, y1 = dxf.crect('core', x - w, y, x + w, y + length)
  x1, y1 = dxf.crect('sio2', x - s, y, x + s, y + length)

  return x1 - w, y1

def tilts(x, y, length, wg, angle):

  x1, y1 = dxf.tilts('edge', x, y, length, cfg.eg, angle)
  x1, y1 = dxf.tilts('core', x, y, length, wg, angle)
  x1, y1 = dxf.tilts('sio2', x, y, length, cfg.sg, angle)

  return x1, y1

def taper(x, y, length, wstart, wstop):

  x1, y1 = dxf.srect('edge', x, y, length, cfg.eg)
  x1, y1 = dxf.taper('core', x, y, length, wstart, wstop)
  x1, y1 = dxf.srect('sio2', x, y, length, cfg.sg)

  return x1, y1

def bends(x, y, angle, rotate, xsign, ysign):

  core = elr.update(cfg.wg, cfg.radius, angle)
  edge = elr.update(cfg.eg, cfg.radius, angle)
  sio2 = elr.update(cfg.sg, cfg.radius, angle)

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, xsign, ysign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)
  x1, y1 = dxf.bends('sio2', x, y, sio2, rotate, xsign, ysign)

  return x1, y1

def sbend(x, y, angle, dy):

  core = elr.update(cfg.wg, cfg.radius, angle)
  edge = elr.update(cfg.eg, cfg.radius, angle)
  sio2 = elr.update(cfg.sg, cfg.radius, angle)

  x1, y1 = dxf.sbend('edge', x, y, edge, angle, dy)
  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def texts(x, y, title, scale, align):

  d = 10 * scale * 2  # 10 when scale = 0.5

  if align[0] == 'l': x = x + d
  if align[0] == 'r': x = x - d

  l, w = dxf.texts('core', x, y, title.lower(), scale, align)

  xalign = x - l * 0.5 - d

  if align[0] == 'l': xalign = x - d
  if align[0] == 'r': xalign = x - l - d

  dxf.srect('edge', xalign, y, l + d * 2, w + d * 2)

def arange(start, stop, step):

  addvar, var = [], start

  while var < stop + step * 0.5:
    addvar.append(var)
    var = var + step

  if len(addvar) < 1: print('No any element')

  return addvar

def center(idev, x, xt, lchip):

  ldev = xt - x
  ltip = (lchip - ldev) * 0.5

  xt, _ = dxf.move(idev, x, 0, xt, 0, ltip, 0, 0)

  return xt - ldev, xt, xt - ldev - x

def removes(folder):

  if os.path.isdir(folder):

    files = os.listdir(folder)

    for fp in files:
      if os.path.exists(folder + fp): os.remove(folder + fp)

    os.rmdir(folder)

def saveas(filename):

  fp = dxf.start(filename)
  dxf.conversion(fp)
  dxf.close(fp)

if __name__ == '__main__':

  sbend(0, 0, 45, 100)

  saveas(cfg.work + 'sbend')