import tensorflow as tf

tf.random.set_seed(0)


def shape_list(tensor):
    static = tensor.shape.as_list()
    dynamic = tf.unstack(tf.shape(tensor))
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]


def shift_tokens_right(
    input_ids: tf.Tensor, pad_token_id: int, decoder_start_token_id: int
):
    start_tokens = tf.fill((shape_list(input_ids)[0], 1), decoder_start_token_id)
    shifted_input_ids = tf.concat([start_tokens, input_ids[:, :-1]], -1)
    shifted_input_ids = tf.where(
        shifted_input_ids == -100, pad_token_id, shifted_input_ids
    )

    if tf.executing_eagerly():
        assert_gte0 = tf.debugging.assert_greater_equal(
            shifted_input_ids, tf.constant(0)
        )

        with tf.control_dependencies([assert_gte0]):
            shifted_input_ids = tf.identity(shifted_input_ids)

    return shifted_input_ids


input_ids = tf.constant([[10, 20, 30, 40]], dtype=tf.int64)
pad_token_id = tf.constant(0, dtype=tf.int32)
decoder_start_token_id = tf.constant(2, dtype=tf.int32)

result = shift_tokens_right(input_ids, pad_token_id, decoder_start_token_id)
print("Result:", result)
