import os
from utils.excel_utils import ExcelUtils

excel_path = os.path.join(os.path.dirname(__file__),'../data/test_case.xlsx')

class DataFarmatConvertUtils():
    def __init__(self,excel_path,sheet_name):
        self.excel_doc = ExcelUtils(excel_path,sheet_name)
        self.excel_data_case = self.get_sheet_data_by_dic()


    def get_sheet_data_by_dic(self):
        """
        将excel中每一行的测试数据转换成字典格式，存放到列表中
        :return:
        """
        first_row = self.excel_doc.get_row_value(0)  # 列表类型
        count_cols = self.excel_doc.get_sheet_cols()
        count_rows = self.excel_doc.get_sheet_rows()
        case_list = []
        for r in range(1, count_rows):  # 控制行
            case_dic = {}
            for c in range(0, count_cols):  # 控制列
                case_dic[first_row[c].value] = self.excel_doc.get_value(r, c)
            case_list.append(case_dic)
        return case_list


    def case_steps_integrate(self):
        """
        get_sheet_data_by_dic()方法是将excel中每一行数据作为一个字典，放到列表
        case_steps_integrate()方法是把一个案例中多个步骤进行整合，
        改成{case1：[{step1},{step2}...],case2：[{step1},{step2}...]....}格式

        :return:
        """
        case_dic = {}
        for case in self.get_sheet_data_by_dic():
            case_name = case['测试用例编号']
            case_dic.setdefault(case_name, []).append(case)
        return case_dic


    def integrate_data_convert_list(self):
        """
        将上面case_steps_integrate()返回的数据格式优化转换成列表
        转成[
         {case_info:case1,
         case_value:[{step1},{step2}...]},
         {case_info:case2,
         case_info:[{step1},{step2}...]}....
        ]格式
        :return:
        """
        intergate_list = []
        for k,v in self.case_steps_integrate().items():
            intergate_dic = {}
            intergate_dic['case_info'] = k
            intergate_dic['case_value'] = v
            intergate_list.append(intergate_dic)
        return intergate_list



if __name__ == '__main__':
    convert_doc = DataFarmatConvertUtils(excel_path,'Sheet1')
    print(convert_doc.get_sheet_data_by_dic())
    print(convert_doc.case_steps_integrate())
    print(convert_doc.integrate_data_convert_list())