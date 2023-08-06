from typing import List, Optional, Tuple
from temporis.iterators.batcher import Batcher
import tensorflow as tf
from rul_pm.models.keras import KerasTrainableModel
from tcn import TCN
from tensorflow.keras import Input, Model, optimizers
from tensorflow.keras.layers import (
    AveragePooling1D,
    BatchNormalization,
    Concatenate,
    Conv1D,
    Dense,
    Dropout,
    Embedding,
    Flatten,
    GlobalAveragePooling1D,
    GlobalMaxPooling1D,
    Lambda,
    Dropout,
    MaxPooling1D,
    UpSampling1D,
    Add,
    Conv2D,
    ReLU,
)
from tensorflow.python.keras.layers.core import SpatialDropout1D

from keras.engine import Layer
from keras import backend as K
import uuid
import tensorflow as tf


class GradientReversal(Layer):
    """Flip the sign of gradient during training."""

    def __init__(self, hp_lambda, **kwargs):
        super(GradientReversal, self).__init__(**kwargs)
        self.supports_masking = False
        # self.hp_lambda = hp_lambda
        self.hp_lambda = K.variable(hp_lambda, dtype="float32", name="hp_lambda")

    def build(self, input_shape):
        self.trainable_weights = []

    def reverse_gradient(self, X):
        """Flips the sign of the incoming gradient during training."""
        """try:
            self.num_calls += 1
        except AttributeError:
            self.num_calls = 1"""

        grad_name = "GradientReversal%d" % uuid.uuid4()  # self.num_calls

        @tf.RegisterGradient(grad_name)
        def _flip_gradients(op, grad):
            return [tf.negative(grad) * self.hp_lambda]

        g = K.get_session().graph
        with g.gradient_override_map({"Identity": grad_name}):
            y = tf.identity(X)

        return y

    def call(self, x, mask=None):
        return self.reverse_gradient(x)

    def get_output_shape_for(self, input_shape):
        return input_shape

    def set_hp_lambda(self, hp_lambda):
        # self.hp_lambda = hp_lambda
        K.set_value(self.hp_lambda, hp_lambda)

    def increment_hp_lambda_by(self, increment):
        new_value = float(K.get_value(self.hp_lambda)) + increment
        K.set_value(self.hp_lambda, new_value)

    def get_hp_lambda(self):
        return float(K.get_value(self.hp_lambda))

    def get_config(self):
        config = {}
        base_config = super(GradientReversal, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class DANNKerasModel(tf.keras.Model):
    def __init__(self, encoder, input_shape:Tuple[int, int]):
        self.encoder = encoder
        x = Input(input_shape)
        input = x
        x = self.encoder(x)
        RUL = Dense(1, activation="relu", use_bias=True)(x)

        self.gradient_reversal = GradientReversal(1.0)
        x_domain = self.gradient_reversal(x)
        domain = Dense(1, use_bias=True)(x_domain)
        
        super(DANNKerasModel, self).__init__(inputs=[input], outputs=[RUL, domain])
        

        


    def train_step(self, data):
        source_ds, target_ds = data
        x_source, RUL_true = source_ds
        x_target = target_ds

        with tf.GradientTape() as tape:
            RUL_pred, domain_pred = self(x_source, training=True)
            loss = self.compiled_loss.regression(RUL_true, RUL_pred)
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        domain_true = [tf.ones(x_source.shape[0]), tf.zeros(x_target.shape[0])]
        with tf.GradientTape() as tape:
            RUL_pred, domain_pred = self([x_source, x_target], training=True)            
            loss = self.compiled_loss.classification(domain_true, domain_pred)

        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))



        return {m.name: m.result() for m in self.metrics}


class DANN(KerasTrainableModel):
    def __init__(self, feature_extractor:tf.keras.Model, **kwargs):
        super().__init__(**kwargs)
        self.feature_extractor = feature_extractor

    def compile(self):
        self.compiled = True
        self.model.compile(
            regression_loss=self.loss,
            classification_loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate),
            metrics=self.metrics,
        )

    def build_model(self, input_shape):
        return DANNKerasModel(self.feature_extractor, input_shape)


    def fit(
        self,
        source_domain_batcher: Batcher,
        taget_domain_batcher: Batcher,
        val_batcher: Optional[Batcher] = None,
        verbose=1,
        epochs=50,
        reset=True,
        class_weight=None,
        print_summary=True,
        callbacks: List[tf.keras.callbacks.Callback] = [],
    ):
        """Fit the model with the given dataset batcher

        Parameters
        ----------
        train_batcher : Batcher
            Batcher of the training set
        val_batcher : Batcher, optional
            Batcher of the validation set, by default None
        verbose : int, optional
            Verbosity level, by default 1
        epochs : int, optional
            Number of epochs to train, by default 50
        reset : bool, optional
            whether to reset the model weights, by default True
        class_weight : str or function, optional
            [description], by default None
        print_summary : bool, optional
            whether to print the model summary, by default True

        Returns
        -------

            Training history
        """
        if reset:
            self.reset()
        self._input_shape = train_batcher.input_shape
        self._model = self.build_model(self._input_shape)
        if not self.compiled:
            self.compile()

        if print_summary:
            self.model.summary()

        a = self.batcher_generator(train_batcher)
        validation_params = {}
        if val_batcher is not None:
            b = self.batcher_generator(val_batcher)
            validation_params = {
                "validation_data": b,
                "validation_steps": len(val_batcher),
            }

        logger.debug("Start fitting")
        history = self.model.fit(
            zip(source_dataset, target_dataset),
            verbose=verbose,
            steps_per_epoch=len(train_batcher),
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weight,
            **validation_params
            
        )
        self.history = history.history
        return self.history
