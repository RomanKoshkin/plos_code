import pandas as pd

grid = []
for HAGA in [True]:
    for astro in [True, False]:
        for symmetric in [True]:
            for mex in [0.3, 0.4]:
                for t_sham_init in [1000, 30000]:
                    for use_thetas in [False, True]:
                        for stim_strength in [0.2, 0.4, 0.8, 1.0]:
                            grid.append({
                                'HAGA': HAGA,
                                'astro': astro,
                                'symmetric': symmetric,
                                't_stim': 30000,
                                't_sham': 30000,
                                't_sham_init': t_sham_init,
                                'mex': mex,
                                'use_thetas': use_thetas,
                                'stim_strength': stim_strength,
                            })

grid = pd.DataFrame(grid)
grid.to_csv('grid.csv')
