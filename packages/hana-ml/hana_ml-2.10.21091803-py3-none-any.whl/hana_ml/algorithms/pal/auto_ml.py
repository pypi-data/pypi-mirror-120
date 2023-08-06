"""
This module contains auto machine learning API.

"""
#pylint: disable=too-many-branches
#pylint: disable=too-many-statements
#pylint: disable=too-many-locals
#pylint: disable=line-too-long
#pylint: disable=too-few-public-methods
from hana_ml.algorithms.pal.pal_base import PALBase
from hana_ml.algorithms.pal.preprocessing import FeatureNormalizer
from hana_ml.algorithms.pal.preprocessing import KBinsDiscretizer
from hana_ml.algorithms.pal.preprocessing import Imputer
from hana_ml.algorithms.pal.preprocessing import Discretize
from hana_ml.algorithms.pal.preprocessing import MDS
from hana_ml.algorithms.pal.preprocessing import SMOTE
from hana_ml.algorithms.pal.preprocessing import SMOTETomek
from hana_ml.algorithms.pal.preprocessing import TomekLinks
from hana_ml.algorithms.pal.preprocessing import Sampling
from hana_ml.algorithms.pal.decomposition import PCA

class Preprocessing(PALBase):
    """
    Preprocessing class. Similar to the function preprocessing.

    Parameters
    ----------
    name : str
        The preprocessing algorithm name.

        - OneHotEncoder
        - FeatureNormalizer
        - KBinsDiscretizer
        - Imputer
        - Discretize
        - MDS
        - SMOTE
        - SMOTETomek
        - TomekLinks
        - Sampling
    """
    def __init__(self, name):
        super(Preprocessing, self).__init__()
        self.name = name

    def fit_transform(self, data, key=None, features=None, **kwargs):
        """
        Execute the preprocessing algorithm and return the transformed dataset.

        Parameters
        ----------
        data : DataFrame
            Input data.
        key : str, optional
            Name of the ID column.

            Defaults to the index column of ``data`` (i.e. data.index) if it is set.
        features : list, optional
            The columns to be preprocessed.
        """
        args = dict(**kwargs)
        if data.index is not None:
            key = data.index
        key_is_none = False
        if key is None:
            key_is_none = True
        if features is None:
            features = data.columns
            if self.name == 'OneHotEncoder':
                features = []
                for col, val in data.get_table_structure().items():
                    if 'VARCHAR' in val.upper():
                        features.append(col)
            if key is not None:
                if key in features:
                    features.remove(key)
        if isinstance(features, str):
            features = [features]
        if self.name != "OneHotEncoder":
            if key is None:
                key = "ID"
                data = data.add_id(key)
            data = data.select([key] + features)
        other = data.deselect(features)
        if self.name == 'FeatureNormalizer':
            if 'method' not in args.keys():
                args['method'] = "min-max"
                args['new_max'] = 1.0
                args['new_min'] = 0.0
            transformer = FeatureNormalizer(**args)
            result = transformer.fit_transform(data, key)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'KBinsDiscretizer':
            if 'strategy' not in args.keys():
                args['strategy'] = "uniform_size"
                args['smoothing'] = "means"
            transformer = KBinsDiscretizer(**args)
            result = transformer.fit_transform(data, key).deselect(["BIN_INDEX"])
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Imputer':
            categorical_variable = None
            strategy_by_col = None
            if 'categorical_variable' in args.keys():
                categorical_variable = args['categorical_variable']
                args.pop('categorical_variable')
            if 'strategy_by_col' in args.keys():
                strategy_by_col = args['strategy_by_col']
                args.pop('strategy_by_col')
            transformer = Imputer(**args)
            result = transformer.fit_transform(data,
                                               key,
                                               categorical_variable=categorical_variable,
                                               strategy_by_col=strategy_by_col)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Discretize':
            if 'strategy' not in args.keys():
                args['strategy'] = "uniform_size"
                args['smoothing'] = "bin_means"
            col_smoothing = None
            strategy_by_col = None
            binning_variable = None
            col_smoothing = None
            categorical_variable = None
            if 'col_smoothing' in args.keys():
                col_smoothing = args['col_smoothing']
                args.pop('col_smoothing')
            if 'categorical_variable' in args.keys():
                categorical_variable = args['categorical_variable']
                args.pop('categorical_variable')
            if 'binning_variable' in args.keys():
                binning_variable = args['binning_variable']
                args.pop('binning_variable')
            if binning_variable is None:
                binning_variable = features
            transformer = Discretize(**args)
            result = transformer.fit_transform(data,
                                               binning_variable=binning_variable,
                                               key=key,
                                               col_smoothing=col_smoothing,
                                               categorical_variable=categorical_variable)[0]
            self.execute_statement = transformer.execute_statement
        elif self.name == 'MDS':
            if 'matrix_type' not in args.keys():
                args['matrix_type'] = "observation_feature"
            transformer = MDS(**args)
            result = transformer.fit_transform(data, key)
            result = result[0].pivot_table(values='VALUE', index='ID', columns='DIMENSION', aggfunc='avg')
            columns = result.columns
            rename_cols = {}
            for col in columns:
                if col != "ID":
                    rename_cols[col] = "X_" + str(col)
            result = result.rename_columns(rename_cols)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'SMOTE':
            label = None
            minority_class = None
            if 'label' in args.keys():
                label = args['label']
                args.pop('label')
            if 'minority_class' in args.keys():
                minority_class = args['minority_class']
                args.pop('minority_class')
            transformer = SMOTE(**args)
            result = transformer.fit_transform(data,
                                               label=label,
                                               minority_class=minority_class)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'SMOTETomek':
            label = None
            minority_class = None
            if 'label' in args.keys():
                label = args['label']
                args.pop('label')
            if 'minority_class' in args.keys():
                minority_class = args['minority_class']
                args.pop('minority_class')
            transformer = SMOTETomek(**args)
            result = transformer.fit_transform(data,
                                               label=label,
                                               minority_class=minority_class)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'TomekLinks':
            label = None
            minority_class = None
            variable_weight = None
            if 'label' in args.keys():
                label = args['label']
                args.pop('label')
            if 'categorical_variable' in args.keys():
                categorical_variable = args['categorical_variable']
                args.pop('categorical_variable')
            if 'variable_weight' in args.keys():
                variable_weight = args['variable_weight']
                args.pop('variable_weight')
            transformer = TomekLinks(**args)
            result = transformer.fit_transform(data,
                                               key=key,
                                               label=label,
                                               categorical_variable=categorical_variable,
                                               variable_weight=variable_weight)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Sampling':
            transformer = Sampling(**args)
            result = transformer.fit_transform(data)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'PCA':
            label = None
            n_components = None
            if 'label' in args.keys():
                label = args['label']
                args.pop('label')
            if 'n_components' in args.keys():
                label = args['n_components']
                args.pop('n_components')
            transformer = PCA(**args)
            result = transformer.fit_transform(data,
                                               key=key,
                                               n_components=n_components,
                                               label=label)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'OneHotEncoder':
            others = list(set(data.columns) - set(features))
            query = "SELECT {}".format(", ".join(others))
            if others:
                query = query + ", "
            for feature in features:
                categoricals = data.distinct(feature).collect()[feature].to_list()
                for cat in categoricals:
                    query = query + "CASE WHEN \"{0}\" = '{1}' THEN 1 ELSE 0 END \"{1}_{0}_OneHot\", ".format(feature, cat)
            query = query[:-2] + " FROM ({})".format(data.select_statement)
            self.execute_statement = query
            return data.connection_context.sql(query)
        else:
            pass
        if features is not None:
            if key is not None:
                result = other.set_index(key).join(result.set_index(key))
        if key_is_none:
            result = result.deselect(key)
        return result
