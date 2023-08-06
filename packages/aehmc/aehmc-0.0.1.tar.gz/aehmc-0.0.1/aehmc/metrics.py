from typing import Callable, Tuple

import aesara.tensor as aet
import aesara.tensor.slinalg as slinalg
from aesara.tensor.random.utils import RandomStream
from aesara.tensor.var import TensorVariable


def gaussian_metric(
    inverse_mass_matrix: TensorVariable,
) -> Tuple[Callable, Callable, Callable]:
    shape = aet.shape(inverse_mass_matrix)[0]

    if inverse_mass_matrix.ndim == 1:
        mass_matrix_sqrt = aet.sqrt(aet.inv(inverse_mass_matrix))
        dot, matmul = lambda x, y: x * y, lambda x, y: x * y
    elif inverse_mass_matrix.ndim == 2:
        tril_inv = slinalg.cholesky(inverse_mass_matrix)
        identity = aet.eye(shape)
        mass_matrix_sqrt = slinalg.solve_lower_triangular(tril_inv, identity)
        dot, matmul = aet.dot, aet.dot
    else:
        raise ValueError(
            f"Expected a mass matrix of dimension 1 (diagonal) or 2, got {inverse_mass_matrix.ndim}"
        )

    def momentum_generator(srng: RandomStream) -> TensorVariable:
        norm_samples = srng.normal(0, 1, size=shape)
        momentum = dot(norm_samples, mass_matrix_sqrt)
        return momentum

    def kinetic_energy(momentum: TensorVariable) -> TensorVariable:
        velocity = matmul(inverse_mass_matrix, momentum)
        kinetic_energy = 0.5 * aet.dot(velocity, momentum)
        return kinetic_energy

    def is_turning(
        momentum_left: TensorVariable,
        momentum_right: TensorVariable,
        momentum_sum: TensorVariable,
    ) -> bool:
        velocity_left = matmul(inverse_mass_matrix, momentum_left)
        velocity_right = matmul(inverse_mass_matrix, momentum_right)

        rho = momentum_sum - (momentum_right + momentum_left) / 2
        turning_at_left = aet.dot(velocity_left, rho) <= 0
        turning_at_right = aet.dot(velocity_right, rho) <= 0

        return turning_at_left | turning_at_right

    return momentum_generator, kinetic_energy, is_turning
