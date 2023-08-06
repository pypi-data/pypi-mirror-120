import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt

device = 'cuda:0'

t = svox.N3Tree(device=device,
         data_dim=1 * 3 + 1, data_format="SH1")
#  t[0, 0, 0, :-1] = 0.0
#  t[0, 0, 0, -1:] = 0.5
t[0, 0, 0] = torch.tensor([0, 0, 0.0, 0.5], device=device)
r = svox.VolumeRenderer(t, step_size=1e-5, background_brightness=1)
print(t)
#  sqrt_2 = 2 ** -0.5

#  ray_ori = torch.tensor([[0.1, 0.1, -0.1],
#                          [0.9, 0.9, -0.1]], device=device)
#  ray_dir = torch.tensor([[0.0, 0.0, 1.0],
#                          [0.0, 0.0, 1.0]], device=device)

target =  torch.tensor([[0.0, 1.0, 0.5]], device=device)

ray_ori = torch.tensor([[0.1, 0.1, -0.1]], device=device)
ray_dir = torch.tensor([[0.0, 0.0, 1.0]], device=device)
ray = svox.Rays(origins=ray_ori, dirs=ray_dir, viewdirs=ray_dir)
cuda = True
print('cuda?', cuda)
print('GRADIENT DESC')
for i in range(1):
    rend = r(ray, cuda=cuda)
    #  if i % 2 == 0:
    print(rend.detach()[0].cpu().numpy())
    #  rend.retain_grad()
    (0.5 * ((rend - target) ** 2).sum()).backward()
    #  print('rend grad', rend.grad)
    #  print('data grad', t.data.grad)
    #  print('data', t.data)

    print('grad:', t.data.grad[0, 0, 0, 0])
    #  print(t.data.data[0, 0, 0, 0])
    t.data.data -= 1e2 * t.data.grad
    #  print(t.data)
    t.zero_grad()

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
