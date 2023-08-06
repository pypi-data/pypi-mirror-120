import svox
import torch
import torch.cuda
import torch.autograd as ag
import matplotlib.pyplot as plt

device = 'cuda:0'

t = svox.N3Tree(device=device,
         data_dim=1 * 3 + 1, data_format="SH1")
t = t.double()
r = svox.VolumeRenderer(t, background_brightness=0)
print(t)
#  sqrt_2 = 2 ** -0.5

#  ray_ori = torch.tensor([[0.1, 0.1, -0.1],
#                          [0.9, 0.9, -0.1]], device=device)
#  ray_dir = torch.tensor([[0.0, 0.0, 1.0],
#                          [0.0, 0.0, 1.0]], device=device)

target =  torch.tensor([[0.0, 1.0, 0.5]], device=device).double()

ray_ori = torch.tensor([[0.1, 0.1, -0.1]], device=device).double()
ray_dir = torch.tensor([[0.0, 0.0, 1.0]], device=device).double()
ray = svox.Rays(origins=ray_ori, dirs=ray_dir, viewdirs=ray_dir)
print('GRADIENT DESC')

def reset():
    t[0, 0, 0, :-1] = 0.0
    t[0, 0, 0, -1:] = 0.5
reset()

step = 1e-10
def grad_comp():
    #  t[0, 0, 0, j] += step * nstep
    rend = r(ray, cuda=False)[0]
    grads = []
    for i in range(rend.shape[0]):
        grad = torch.autograd.grad(rend[i], t.data, create_graph=True)[0]
        grads.append(grad)
    grads = torch.stack(grads)
    print(grads.shape)
    print(grads)
    #  reset()
    #  return grad

for i in range(1):
    grad_gt = grad_comp()
    #  print(grad_gt)

    #  rend, grad, hessdiag = r.mse_grad(ray, target)
    #  print(hessdiag)

    #  if i % 2 == 0:
    #      print(rend.detach()[0].cpu().numpy())
    #  rend.retain_grad()
    #  .backward()
    #  print('rend grad', rend.grad)
    #  print('data grad', t.data.grad)
    #  print('data', t.data)

    #  print(t.data.grad[0, 0, 0, 0])
    #  t.data.data -= 1e2 * t.data.grad
    #  print(t.data)
    #  t.zero_grad()

#  print('TARGET')
#  print(target[0].cpu().numpy())

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
