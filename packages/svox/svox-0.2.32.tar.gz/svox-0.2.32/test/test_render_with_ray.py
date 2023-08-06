import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt
import numpy as np

device = 'cuda:0'

t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lowcost/lego.npz",
#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/nerf_synthetic_v2/ship_v2.npz",
#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/mic_sg_sp.npz",
                      device=device)
#  t = svox.N3Tree(map_location=device)
#  t.expand("SH16")
r = svox.VolumeRenderer(t)
print(t)
c2w = torch.tensor([
                [ -0.9999999403953552, 0.0, 0.0, 0.0 ],
                [ 0.0, -0.7341099977493286, 0.6790305972099304, 2.737260103225708 ],
                [ 0.0, 0.6790306568145752, 0.7341098785400391, 2.959291696548462 ],
                [ 0.0, 0.0, 0.0, 1.0 ],
            ], device=device)

with torch.no_grad():
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    width = height = 800
    fx = fy = 1111
    origins = c2w[None, :3, 3].expand(height * width, -1).contiguous()
    yy, xx = torch.meshgrid(
        torch.arange(height, dtype=torch.float64, device=c2w.device),
        torch.arange(width, dtype=torch.float64, device=c2w.device),
    )
    xx = (xx - width * 0.5) / float(fx)
    yy = (yy - height * 0.5) / float(fy)
    zz = torch.ones_like(xx)
    dirs = torch.stack((xx, -yy, -zz), dim=-1)
    dirs /= torch.norm(dirs, dim=-1, keepdim=True)
    dirs = dirs.reshape(-1, 3)
    del xx, yy, zz
    dirs = torch.matmul(c2w[None, :3, :3].double(), dirs[..., None])[..., 0].float()
    #  vdirs = dirs
    vdirs = dirs / torch.norm(dirs, dim=-1, keepdim=True)
    vdirs = vdirs.float()

    rays = svox.Rays(
        origins=origins,
        dirs=dirs,
        viewdirs=vdirs
    )

    im = None
    #  start.record()
    #  for i in range(5):
    im = r(rays)
    im_persp = r.render_persp(c2w, height=800, width=800, fx=1111)
    #  end.record()

    torch.cuda.synchronize(device)
    #  dur = start.elapsed_time(end) / 5
    #  print('render time', dur, 'ms =', 1000 / dur, 'fps')

    im = im.view(height, width, 3)
    print(im.shape, im_persp.shape)

    im = im.detach().clamp_(0.0, 1.0).cpu()
    im_persp = im_persp.detach().clamp_(0.0, 1.0).cpu()
    errmap = torch.abs(im - im_persp)
    print(im.max(), (errmap > 1e-2).sum(), errmap.max(), 'err')
    print((errmap > 1e-2).nonzero(as_tuple=False))

    plt.figure()
    plt.subplot(1, 3, 1)
    plt.imshow(im)
    plt.subplot(1, 3, 2)
    plt.imshow(im_persp)
    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(im - im_persp))
    plt.show()
