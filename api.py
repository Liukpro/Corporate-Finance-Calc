from fastapi import FastAPI, UploadFile, File
import pandas as pd

from exec_engine import FinancialExecutionEngine
from batch_engine import BatchFinancialEngine

app = FastAPI(title="Financial DAG System")


@app.post("/run/")
async def run(file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    engine = FinancialExecutionEngine(df)

    results = (
        engine
        .run_data_layer()
        .run_validation()
        .run_metrics()
    )

    return {
        "status": "success",
        "mode": "single",
        "results": results
    }


@app.post("/run-batch/")
async def run_batch(file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    batch_engine = BatchFinancialEngine(df)

    results = batch_engine.run()

    return {
        "status": "success",
        "mode": "batch",
        "results": results
    }
