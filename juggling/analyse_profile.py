import pstats


p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(15)
