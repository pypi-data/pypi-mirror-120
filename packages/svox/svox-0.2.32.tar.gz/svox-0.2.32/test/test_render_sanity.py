import torch
import svox
device = 'cuda:0'

def fn(SW):
    if SW:
        t = svox.N3Tree(map_location=device,
            data_dim=4 * 3 + 1, data_format="SH4")
        t[0, 0, 0, 0] = 0.25
        t[0, 0, 0, 4] = -0.5
        t[0, 0, 0, 8] = 0.8
    else:
        t = svox.N3Tree(map_location=device,
                 data_dim=1 * 3 + 1, data_format="SH1")
        t[0, 0, 0, 0] = 0.25
        t[0, 0, 0, 1] = -0.5
        t[0, 0, 0, 2] = 0.8
    t[0, 0, 0, -1:] = 0.5
    r = svox.VolumeRenderer(t)

    ray_ori = torch.tensor([[0.1, 0.1, -0.1]], device=device)
    ray_dir = torch.tensor([[0.0, 0.0, 1.0]], device=device)
    ray = svox.Rays(origins=ray_ori, dirs=ray_dir, viewdirs=ray_dir)


    if SW:
        t[:, 1:4] = 0
        t[:, 5:8] = 0
        t[:, 9:12] = 0
    rend = r(ray, cuda=True)
    print(rend.detach().cpu().numpy())
    rend.sum().backward()


    print(t.data.grad)

    #  0.8907684 0.8907684 0.8907684

fn(True)
fn(False)
