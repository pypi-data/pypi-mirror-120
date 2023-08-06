import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt
print(svox.__version__)

device = 'cuda:0'

#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lego_diffscale.npz",
#  t = svox.N3Tree.load("quant_exp_16.npz",
t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lowcost/mic.npz",
#  t = svox.N3Tree.load("/f/fastnerf/oct/misc/mic_sg_sp.npz",
                      device=device)
print(t.data_format)
#  t.expand("SH16")
#  print(t.data_format)
#  t = svox.N3Tree(map_location=device)
r = svox.VolumeRenderer(t, density_softplus=False, rgb_padding=0.001)
print(t)
#  t.shrink_to_fit()
#  print(t)

#  t.save("tmp.npz", compress=True, strip=True)
c2w = torch.tensor([
                [ -0.9999999403953552, 0.0, 0.0, 0.0 ],
                [ 0.0, -0.7341099977493286, 0.6790305972099304, 2.737260103225708 ],
                [ 0.0, 0.6790306568145752, 0.7341098785400391, 2.959291696548462 ],
                [ 0.0, 0.0, 0.0, 1.0 ],
            ], device=device)

with torch.no_grad():
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    im = None
    start.record()
    #  with t.accumulate_weights(op='sum') as accum:
    cols = torch.zeros((800, 800, 3), device=device)
    for i in range(5):
        #  im = r.render_persp(c2w, height=800, width=800, fx=1111, cuda=True, fast=True)
        #  (0.5 * ((im - cols)**2).sum()).backward()
        im, grad, hess = r.se_grad_persp(c2w, cols, height=800, width=800, fx=1111)
        #  im = r.render_persp(c2w, height=800, width=800, fx=1111, cuda=True, fast=True)
    #  accum = accum()
    #  print(accum.max())
    end.record()

    torch.cuda.synchronize(device)
    dur = start.elapsed_time(end) / 5
    print('render time', dur, 'ms =', 1000 / dur, 'fps')
    print(im.shape)

    im = im.detach().clamp_(0.0, 1.0)
    plt.figure()
    plt.imshow(im.cpu())
    plt.show()



