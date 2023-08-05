# ÜberLimb

Generative art with CPPN networks.

# Get started
Install package with `pip install uberlimb[runtime]`

```python
from uberlimb.renderer import Renderer
from uberlimb.parameters import RendererParams

renderer = Renderer(RendererParams())
renderer.render_frame().as_pillow().show()
```

Expected output:

![](https://cai-misc.s3.eu-central-1.amazonaws.com/uberlimb/uberlimb_splash.png)

# TODO
- [ ] video pipeline
- [ ] color schemes, both predefined and custom (will require varying
  the number of output channels)