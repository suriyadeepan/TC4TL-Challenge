import os
import pickle
import types

from tqdm import tqdm


def aggregate_features_from_folder(folder, key, feat_fn,
                                   postproc_fn, predictors=None,
                                   target=None, encoders={}, testing=False):
    features = []
    # for filename in tqdm(files, total=len(files)):
    _key = key.sample(100) if testing else key
    for _, row in tqdm(_key.iterrows(), total=_key.shape[0]):
        filepath = os.path.join(folder, row.fileid)
        features.append(feat_fn(filepath, row))
    df, encoders = postproc_fn(features, encoders=encoders)
    if isinstance(predictors, type(None)):
        return df, encoders
    if not isinstance(predictors, type([6, 9])):
        assert isinstance(predictors, types.FunctionType)
        predictors = predictors(df)
    assert len(predictors) > 0
    assert df[predictors].shape[0] > 0
    assert target in df
    return df[['fileid'] + predictors + [target]], encoders


def save_encoders(encoders, filepath):
    with open(filepath, 'wb') as fd:
        pickle.dump(encoders, fd)


def pad_devset(devset, trainset):
    for col in trainset.columns:
        if col not in devset:
            devset[col] = trainset[col].min()
    return devset