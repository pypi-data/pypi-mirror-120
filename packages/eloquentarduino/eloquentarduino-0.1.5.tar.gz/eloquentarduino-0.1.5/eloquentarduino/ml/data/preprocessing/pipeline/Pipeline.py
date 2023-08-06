import numpy as np
import pickle
from copy import copy
from cached_property import cached_property
from eloquentarduino.ml.data.Dataset import Dataset
from eloquentarduino.utils import jinja
from sklearn.model_selection import cross_validate
from eloquentarduino.ml.classification.abstract.Classifier import Classifier
from eloquentarduino.ml.data.preprocessing.pipeline.BaseStep import BaseStep
from eloquentarduino.ml.data.preprocessing.pipeline.classification.Classify import Classify
from eloquentarduino.ml.data.preprocessing.pipeline.device.PipelineDeviceResources import PipelineDeviceResources


class Pipeline:
    """
    Define a pre-processing pipeline that can be ported to plain C++
    """
    def __init__(self, name, dataset, steps):
        """
        Constructor
        :param name: str a name for the pipeline
        :param dataset: Dataset a dataset to train the pipeline on
        :param steps: list list of steps
        """
        assert isinstance(dataset, Dataset), 'dataset MUST be an instance of eloquentarduino.ml.data.Dataset.Dataset, %s found' % str(type(dataset))
        assert isinstance(steps, list), 'steps MUST be a list'

        self.name = name
        self.X = dataset.X.copy()
        self.y = dataset.y.copy()
        self.steps = []

        [self.add(step) for step in steps]
        self._assert_unique_steps()

    def __str__(self):
        """
        Convert to string
        """
        steps = '\n'.join([str(step) for step in self.steps])

        return '%s\n%s\n%s' % (self.name, '-' * len(self.name), steps)

    def __repr__(self):
        """
        Convert to string
        """
        return str(self)

    def __getitem__(self, item):
        """
        Get step by name
        :param item: str
        :return: Step|None
        """
        step = [step for step in self.steps if step.name == item]

        return step[0] if len(step) == 1 else None

    @property
    def dataset(self):
        """
        Convert pipeline data to Dataset object
        """
        assert self.y is None or len(self.y.shape) == 1 or self.y.shape[1] == 1, 'y MUST be None or 1d'

        return Dataset(name=self.name, X=self.X, y=np.flatten(self.y), test_validity=False)

    @property
    def input_dim(self):
        """
        Get input dim of the whole pipeline
        """
        return self.steps[0].input_dim

    @property
    def working_dim(self):
        """
        Get work data size
        """
        return max([step.working_dim for step in self.steps])

    @property
    def output_dim(self):
        """
        Get output size (works only after fitting)
        """
        return self.X.shape[1]

    @property
    def includes(self):
        """
        Get list of included libraries
        """
        return [library for step in self.steps for library in step.includes]

    @cached_property
    def resources(self):
        return PipelineDeviceResources(self)

    def add(self, step):
        """
        Add step
        :param step: BaseStep
        """
        if isinstance(step, Classifier):
            step = Classify(clf=step)

        assert isinstance(step, BaseStep), 'steps MUST extend BaseStep: %s found' % str(step.__class__)
        self.steps.append(step)
        self._assert_unique_steps()

    def until(self, step_name, including=True, clone=True):
        """
        Return a pipeline up until the given step
        :param step_name: str
        :param including: bool if True, the given step will be included
        :param clone: bool if True, steps will be cloned
        """
        idx = max([i if step.name == step_name else -1 for i, step in enumerate(self.steps)])
        assert idx > -1, 'step %s not found' % step_name

        if including:
            idx += 1

        steps = self.steps[:idx]

        if clone:
            steps = [copy(step) for step in steps]

        return Pipeline(self.name, Dataset('Dataset', self.X, self.y), steps)

    def fit(self, catch_error=False):
        """
        Fit the steps
        :param catch_error: bool if True, returns None on common errors due to steps incompatibility
        :return: self
        """
        for step in self.steps:
            try:
                self.X, self.y = step.fit(self.X, self.y)
            except ValueError as err:
                if catch_error:
                    return None
                else:
                    raise err

        return self

    def transform(self, X, y=None):
        """
        Apply pipeline
        :param X:
        :param y:
        """
        # if X is a dataset, extract X and y
        if hasattr(X, 'X') and hasattr(X, 'y'):
            y = y or X.y
            X = X.X

        return_X_y = y is not None

        for step in self.steps:
            X, y = step.transform(X, y)

        if return_X_y:
            return X, y

        return X

    def score(self, clf, cv=3, return_average_accuracy=True, return_best_estimator=False):
        """
        Score a classifier on this pipeline via cross validation
        :param clf:
        :param cv: int cross validation splits
        :param return_average_accuracy: bool
        :param return_best_estimator: bool
        """
        scores = cross_validate(clf, self.X, self.y, cv=cv, return_estimator=True)

        if return_average_accuracy:
            return scores['test_score'].mean()

        if return_best_estimator:
            max_score_idx = scores['test_score'].argmax()
            return scores['estimator'][max_score_idx]

        return scores

    def port(self, classname='Pipeline', instance_name=None):
        """
        Port to C++
        :param classname: str class name of the generated class
        :param instance_name: str|None if not None, creates an instance of the class with the given name
        :return: str the generated C++ code
        """
        return jinja('ml/data/preprocessing/pipeline/Pipeline.jinja', {
            'ns': self.name,
            'classname': classname,
            'instance_name': instance_name,
            'steps': self.steps,
            'input_dim': self.input_dim,
            'output_dim': max([self.output_dim, self.working_dim]),
            'working_dim': max([1, self.working_dim]),
            'includes': self.includes
        }, pretty=True)

    def serialize(self, filename):
        """
        Serialize pipeline to pickle file
        :param filename: str
        """
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(filename):
        """
        Deserialize pipeline to pickle file
        :param filename: str
        :return: Pipeline
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def _assert_unique_steps(self):
        """
        Be sure step names are unique
        """
        step_names = [step.name for step in self.steps]

        assert len(step_names) == len(set(step_names)), 'steps names MUST be unique'


