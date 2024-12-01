import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

def kde_plot(my_acceleration, bg_data):
    res = sn.kdeplot(data=bg_data, label="Distribution")
    plt.axvline(my_acceleration, color='red', label="Your value")
    plt.xlabel("Ageing acceleration")
    plt.ylabel("Density")
    plt.title("Ageing acceleration KDE plot")
    plt.grid(True)
    plt.show()

def feat_plot(feature, age, **kwargs):
    sd = np.std(feature)

    plt.scatter(age, feature)
    plt.plot(np.unique(age), np.poly1d(np.polyfit(age, feature, 1))(np.unique(age)), color='red', label='line fit')
    plt.plot(np.unique(age), np.poly1d(np.polyfit(age, feature, 1))(np.unique(age)) + sd, color='green', label='fit + std')
    plt.plot(np.unique(age), np.poly1d(np.polyfit(age, feature, 1))(np.unique(age)) - sd, color='purple', label='fit - std')
    plt.xlabel("Age")
    feat_name = kwargs.get('feat', None)
    if feat_name is not None:
        plt.ylabel(feat_name)
        plt.title(f"{feat_name}-age dependency plot")
    else:
        plt.ylabel("Feature")
        plt.title("Feature-age dependency plot")
    
    no_legend = kwargs.get('no_legend', None)
    if no_legend is not None and not no_legend:
        plt.legend()
    elif no_legend is None:
        plt.legend()