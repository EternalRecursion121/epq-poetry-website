import faiss
import numpy as np
import pandas as pd

res = faiss.StandardGpuResources()  # use a single GPU