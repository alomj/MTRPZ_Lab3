from fastapi import APIRouter

import numpy as np

router = APIRouter()


@router.get('')
def hello_world() -> dict:
    return {'msg': 'Hello, World!'}


def multiply_matrix() -> dict:
    first_matrix = np.random.randint(low=0, high=10, size=(10, 10))
    second_matrix = np.random.randint(low=0, high=10, size=(10, 10))
    product = np.dot(np.array(first_matrix), np.array(second_matrix))

    return {'first_matrix': first_matrix.tolist(),
            'second_matrix': second_matrix.tolist(),
            'product': product.tolist()
            }