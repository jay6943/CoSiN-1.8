import cfg
import dxf
import dev
import key
import mask
import numpy as np

radius = 150 * 0.5 * 1000
size = key.wkey + cfg.size
rmax = radius + 5000

def wafer(x, y):
  
  a = np.linspace(-70, 250, 81) * np.pi / 180
  
  xp = x + radius * np.cos(a)
  yp = y + radius * np.sin(a)

  data = np.array([xp, yp]).transpose()
  cfg.data.append(['edge'] + data.tolist())

  t = 4000

  dxf.crect('fill', x - rmax, y - rmax, t - rmax, t - rmax)
  dxf.crect('fill', x - rmax, y + rmax, t - rmax, rmax - t)
  dxf.crect('fill', x + rmax, y - rmax, rmax - t, t - rmax)
  dxf.crect('fill', x + rmax, y + rmax, rmax - t, rmax - t)

def cells(x, y, n, title):

  cs = cfg.size * 0.5
  dy = cs + key.wkey

  for i in range(n):
    dx = size * (i - n * 0.5) + 200
    key.bars(x + dx - key.wkey, y)
    dxf.srect('recs', x + dx, y + dy, cfg.size, cfg.size)
    dxf.texts('text', x + dx + cs, y + cs, title, 40, 'cc')

def tooling(x, y):

  fp = cfg.work + 'wafer'

  for i in range(11):
    j = i % 4 + 1
    n = 10 if i % 10 else 8
    dx = size * (i - 5)
    dy = dx - size * 0.5

    if j != 4: cells(x, y + dy, n, '0' + str(i % 4 + 1))
    else: mask.align_key(x + key.wkey, y + dy + key.wkey)
    
    dxf.srect('cuts', x + dx, y, 10, rmax * 2)
  
  dxf.srect('cuts', x - rmax, y + size * 6, rmax * 2, 10)
  dxf.srect('cuts', x - rmax, y + size * 2, rmax * 2, 10)
  dxf.srect('cuts', x - rmax, y - size * 2, rmax * 2, 10)
  dxf.srect('cuts', x - rmax, y - size * 6, rmax * 2, 10)

  wafer(0, 0)

  dev.saveas(fp)

if __name__ == '__main__': tooling(0, 0)