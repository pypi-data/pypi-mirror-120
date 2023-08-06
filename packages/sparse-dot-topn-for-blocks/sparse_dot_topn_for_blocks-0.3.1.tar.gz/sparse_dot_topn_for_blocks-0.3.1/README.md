# sparse\_dot\_topn\_for\_blocks: 

**sparse\_dot\_topn\_for\_blocks** is a slight variation of [**sparse\_dot\_topn**](https://github.com/ing-bank/sparse_dot_topn) which provides a fast way to perform sparse matrix multiplication followed by top-n selection and sorting in each row.

It has the same interface as [**sparse\_dot\_topn**](https://github.com/ing-bank/sparse_dot_topn) but additionally allows an array to be passed which will be updated with the maximum number of nonzero elements of each row of the result matrix with values above the given lower bound.  This is suitable for block-matrix multiplication.  That's all!