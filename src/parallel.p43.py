from minCiencia2Influx import *
import multiprocessing as mp

if __name__ == '__main__':
    # for k in relevantCSVs:
    #     print('Checking ' + k + ': ' + relevantCSVs[k])
    #     df = csv2line(relevantCSVs[k])
    if len(sys.argv) >= 3:
        print('Generando prod43 entre ' + sys.argv[1] + ' y ' + sys.argv[2])
        prod43_generator_validate_particles('../output/p43-', sys.argv[3:], from_year=sys.argv[1], to_year=sys.argv[2])
        ## paralelizamos por particula
        ## iterable of [(1,2), (3, 4)] results in [func(1,2), func(3,4)].
        my_iterable = []
        valid_particles = ['CO', 'MP10', 'MP2.5', 'NO2', 'O3', 'SO2']
        for vp in valid_particles:
            tupla = ('../output/p43-', vp, 'from_year=' + sys.argv[1], 'to_year=' + sys.argv[2])
            my_iterable.append(tupla)
        with mp.Pool(processes=6) as pool:
            results = pool.starmap(prod43_generator_validate_particles, iterable=my_iterable)
        print(results)


    elif len(sys.argv) == 1:
        print('Generando prod43 entre 2019 y 2020')
        prod43_generator('../output/p43-')