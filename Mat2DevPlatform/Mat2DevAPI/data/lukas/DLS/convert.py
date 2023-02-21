import pandas as pd

path = "Umicore-PtC05-ic065-1Prop088.csv"
path1 = "IrO2-15wt-ic013-1Prop086-066ml.csv"

df = pd.read_csv(path, delimiter = ",", decimal = ",")
df['Dilution'] = 0.66
sizes = []
intensities = []
volumes = []
for col in df.columns:
    if col.startswith("Intensities["):
        intensities.append(col)
    if col.startswith("Volumes["):
        volumes.append(col)
    if col.startswith("Sizes["):
        sizes.append(col)
cols = df.columns
df['sizes'] = [[e for e in row if e==e] for row in df[sizes].values.tolist()]
df['intensities'] = [[e for e in row if e==e] for row in df[intensities].values.tolist()]
df['volumes'] = [[e for e in row if e==e] for row in df[volumes].values.tolist()]
df['Researcher'] = "Lukas"
df['Material'] = path[:-4]
df['Ontology'] = "DynamicLightScattering"
df['Instrument'] = "Zetasizer Nano ZS"
df['PIDA'] = path[:-4]
for i, el in enumerate(df['PIDA']):
    df['PIDA'][i]   += "_" + str(i)
df.to_csv(path1[:-4]+ "_DLS.csv", mode = 'a', header = False)

