import numpy as np
from tqdm import tqdm
import pandas as pd
from scipy.special import expit

def weighted_percentile(data, weights, perc):
    ix = np.argsort(data)
    data = data[ix] # sort data
    weights = weights[ix] # sort weights
    cdf = (np.cumsum(weights) - 0.5 * weights) / np.sum(weights) # 'like' a CDF function
    return np.interp(perc, cdf, data)

def movavg_approx(qx, x, y, sd_x=1, weights='gaussian', high_variance_fixed=False, var_thr=4):
    y_avg = []
    y_sd = []
    y_median = []
    y_q1 = []
    y_q3 = []
    y_qx = []
    for cx in qx:
        if weights == 'gaussian':
            aweights = np.exp(-((x - cx) / sd_x) ** 2)
        weighted_avg = np.average(y, weights=aweights)
        weighted_sd = np.sqrt(np.cov(y, aweights=aweights))
        weighted_median = weighted_percentile(y, aweights, 0.5)
        weighted_q1 = weighted_percentile(y, aweights, 0.25)
        weighted_q3 = weighted_percentile(y, aweights, 0.75)
        if high_variance_fixed:
            if weighted_sd > var_thr:
                norm_sd = (weighted_sd - var_thr) / var_thr
                coef = expit(norm_sd * 2 - 1)
                weighted_avg = weighted_avg * (1 - coef) + cx * coef 
        y_qx += [cx]
        y_avg += [weighted_avg]
        y_sd += [weighted_sd]
        y_median += [weighted_median]
        y_q1 += [weighted_q1]
        y_q3 += [weighted_q3]        
    return pd.DataFrame({
        'x': y_qx,
        'movavg': y_avg,
        'movsd': y_sd,
        'movmed': y_median,
        'movq1': y_q1,
        'movq3': y_q3,
    })

def make_movavg(df_ys, feature_names, sd_age = 7):
    df_ysn = df_ys.copy()
    ages = df_ysn['age'].values
    for feature_name in tqdm(feature_names):
        feature = df_ysn[feature_name].values
        feature_avg = []
        feature_sd = []
        feature_median = []
        feature_q1 = []
        feature_q3 = []
        for age in ages:
            weights = np.exp(-((ages - age) / sd_age) ** 2)
            weighted_avg = np.average(feature, weights=weights)
            weighted_sd = np.sqrt(np.cov(feature, aweights=weights))
            weighted_median = weighted_percentile(feature, weights, 0.5)
            weighted_q1 = weighted_percentile(feature, weights, 0.25)
            weighted_q3 = weighted_percentile(feature, weights, 0.75)
            feature_avg += [weighted_avg]
            feature_sd += [weighted_sd]
            feature_median += [weighted_median]
            feature_q1 += [weighted_q1]
            feature_q3 += [weighted_q3]
        df_ysn['movavg_' + feature_name] = feature_avg
        df_ysn['movsd_' + feature_name] = feature_sd
        df_ysn['movq1_' + feature_name] = feature_q1
        df_ysn['movmed_' + feature_name] = feature_median
        df_ysn['movq3_' + feature_name] = feature_q3
    return df_ysn

def assess_subject_over_movavg(df_ys, feature_names, coef = 0.5):
    df_ysn = df_ys.copy()
    for feature_name in tqdm(feature_names):
        feature = df_ysn[feature_name]
        feature_avg = df_ysn['movavg_' + feature_name]
        feature_sd = df_ysn['movsd_' + feature_name] * coef
        df_ysn['higher_' + feature_name] = feature > feature_avg + feature_sd
        df_ysn['less_' + feature_name] = feature < feature_avg - feature_sd
    return df_ysn

def assess_subject_over_quartiles(df_ys, feature_names):
    df_ysn = df_ys.copy()
    for feature_name in tqdm(feature_names):
        feature = df_ysn[feature_name]
        feature_q1 = df_ysn['movq1_' + feature_name]
        feature_q3 = df_ysn['movq3_' + feature_name]
        df_ysn['higher_' + feature_name] = feature > feature_q3
        df_ysn['less_' + feature_name] = feature < feature_q1
    return df_ysn

def make_movavg_model(df_ys, feature_names, age_space=None, age_lim=[15, 80], sd_age = 7):
    if age_space is None:
        age_space = np.arange(age_lim[0], age_lim[1] + 1)
    ages = df_ys['age'].values
    feature_models = {}
    feature_models['age'] = age_space
    for feature_name in tqdm(feature_names):
        feature = df_ys[feature_name].values
        feature_avg = []
        feature_sd = []
        feature_median = []
        feature_q1 = []
        feature_q3 = []
        for age in age_space:
            weights = np.exp(-((ages - age) / sd_age) ** 2)
            weighted_avg = np.average(feature, weights=weights)
            weighted_sd = np.sqrt(np.cov(feature, aweights=weights))
            weighted_median = weighted_percentile(feature, weights, 0.5)
            weighted_q1 = weighted_percentile(feature, weights, 0.25)
            weighted_q3 = weighted_percentile(feature, weights, 0.75)
            feature_avg += [weighted_avg]
            feature_sd += [weighted_sd]
            feature_median += [weighted_median]
            feature_q1 += [weighted_q1]
            feature_q3 += [weighted_q3]
        feature_models['movavg_' + feature_name] = feature_avg
        feature_models['movsd_' + feature_name] = feature_sd
        feature_models['movq1_' + feature_name] = feature_q1
        feature_models['movmed_' + feature_name] = feature_median
        feature_models['movq3_' + feature_name] = feature_q3
    df_feature_models = pd.DataFrame(feature_models)
    return df_feature_models