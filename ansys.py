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

  wg, radius, angle, dy = cfg.wg, 10, 25, 4

  df = elr.update(wg, radius, angle)

  dxf.sbend('core', 0, 0, df, angle, -dy)
  dev.saveas(folder + str(wg) + '-1')

  dxf.sbend('core', 0, 0, df, angle, dy)
  dev.saveas(folder + str(wg) + '-2')

def sbend_in_out(folder):

  cfg.draft = 'mask'

  angle, dy = 5, 4

  df = elr.update(cfg.wg, cfg.radius, angle)

  x1, y1 = 0, -dy
  x2, y2 = dxf.sline('core', x1, y1, 10)
  x3, y3 = dxf.sbend('core', x2, y2, df, angle,  dy)
  x4, y4 = dxf.sbend('core', x3, y3, df, angle, -dy)
  x5, y5 = dxf.sline('core', x4, y4, 10)
  dev.saveas(folder + 'sbend')

  return x5, y5

def dc(folder):

  cfg.draft = 'mask'

  radius, angle, dy = cfg.radius, 3, 2

  for i in range(1):
    wg = round(0.8 + i * 0.01, 2)

    df = elr.update(wg, radius, angle)
    rf = elr.update(wg, radius, 20)

    x1, _ = dxf.sbend('core', 0, 0, df, angle, -dy)
    dev.saveas(folder + str(wg) + '-1')

    x1, _ = dxf.sbend('core', 0, 0, df, angle, dy)
    dev.saveas(folder + str(wg) + '-2')

    x2, y2 = dxf.bends('core', x1, 0, rf, 0, -1, 1)
    dev.saveas(folder + str(wg) + '-3')

  return x2, y2

if __name__ == '__main__':

  cfg.draft = 'mask'

  # angle_45('D:/ansys/Euler/45')
  # angle_90('D:/ansys/Euler/90')
  # angle_180('D:/Git/mask/SiN-1.8/180-0.8w-' + str(cfg.radius) + 'R', cfg.wg)
  # angle_90x2('D:/ansys/Euler/90x2')
  # sbend_in_out('D:/ansys/tap/')
  dc('D:/ansys/DC/')
