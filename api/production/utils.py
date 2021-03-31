

class ProcessFileXLSX:

    @staticmethod
    def separate_rows_from_pages(data) -> list:
        list_rows = list()

        for row in data.iter_rows():
            row_temp = list()
            for cell in row:
                row_temp.append(cell.value)

            list_rows.append(row_temp)
        return list_rows

    @staticmethod
    def clean_data(list_row: list = []) -> list:
        list_row_temp = list()
        count = 0

        for row in list_row:
            count += 1
            if row.count(None) >= len(row) - 1:
                # print('Valores Nulos ('+str(row.count(None))+') ---> ', row)
                continue

            else:
                list_row_temp.append(row)

        return list_row_temp
