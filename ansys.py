import cfg
import dxf
import dev
import elr

l = 10

def angle_45(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.sbend(x, y, 45, 0)
  x, y = dev.sline(x, y, l)

  dev.saveas(filename)

def angle_90(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.bends(x, y, 90, 0, 1, 1)
  x, y = dev.tline(x, y, l)

  dev.saveas(filename)

def angle_180(filename, wg):

  s1 = elr.update(wg, cfg.radius, 180)

  x1, y1 = dxf.srect('core', 0, 0, l, wg)
  x2, y2 = dxf.bends('core', x1, y1, s1, 0, 1, 1)
  x3, y3 = dxf.srect('core', x2, y2, -l, wg)

  dev.saveas(filename)

def angle_90x2(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.bends(x, y, 90, 0, 1, 1)
  x, y = dev.tline(x, y, l)
  x, y = dev.bends(x, y, 90, 90, 1, 1)
  x, y = dev.sline(x, y, -l)

  dev.saveas(filename)

def sbend(folder):

  cfg.draft = 'mask'

  wg, radius, angle, dy = 1.2, 10, 25, 1

  df = elr.update(wg, radius, angle)

  dxf.sbend('core', 0, 0, df, angle, -dy)
  dev.saveas(folder + str(wg) + '-1')

  dxf.sbend('core', 0, 0, df, angle, dy)
  dev.saveas(folder + str(wg) + '-2')

def dc(folder):

  cfg.draft = 'mask'

  radius, angle, dy = 50, 3, 1

  for i in range(7):
    wg = round(0.37 + i * 0.01, 2)

    df = elr.update(wg, radius, angle)
    rf = elr.update(wg, radius, 20)

    x1, _ = dxf.sbend('core', 0, 0, df, angle, -dy)
    dev.saveas(folder + str(wg) + '-1')

    x1, _ = dxf.sbend('core', 0, 0, df, angle, dy)
    dev.saveas(folder + str(wg) + '-2')

    x2, y2 = dxf.bends('core', x1, 0, rf, 0, -1, 1)
    dev.saveas(folder + str(wg) + '-3')

  return x2, y2

import pbs

def pbs_in(x, y, angle, dy):

  core = elr.update(cfg.wg, cfg.radius, angle)

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x1, _ = dxf.srect('core', x, y2, 20, cfg.wg)
  x1, _ = dxf.taper('core', x1, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)

  pbs.tail(x1 - 5, y + cfg.d2x2, 90, 90, -1, 1)

  x3, _ = dxf.taper('core', x2, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
  x3, _ = dxf.taper('core', x2, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  x4, y3 = dxf.sbend('core', x3, y1, core, angle,  dy)
  x4, y4 = dxf.sbend('core', x3, y2, core, angle, -dy)

  x5, y3 = dxf.taper('core', x4, y3, cfg.ltpr, cfg.wg, cfg.wpbs)
  x5, y4 = dxf.taper('core', x4, y4, cfg.ltpr, cfg.wg, cfg.wpbs)

  x6, y3 = dxf.srect('core', x5, y3, 10, cfg.wpbs)
  x6, y4 = dxf.srect('core', x5, y4, 10, cfg.wpbs)
  
  return x6, y
  
def pbs_out(x, y, angle, dy):

  core = elr.update(cfg.wg, cfg.radius, angle)

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x5, _ = dxf.sbend('core', x, y1 + dy, core, angle, -dy)
  x5, _ = dxf.sbend('core', x, y2 - dy, core, angle,  dy)
  x6, _ = dxf.taper('core', x5, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
  x6, _ = dxf.taper('core', x5, y2, cfg.ltpr, cfg.wg, cfg.wtpr)

  x6, _ = dxf.srect('core', x6, y, cfg.l2x2, cfg.w2x2)

  angle, dy = 2, 1
  core = elr.update(cfg.wg, cfg.radius, angle)
  x8, y3 = dxf.sbend('core', x6, y1, core, angle,  dy)
  x8, y4 = dxf.sbend('core', x6, y2, core, angle, -dy)

  x9, y3 = dxf.srect('core', x8, y3, 10, cfg.wg)
  x9, y4 = dxf.srect('core', x8, y4, 10, cfg.wg)

  return x9, y

def pbs_mzi(folder):

  cfg.draft = 'mask'

  angle, dy = 2, 1

  pbs_in(-10, 0, angle, dy)
  dev.saveas(folder + 'mmi-in')

  pbs_out(0, 0, angle, dy)
  dev.saveas(folder + 'mmi-out')

if __name__ == '__main__':

  cfg.draft = 'mask'

  # angle_45('D:/ansys/Euler/45')
  # angle_90('D:/ansys/Euler/90')
  angle_180('D:/Git/mask/SiN-1.8/180-0.8w-' + str(cfg.radius) + 'R', cfg.wg)
  # angle_90x2('D:/ansys/Euler/90x2')
  # sbend('D:/ansys/tap/')
  # dc('D:/ansys/tap/')
  # pbs_mzi('D:/ansys/PBS/')
