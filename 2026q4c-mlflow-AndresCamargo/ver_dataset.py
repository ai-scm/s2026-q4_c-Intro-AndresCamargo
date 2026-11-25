import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer

df = load_breast_cancer(as_frame=True).frame
df["diagnostico"] = df["target"].map({0: "maligno", 1: "benigno"})

# Vista resumida: 5 medidas + la etiqueta
cols = ["mean radius", "mean texture", "mean perimeter", "mean area", "diagnostico"]
print(df[cols].head(8).to_string())
print("\nFilas y columnas:", df.shape)
print(df["diagnostico"].value_counts())

# CSV completo para abrirlo en VS Code o en una hoja de cálculo
df.to_csv("dataset_cancer.csv", index=False)

# Gráfica: balance de clases y una variable por clase
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
df["diagnostico"].value_counts().plot.bar(ax=ax[0], color=["#4c72b0", "#dd8452"])
ax[0].set_title("Balance de clases")
ax[0].set_ylabel("Pacientes")
for clase, color in [("maligno", "#dd8452"), ("benigno", "#4c72b0")]:
    ax[1].hist(df[df["diagnostico"] == clase]["mean radius"], bins=20, alpha=0.6, label=clase, color=color)
ax[1].set_title("Radio medio del tumor por diagnóstico")
ax[1].set_xlabel("mean radius")
ax[1].legend()
plt.tight_layout()
plt.savefig("evidencias-mlflow/07-dataset.png", dpi=120)
print("\nGráfica guardada en evidencias-mlflow/07-dataset.png")
