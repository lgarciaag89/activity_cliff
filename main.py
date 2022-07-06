from normalizando_activity import GetCliff
import ComputeMatrix
from sin_normalizar_activity import GetCliffForMax

if __name__ == '__main__':
    models = ["clifft"]
    # names = ["train", "test", "merge_all"]
    names = ['merge_all_with_name']
    folder = "/home/potter/Doctorado/BASES_CONCENTRACION/Cebrafisch/48H/divido/no_coop/best_model/5539"

    for model in models:
        for name in names:
            print(name)

            mat, act = ComputeMatrix.readData(f'{folder}/{model}/{name}_{model}.csv')

            # functions = ["tanimoto","euclidean","manhattan"]
            functions = ["euclidean"]

            idxTest = [156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,
                       180,181,182,183,184,185,186,187,188,189,190,191,192,193,194]

            for function in functions:
                GetCliffForMax.searchCliff(mat, act, folder, model, name, function, idxTest)
                # GetCliff.searchNormCliff(mat, act, folder, model, name, function, idxTest)
