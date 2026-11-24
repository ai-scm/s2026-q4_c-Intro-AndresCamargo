from sklearn.datasets import load_breast_cancer

df = load_breast_cancer(as_frame=True).frame

print("Dimensiones:", df.shape)
print("Nulos totales:", df.isnull().sum().sum())
print("Balance de clases:")
print(df["target"].value_counts())
