# Credit Derivatives Modelling

This project implements a simplified credit risk modelling pipeline in Python, including yield curve calibration, CDS hazard rate estimation, and multi-name default simulation.

## Project Structure

- `data/` – input Excel files (market data)
- `outputs/` – plots and model outputs
- `credit_derivatives_assignment.ipynb`
- `requirements.txt`

## Workflow

1. **Yield Curve Calibration**  
   Calibrate a Nelson–Siegel–Svensson (NSS) model to the swap curve and compute discount factors

2. **CDS Calibration**  
   Bootstrap hazard rates from CDS spreads and compute survival and default probabilities

3. **Copula Simulation**  
   Simulate correlated default times using a Gaussian copula and price a stylized first-to-default CDS via Monte Carlo

## Methodology

- NSS yield curve calibration via nonlinear least squares
- Hazard rate bootstrapping via Brent root-finding
- Survival probability construction under piecewise-constant hazard rates
- Rank-based transformation of CDS spreads to uniform variables
- Gaussian copula with Cholesky decomposition
- Monte Carlo simulation of joint default events

## Data

- Market data: CDS spreads and swap curve (Excel files in `data`)
- Processed data: generated during execution (e.g. discount factors)

## Outputs

- NSS parameters and fitted yield curve plots
- Discount factor term structure
- Hazard rates per entity
- Survival and default probability curves
- Correlation matrix of transformed variables
- Monte Carlo estimate of CDS fair value

## Usage

Run the scripts in sequence:

```bash
pip install -r requirements.txt
