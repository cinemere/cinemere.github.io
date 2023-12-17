import plotly.express as px
import pandas as pd
import numpy as np
import io
import os
import PIL

SAVEDIR="blog/2023/probs"

r = np.random.RandomState(42)

# sample data
df = pd.DataFrame(
    {
        "step": np.repeat(np.arange(0, 8), 10),
        "x": np.tile(np.linspace(0, 9, 10), 8),
        "y": r.uniform(0, 5, 80),
    }
)

# smaple plotly animated figure
fig = px.bar(df, x="x", y="y", animation_frame="step")

# generate images for each step in animation
frames = []
for s, fr in enumerate(fig.frames):
    # set main traces to appropriate traces within plotly frame
    fig.update(data=fr.data)
    # move slider to correct place
    fig.layout.sliders[0].update(active=s)
    # generate image of current state
    frames.append(PIL.Image.open(io.BytesIO(fig.to_image(format="png"))))
    
# create animated GIF
frames[0].save(
        os.path.join(SAVEDIR, "test.gif"),
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=500,
        loop=0,
    )