# Deploy a Streamlit Cloud

## Opcion 1: Streamlit Community Cloud (GRATIS)

### Paso 1: Crear repo en GitHub

```bash
cd london_edge
git init
git add .
git commit -m "Initial commit"
```

Crear repo en github.com y:
```bash
git remote add origin https://github.com/TU_USUARIO/london-edge.git
git push -u origin main
```

### Paso 2: Conectar a Streamlit Cloud

1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Login con GitHub
3. Click "New app"
4. Seleccionar:
   - Repository: `TU_USUARIO/london-edge`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

### Paso 3: Esperar

El deploy toma 2-5 minutos. Tu app estara en:
```
https://TU_USUARIO-london-edge.streamlit.app
```

---

## Opcion 2: Hugging Face Spaces (GRATIS)

1. Crear cuenta en [huggingface.co](https://huggingface.co)
2. New Space -> Streamlit
3. Subir archivos:
   - `app.py`
   - `requirements.txt`
   - `data/historical_prices/*.json`

---

## Opcion 3: Railway (PAGO pero facil)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

---

## Archivos necesarios

```
london_edge/
├── app.py                 # Entry point
├── requirements.txt       # Dependencies
├── .streamlit/
│   └── config.toml       # Theme config
└── data/
    └── historical_prices/
        ├── london_temp_2025-01-01.json
        ├── london_temp_2025-01-02.json
        └── ... (todos los JSONs)
```

## Nota sobre los datos

Los archivos JSON en `data/historical_prices/` deben incluirse en el repo.
Son ~365 archivos, cada uno de ~50-100KB.

Si el repo es muy grande, considera:
1. Comprimir los JSONs
2. Usar Git LFS
3. Cargar desde una API externa
