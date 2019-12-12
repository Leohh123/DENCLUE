from reader import Reader
from denclue2D import Denclue2D, H, K, DELTA, XI
from renderer import Renderer
import json

if __name__ == "__main__":
    for i in range(1, 17):
        r = Reader("data/%d.in" % i)
        x, y = r.read()
        dc = Denclue2D(x, y)
        dc.work()
        dc.render_dens_fig("output/dens_fig/%d.png" % i)
        cnt, bel = dc.get_result()
        with open("output/numeric/%d.json" % i, "w") as f:
            config = {"h": H, "k": K, "delta": DELTA, "xi": XI}
            f.write(json.dumps({"config": config, "cnt": cnt, "bel": bel}))
        rd = Renderer(x, y, cnt, bel)
        rd.render("output/cluster_fig/%d.png" % i)
