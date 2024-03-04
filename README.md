# proyecto_final_1_experimento_analitica
servicio que escucha de una cola y procesa medidas

## ejecución local
```python
python main.py
```

## ejecución por docker
```python
docker build -t metrics-worker .
docker run --env-file ./.env -p 3001:3001 metrics-worker
```