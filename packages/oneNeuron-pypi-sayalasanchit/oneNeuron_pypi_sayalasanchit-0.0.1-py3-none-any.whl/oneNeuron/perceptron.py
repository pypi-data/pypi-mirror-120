import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
    def __init__(self, eta, epochs):
        self.eta=eta # Learning rate
        self.epochs=epochs

        self.weights=np.random.randn(3) * 1e-4 # Very small weights initialization
        logging.info(f"Initial weights before training:\n{self.weights}")

    def activationFunction(self, inputs, weights):
        z=np.dot(inputs, weights) # inputs:(4, 3); weights:(3, 1); z:(4, 1)
        return np.where(z>0, 1, 0)

    def fit(self, X, y):
        self.X=X
        self.y=y
        X_with_biases=np.c_[self.X, -np.ones((self.X.shape[0], 1))]
        logging.info(f"X with biases:\n{X_with_biases}")
        for epoch in tqdm(range(self.epochs), total=self.epochs):
            logging.info("**"*10)
            logging.info(f"For epoch:\n{epoch}/{self.epochs-1}")
            logging.info("**"*10)

            y_hat=self.activationFunction(X_with_biases, self.weights)
            logging.info(f"Predicted value after forward pass:\n{y_hat}")
            self.error=self.y-y_hat
            logging.info(f"Error:\n{self.error}")
            
            # Weight updates
            self.weights+=self.eta*np.dot(X_with_biases.T, self.error) # X_with_biases:(4, 3); self.error:(4, 1); self.weights:(3, 1)
            logging.info(f"Updated weights:\n{self.weights}")
            logging.info("##"*10)
    
    def predict(self, X):
        X_with_biases=np.c_[X, -np.ones((X.shape[0], 1))]
        return self.activationFunction(X_with_biases, self.weights)

    def totalLoss(self):
        total_error=np.sum(self.error)
        logging.info(f"Total loss:\n{total_error}")
        return total_error