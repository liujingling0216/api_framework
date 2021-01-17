import os
import xlrd

excel_path = os.path.join(os.path.dirname(__file__),'../data/test_case.xlsx')

ws = xlrd.open_workbook(excel_path)
wb = ws.sheet_by_name('Sheet1')


#获取合并单元格的值
def cell_value(row,col):
    merge_cell = wb.merged_cells  # 数组包含四个元素（起始行，结束行，起始列，结束列）
    for (min_row,max_row,min_col,max_col) in merge_cell:
        if row >= min_row and row < max_row:
            if col >= min_col and col < max_col:
                cell_value = wb.cell(min_row,min_col)
                break
            else:
                cell_value = wb.cell(row,col)
        else:
            cell_value = wb.cell_value(row,col)

    return cell_value


def get_sheet_data_by_dic():
    """
    数据形式转换
    :return:
    """
    first_row = wb.row(0)  # 列表类型
    ncols = wb.ncols
    nrows = wb.nrows
    case_list = []
    for r in range(1,nrows): # 控制行
        case_dic = {}
        for c in range(0,ncols): # 控制列
            case_dic[first_row[c].value]= cell_value(r,c)
        case_list.append(case_dic)
    return case_list


def case_steps_integrate():
    """
    将多个步骤整合成一个案例，处理成{case1：[{step1},{step2}...],case2：[{step1},{step2}...]....}格式
    :return:
    """
    case_dic = {}
    for case in get_sheet_data_by_dic():
        case_name = case['测试用例编号']
        case_dic.setdefault(case_name,[]).append(case)
    return case_dic


def integrate_data_convert_list():
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
    for k,v in case_steps_integrate().items():
        intergate_dic = {}
        intergate_dic['case_info'] = k
        intergate_dic['case_value'] = v
        intergate_list.append(intergate_dic)
    return intergate_list





if __name__ == '__main__':
    for j in range(1,5):#控制行
        for i in range(0,4):#控制列
            print(cell_value(j,i))


    print(get_sheet_data_by_dic())
    print(case_steps_integrate())
    print(integrate_data_convert_list())


