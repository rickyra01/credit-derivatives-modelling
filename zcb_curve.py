import os
import numpy as np
import pandas as pd
from myLib import calibration_nss, display_nss, bootstrap_df

def main():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "market_data2.xlsx")
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

    os.makedirs(os.path.join(BASE_DIR, "data", "processed"), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    

    data = pd.read_excel(DATA_PATH,
                        sheet_name= 'swap curve',
                        header = 2,
                        usecols= 'A:B',
                        nrows = 18)
    

    # NSS curve fit

    nss_df = data[data["Maturity"] >= 1] # the assignment asks to consider only rates for maturities >= 1 here
    maturities = nss_df["Maturity"]
    rates = nss_df["Swap rates (in %)"] / 100
    t_grid = np.arange(1, maturities.iloc[-1] + 1)

    nss_curve, optimized_params = calibration_nss(maturities, rates, output_maturities = t_grid)
    print(f"Optimized parameters:\n{optimized_params}")
    display_nss(nss_curve, maturities, rates)

    optimized_params = pd.DataFrame(optimized_params, index=["beta0", "beta1", "beta2", "beta3", "tau1", "tau2"])
    optimized_params.to_csv(os.path.join(OUTPUT_DIR, "nss_parameters.csv"), index=True)


    # Getting Discount factors
    rates = np.concatenate((nss_curve["NSS Predictions"], data[data["Maturity"] < 1]["Swap rates (in %)"].to_numpy() / 100))
    maturities = np.concatenate((data[data["Maturity"] < 1]["Maturity"].to_numpy(), nss_curve["Maturities"]), dtype=float)
    bootstrap = bootstrap_df(rates, maturities)
    dfs = pd.DataFrame({
        "Maturities": np.round(maturities, 2),
        "Discount Factors": bootstrap
    })
    print(dfs)

    dfs.to_csv(os.path.join(BASE_DIR, "data", "processed", "discount_factors.csv"), index=False)


if __name__ == "__main__":
    main()