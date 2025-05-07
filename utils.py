dataset_map = {
    "lucas":"LUCAS",
    "indian_pines":"Indian Pines",
    "ghisaconus":"GHISACONUS",
}

metric_map = {
    "time":{
        "LUCAS": "Logarithmic Training Time",
        "LUCAS (Skipped)": "Logarithmic Training Time",
        "LUCAS (Downsampled)": "Logarithmic Training Time",
        "LUCAS (Truncated)": "Logarithmic Training Time",
        "Indian Pines": "Logarithmic Training Time",
        "GHISACONUS": "Logarithmic Training Time",
    },
    "metric1":{
        "LUCAS": "$R^2$",
        "LUCAS (Skipped)": "$R^2$",
        "LUCAS (Downsampled)": "$R^2$",
        "LUCAS (Truncated)": "$R^2$",
        "Indian Pines": "OA",
        "GHISACONUS": "OA",
    },
    "metric2":{
        "LUCAS": "RMSE",
        "Indian Pines": "$\kappa$",
        "GHISACONUS": "$\kappa$",
    }
}

algorithm_map = {
    "all_bands" : "All Bands",
    "bsdr":"BSDR",
    "bsnet":"BS-Net-FC",
    "zhang":"Zhang et al.",
    "mcuve":"MCUVE",
    "pcal":"PCAL",
    "lasso":"LASSO",
    "spa":"SPA",
}

color_map = {
    "All Bands" : "black",
    "BSDR":"blue",
    "BS-Net-FC":"red",
    "Zhang et al.":"green",
    "MCUVE":"purple",
    "PCAL":"brown",
    "LASSO":"pink",
    "SPA":"cyan",
}

