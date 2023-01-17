from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def preprocess_data(X, y):
    """"
        This function preprocesses the input data by scaling the feature values and encoding the labels as integers.

    Inputs:
        X (pandas.DataFrame or numpy.ndarray): The feature values to be processed.
        y (pandas.Series or numpy.ndarray): The labels to be processed.

    Returns:
        X_scaled (numpy.ndarray): The scaled feature values.
        y_encoded (numpy.ndarray): The encoded labels.

    """
    # Scale the feature values using a StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Encode the labels as integers
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X_scaled, y_encoded


def compute_subgradients(v, X, y, C, sample_size):
    """
        This function computes the subgradients of the objective function for a given set of model parameters.

    Inputs:
        v (tuple): A tuple containing the weights and bias term of the model.
        X (numpy.ndarray): The feature values of the training data.
        y (numpy.ndarray): The labels of the training data.
        C (float): The regularization parameter.
        sample_size (int): The size of the sample subset used to approximate the subgradients.

    Returns:
        subgrad_w (numpy.ndarray): The subgradient of the objective function with respect to the weights.
        subgrad_b (float): The subgradient of the objective function with respect to the bias term.
    """

    w, b = v
    n = len(X)
    # if sample_size > n:
    #     sample_size = n
    # # n = len(X)
    sample_size = min(n, sample_size)
    margin = y * (np.dot(X, w) + b)
    hinge_loss = np.maximum(0, 1 - margin)
    hinge_loss[hinge_loss == 0] = 1
    sample_indices = np.random.choice(n, sample_size, replace=False)
    X_sample = X[sample_indices]
    y_sample = y[sample_indices]
    margin_sample = y_sample * (np.dot(X_sample, w) + b)
    hinge_loss_sample = np.maximum(0, 1 - margin_sample)
    subgrad_w = w - C * \
        np.sum(X_sample * y_sample[:, np.newaxis] *
               hinge_loss_sample[:, np.newaxis], axis=0)
    subgrad_b = - C * np.sum(y_sample * hinge_loss_sample)
    return subgrad_w, subgrad_b


def compute_objective_function(v, X, y, C, sample_size):
    """
    This function computes the objective function value for a given set of model parameters.

    Inputs:
        v (tuple): A tuple containing the weights and bias term of the model.
        X (numpy.ndarray): The feature values of the training data.
        y (numpy.ndarray): The labels of the training data.
        C (float): The regularization parameter.
        sample_size (int): The size of the sample subset used to approximate the objective function value.

    Returns:
        obj_value (float): The value of the objective function.
    """
    w, b = v
    n = len(X)
    # if sample_size > n:
    #     sample_size = n
    # # n = len(X)
    sample_size = min(n, sample_size)
    margin = y * (np.dot(X, w) + b)
    hinge_loss = np.maximum(0, 1 - margin)
    hinge_loss[hinge_loss == 0] = 1
    sample_indices = np.random.choice(n, sample_size, replace=False)
    X_sample = X[sample_indices]
    y_sample = y[sample_indices]
    obj_value = 0.5 * np.linalg.norm(w) ** 2 + C * np.mean(hinge_loss)
    return obj_value
