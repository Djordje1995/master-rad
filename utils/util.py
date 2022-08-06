from utils import constant, csv_handler


def get_brands_with_modules():
    all_brands = {}
    data = csv_handler.get_learning_data_serbian()
    for row in data:
        marka = row[constant.MODEL].split(":")[0].strip()
        if marka not in list(all_brands.keys()):
            all_brands[marka] = []
        model = row[constant.MODEL].split(":")[1].strip()
        if model not in all_brands[marka]:
            all_brands[marka].append(model)
    return all_brands
