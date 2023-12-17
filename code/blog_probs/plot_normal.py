# %% Imports
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io
import os
import PIL

# %% Globals
SAVEDIR="blog/2023/probs"

XMIN = -10
XMAX = 10

# %% Functions

def normal_distr(mu: float, sigma: float):
    x = np.linspace(XMIN, XMAX, 200)
    coef = 1 / (sigma * np.sqrt(2 * np.pi))
    frac = ((x - mu) / sigma)**2
    y = coef * np.exp( (-0.5) * frac)
    x, y = x.tolist(), y.tolist()
    mu = [mu] * len(x)
    sigma = [sigma] * len(x)
    return x, y, mu, sigma

def fig2gif(fig, filename: str = "test"):
    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=18,  # Set the font size here
            color="RebeccaPurple"
        ),
        width=600, 
        height=500
    )
    
    frames = []
    for s, fr in enumerate(fig.frames):
        fig.update(data=fr.data)
        fig.layout.sliders[0].update(active=s)
        frames.append(PIL.Image.open(io.BytesIO(fig.to_image(format="png"))))
        
    # create animated GIF
    frames[0].save(
            os.path.join(SAVEDIR, f"{filename}.gif"),
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=500,
            loop=0,
        )

# %% Plot (vary mu)

mu_arr = np.arange(-10, 10)
sigma = 1

xyms_arr = [normal_distr(mu, sigma) for mu in mu_arr]
xyms_arr = np.array(xyms_arr)

x_arr = xyms_arr[:, 0, :].reshape(-1)
y_arr = xyms_arr[:, 1, :].reshape(-1)
m_arr = xyms_arr[:, 2, :].reshape(-1)
s_arr = xyms_arr[:, 3, :].reshape(-1)

# sample data
df = pd.DataFrame(
    {
        "mu": m_arr,
        "random variable": x_arr,
        "distribution": y_arr,
    }
)

fig = px.line(df, 
              x="random variable", 
              y="distribution", 
              animation_frame="mu", 
              title="Normal distribution (varying mu)")
fig2gif(fig, "normal_mu")
# %% Plot (vary sigma)

mu = 0
sigma_arr = np.arange(1, 20) / 20

xyms_arr = [normal_distr(mu, sigma) for sigma in sigma_arr]
xyms_arr = np.array(xyms_arr)

x_arr = xyms_arr[:, 0, :].reshape(-1)
y_arr = xyms_arr[:, 1, :].reshape(-1)
m_arr = xyms_arr[:, 2, :].reshape(-1)
s_arr = xyms_arr[:, 3, :].reshape(-1)

# sample data
df = pd.DataFrame(
    {
        "sigma": s_arr,
        "random variable": x_arr,
        "distribution": y_arr,
    }
)

fig = px.line(df, 
              x="random variable", 
              y="distribution", 
              animation_frame="sigma", 
              title="Normal distribution (varying sigma)")
fig.update_yaxes(range=[0, 5])
fig2gif(fig, "normal_sigma")

# %%
