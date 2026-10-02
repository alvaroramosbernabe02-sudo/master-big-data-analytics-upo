create 'clientes_dist', 'datos', SPLITS => ['g', 'n']
put 'clientes_dist', 'a-001', 'datos:nombre', 'Ana'
put 'clientes_dist', 'h-002', 'datos:nombre', 'Hugo'
put 'clientes_dist', 'p-003', 'datos:nombre', 'Paula'
put 'clientes_dist', 'z-004', 'datos:nombre', 'Zoe'
scan 'clientes_dist'
list_regions 'clientes_dist'
flush 'clientes_dist'
exit
