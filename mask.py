import cfg
import dxf
import dev
import key
import ohm
import pbs
import psk
import tip
import ssc
import tap
import icr
import voa
import dci
import y1x2
import y2x2
import psk2x2

# key.frame(layer, quadrant, key position)
# 'recs' layer : stress released patterns
# 'fill' layer : filled with soild
# 'none' layer : not filled

def components(x, y):

  key.frame(x, y, 1, 'fill')

  _, y1 = dev.sline(x, y + cfg.sch, cfg.size)
  _, y1 = tip.chip(x, y1 + cfg.sch, cfg.size, 0.36)
  _, y1 = ohm.chips(x, y1 + cfg.sch)
  _, y1 = y1x2.chips(x, y1 + cfg.sch, dev.arange(16, 20, 1))
  _, y1 = y2x2.chips(x, y1 + cfg.sch * 0.5, dev.arange(51, 55, 0.5))
  _, y1 = tip.chips(x, y1 + cfg.sch * 0.5, dev.arange(0.1, 0.3, 0.02))
  _, y1 = ssc.chips(x, y1 + cfg.sch, dev.arange(500, 900, 50))
  _, y1 = tap.chips(x, y1, dev.arange(31, 39, 2))
  _, y1 = dci.chips(x, y1 - cfg.sch * 0.5, dev.arange(1.8, 2.6, 0.2))
  _, y1 = tip.chip(x, y1 + cfg.sch * 1.5, cfg.size, 0.36)
  _, y1 = dev.sline(x, y1 + cfg.sch, cfg.size)

def optical_hybrid(x, y):

  key.frame(x, y, 1, 'fill')

  _, y1 = dev.sline(x, y + cfg.sch, cfg.size)
  _, y1 = tip.chip(x, y1 + cfg.sch, cfg.size, 0.36)
  _, y1 = psk2x2.chip(x, y1 + cfg.sch, cfg.size)
  _, y1 = psk.chips(x, y1 + cfg.ch, dev.arange(84, 90, 3))
  _, y1 = psk.chips(x, y1 + cfg.ch, dev.arange(90, 96, 3))
  _, y1 = psk2x2.chip(x, y1 + cfg.ch, cfg.size)
  _, y1 = voa.chips(x, y1 - cfg.sch * 2, dev.arange(200, 600, 200))
  _, y1 = tip.chip(x, y1 + cfg.sch * 5, cfg.size, 0.36)
  _, y1 = dev.sline(x, y1 + cfg.sch, cfg.size)

  dxf.seperation('gold', 0, -cfg.mask)

def polarization_splitter(x, y):

  key.frame(x, y, 1, 'fill')

  _, y1 = dev.sline(x, y + cfg.sch, cfg.size)
  _, y1 = tip.chip(x, y1 + cfg.sch, cfg.size, 0.36)
  _, y1 = pbs.chips(x, y1 + cfg.sch, dev.arange(10, 50, 2))
  _, y1 = dev.sline(x, y1 + cfg.sch * 2, cfg.size)

def coherent_receiver(x, y):

  key.frame(x, y, 1, 'fill')

  icr.chips(x, y + cfg.size * 0.5)

def align_key(x, y):

  key.frame(x, y, 1, 'none')

  key.contact_align_keys('core', x, y, 1)

if __name__ == '__main__':

  cfg.draft = 'draft' # draft or mask

  x = key.wbar + key.wkey
  y = key.wbar + key.wkey

  key.cross(0, 0)

  ok = 0
  
  if ok == 0 or ok == 1: components(x - cfg.mask, y)
  if ok == 0 or ok == 2: optical_hybrid(x, y)
  if ok == 0 or ok == 3: polarization_splitter(x - cfg.mask, y - cfg.mask)
  if ok == 0 or ok == 4: align_key(x, y - cfg.mask)
  
  dev.saveas(cfg.work + cfg.draft)
