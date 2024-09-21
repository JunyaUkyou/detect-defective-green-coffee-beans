from fastapi import FastAPI


app = FastAPI()

@app.get('/ssd')
async def ssd():
  return 'ssd'