# quant-research


**Set up quant-research computing env at jupyter_notebook**:

1. mamba create -n quant-research -c conda-forge python=3.12 jupyterlab numpy pandas matplotlib yfinance scikit-learn ta tqdm
 
2. conda activate quant-research
 
3. python -m ipykernel install --user --name quant-research --display-name "Python (quant-research)"

4. set environment.yml:
    rebuild environment by conda env create -f environment.yml
    conda activate quant-research