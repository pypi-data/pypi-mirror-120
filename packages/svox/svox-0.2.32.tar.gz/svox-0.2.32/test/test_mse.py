import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt
import torch.autograd as ag

device = 'cuda:0'

t = svox.N3Tree(device=device, data_format="SH1")
t[0, 0, 0] = torch.tensor([0, 0, 0.0, 0.5], device=device)
r = svox.VolumeRenderer(t, step_size=1e-5, background_brightness=0)
target =  torch.tensor([[0.0, 1.0, 0.5]], device=device)

ray_ori = torch.tensor([[0.1, 0.1, -0.1]], device=device)
ray_dir = torch.tensor([[0.0, 0.0, 1.0]], device=device)
ray = svox.Rays(origins=ray_ori, dirs=ray_dir, viewdirs=ray_dir)

with torch.no_grad():
    for i in range(1):
        rend, grad, hessdiag = r.se_grad(ray, target)
        #  if i % 2 == 0:
        print(i)
        print('rendered color:', rend.detach()[0].cpu().numpy())
        print('gradient:', grad[0, 0, 0, 0])
        print('hessian diagonal:', hessdiag[0, 0, 0, 0])
        print('values:', t.data.data[0, 0, 0, 0])
        #  t.data.data[..., :-1] -= 1e2 * grad[..., :-1]
        #  print(grad[0, 0, 0, 0, -1], hessdiag[0, 0, 0, 0, -1])
        hessdiag += 1e-20
        tr_radius = 5
        grad /= hessdiag
        grad.clamp_(-tr_radius, tr_radius)

        #  delta = 1e2 * grad[..., -1]

        #  print('step:', delta[0, 0, 0, 0])
        #  mask = hessdiag == 0
        #  delta[mask] = 0.0
        #  delta[..., :-1].clamp_max_(0.1)
        #  delta[..., -1].clamp_max_(1)
        #  print(delta)
        t.data.data -= grad
        #  t.data.data[..., -1] -= delta
        #  print(t.data)

print('TARGET')
print(target[0].cpu().numpy())

#  c2w = torch.tensor([[1.0, 0.0, 0.0,  0.0],
#                      [0.0, 1.0, 0.0,  0.0],
#                      [0.0,  0.0, 1.0, 0.0]], device=device)
#
#
#
#  start = torch.cuda.Event(enable_timing=True)
#  end = torch.cuda.Event(enable_timing=True)
#  im = None
#
#  start.record()
#  im = r.render_persp(c2w, height=400, width=400, fx=300)
#  end.record()
#
#  torch.cuda.synchronize(device)
#  dur = start.elapsed_time(end)
#  print('render time', dur, 'ms =', 1000 / dur, 'fps')
#  print(im.shape)
#
#  im = im.detach().clamp_(0.0, 1.0)
#  plt.figure()
#  plt.imshow(im.cpu())
#  plt.show()
