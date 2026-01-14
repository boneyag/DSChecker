import tensorflow as tf

tf.random.set_seed(0)
x = tf.constant([1, 2, 0, 2, 1, 1, 0, 1], dtype=tf.int64)
mask = tf.constant([1, 1, 0, 1, 1, 1, 0, 1], dtype=tf.int64)

output = tf.where(x == mask, tf.cast(tf.fill(tf.shape(x), -100), x.dtype), x)

print(output)
