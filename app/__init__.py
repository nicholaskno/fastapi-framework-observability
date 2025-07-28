from fastapi import FastAPI
from app.utils.metrics import AppMetrics, MetricsMiddleware
import app.utils.config as apiConfig


# Start FastAPI
app = FastAPI()
logger, meter = apiConfig.initObservability(app)

# Initialize Prometheus Metrics
metrics = AppMetrics(meter)
app.add_middleware(MetricsMiddleware, metrics=metrics)

# CORS
apiConfig.setCors(app)

# Include Routes
apiConfig.setRoutes(app)

# Open API Doc
apiConfig.setOpenApiCfg(app)
