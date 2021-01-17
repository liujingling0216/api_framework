import os
import xlrd

excel_path = os.path.join(os.path.dirname(__file__),'../data/test_case.xlsx')

class ExcelUtils():
    def __init__(self,excel_path,sheet_name):
        self.wb = xlrd.open_workbook(excel_path)
        self.sheet_name = sheet_name
        self.ws = self.get_sheet()


    def get_sheet(self):
        ws = self.wb.sheet_by_name(self.sheet_name)
        return ws

    def get_row_value(self,row_index):
        row_value = self.ws.row(row_index)
        return row_value


    def get_sheet_rows(self):
        rows = self.ws.nrows
        return rows


    def get_sheet_cols(self):
        cols = self.ws.ncols
        return cols


    def __get_cell_value(self,row_index,col_index):
        value = self.ws.cell_value(row_index,col_index)
        return value


    def __get_merge_cells(self):
        merge_cells = self.ws.merged_cells
        return merge_cells


    def get_value(self,row_index,col_index):
        """
        这个方法既能获取普通单元格的内容又能获取合并单元格的内容
        :return:
        """
        cell_value = None
        merge_cell = self.__get_merge_cells()  # 数组包含四个元素（起始行，结束行，起始列，结束列）
        for (min_row,max_row,min_col,max_col) in merge_cell:
            if row_index>= min_row and row_index < max_row:
                if col_index >= min_col and col_index < max_col:
                    cell_value = self.__get_cell_value(min_row,min_col)
                    break    # 防止循环去进行判断出现值覆盖的情况
                else:
                    cell_value = self.__get_cell_value(row_index,col_index)
            else:
                cell_value = self.__get_cell_value(row_index,col_index)
        return cell_value


    # def get_data_by_dic(self):
    #     """
    #     将excel中每一组测试数据变成字典形式，放到列表中，封装到数据转换的类中
    #     :return:
    #     """
    #     first_row = self.ws.row(0)  # 列表类型
    #     case_list = []
    #     for r in range(1,self.get_sheet_rows()): # 控制行
    #         case_dic = {}
    #         for c in range(0,self.get_sheet_cols()): # 控制列
    #             case_dic[first_row[c].value]= self.get_value(r,c)
    #         case_list.append(case_dic)
    #     return case_list





if __name__ == '__main__':
    excel_doc = ExcelUtils(excel_path, 'Sheet1')
    print(excel_doc.get_sheet_cols())
    print(excel_doc.get_value(5,2))
    # print(excel_doc.get_data_by_dic())
