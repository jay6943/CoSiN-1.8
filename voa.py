import cfg
import dev
import tip
import pad
import y1x2

def arm(x, y, sign):

  x1, y = dev.srect(x, y, cfg.lvoa, cfg.wg)
  
  pad.electrode('gold', x, y, cfg.lvoa, cfg.wg + 2, sign)
  pad.electrode('edge', x, y, cfg.lvoa, cfg.eg, sign)

  return x1, y

def device(x, y):

  ch = cfg.ch * 0.5

  x2, y1, y2 = y1x2.device(x, y, 1)

  x3, y3 = dev.sbend(x2, y1, 45,  ch)
  x3, y4 = dev.sbend(x2, y2, 45, -ch)

  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)

  x9, y1 = dev.sbend(x5, y3, 45, -ch)
  x9, y2 = dev.sbend(x5, y4, 45,  ch)

  x10, y1, y2 = y1x2.device(x9, y, -1)

  return x10, y

def chip(x, y, lchip):

  ch = cfg.ch * 0.5
  dl = 2000 + (cfg.lvoa - 200) * 10

  x1, t1 = tip.fiber(x + dl, y, dl, -1)
  x2, _ = device(x1 + dl, y)
  x8, t2 = tip.fiber(x2, y, x + cfg.size - x2,  1)

  s = 'VOA-' + str(round(cfg.lvoa))
  dev.texts(t1, y + ch, s, 0.4, 'lc')
  dev.texts(t1, y - ch, s, 0.4, 'lc')
  dev.texts(t2, y + ch, s, 0.4, 'rc')
  dev.texts(t2, y - ch, s, 0.4, 'rc')

  print(s, round(x2 - x1), round(x8 - x))

  return x + lchip, y

def chips(x, y, arange):

  var = cfg.lvoa
  for cfg.lvoa in arange: _, y = chip(x, y + cfg.ch * 2, cfg.size)
  cfg.lvoa = var

  return x + cfg.size, y

if __name__ == '__main__':

  # chip(0, 0, 2000)
  
  chips(0, 0, dev.arange(200, 500, 100))

  dev.saveas(cfg.work + 'voa')