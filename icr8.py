import cfg
import dev
import pbs
import voa
import psk
import tip

yqpsk = cfg.ch * 2

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)

  x2, y1 = voa.device(x, y + cfg.ch)
  x3, y2 = dev.sline(x, y - cfg.ch, x2 - x)

  x4, y41, y42 = pbs.device(x3, y1)
  x4, y43, y44 = pbs.device(x3, y2)

  h = [y + ch * (i * 2 - 7) for i in range(8)]

  x1, y71 = dev.sbend(x4, y41, 45, h[6] - y41)
  x1, y74 = dev.sbend(x4, y44, 45, h[1] - y44)
  x2, y72 = dev.sbend(x4, y42, 45, h[2] - y42)
  x2, y73 = dev.sbend(x4, y43, 45, h[5] - y43)

  x9, _ = dev.sline(x1, y71, x2 - x1)
  x9, _ = dev.sline(x1, y74, x2 - x1)

  x10, _ = psk.device(x9, y + yqpsk)
  x10, _ = psk.device(x9, y - yqpsk)

  x11, x12, ltip = dev.center(idev, x, x10, lchip)

  x13, _ = tip.fiber(x11, y1, ltip, -1)
  x13, _ = tip.fiber(x11, y2, ltip, -1)

  for i in h: x14, _ = tip.diode(x12, i, ltip, 1)

  print('DP-QPSK', round(x12 - x11), round(x14 - x13))

  return x + lchip, y

if __name__ == '__main__':

  chip(0, 0, cfg.size)

  dev.saveas(cfg.work + '8ch')