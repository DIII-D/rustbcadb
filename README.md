# rustbcadb
Python package to generate a database of sputtering yield and reflection coefficients with rustbca 

#install

1. Create a new conda environment

Create a new conda/mamba environment named `rust_bca` with the package rust
```bash
  mamba create -n rust_bca python =3.10 rust```
  mamba activate rust_bca
```

2. Install rustbcadb

```
git clone https://github.com/DIII-D/rustbcadb
cd rustbcadb
poetry install
cd ..
```

