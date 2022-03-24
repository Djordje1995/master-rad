import csv
import constant


def read_row(row, header):
    row_dict = {}
    i = 0
    for column in row:
        row_dict[header[i]] = column
        i += 1
    return row_dict


def get_header():
    return [constant.BRAND,
            constant.MODEL,
            constant.YEAR,
            constant.PRICE,
            constant.TRANSMISSION,
            constant.MILEAGE,
            constant.FUEL_TYPE,
            constant.TAX,
            constant.MPG,
            constant.ENGINE_SIZE]


def read_csv(file_name):
    data = []
    with open(constant.DATA_FOLDER + file_name + constant.CSV) as csv_data:
        csv_reader = csv.reader(csv_data)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                row_dict = read_row(row, get_header())
                data.append(row_dict)
                line_count += 1
    return data


def write_rows(writer, data, header):
    writer.writerow(header)
    is_header = True
    for row in data:
        if is_header:
            is_header = False
            continue
        values = row.values()
        writer.writerow(list(values))


def write_csv(data, file_name, header):
    with open(constant.DATA_FOLDER + file_name + constant.CSV, mode='w', newline='\n') as file:
        writer = csv.writer(file)
        write_rows(writer, data, header)

