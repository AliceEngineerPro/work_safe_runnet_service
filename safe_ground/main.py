
from math import pi, sin, cos, degrees
import numpy as np
import random
import cmath
import copy
import matplotlib.pyplot as plt


def run(ground_r_big=100, safe_r=0.05, Number_of_Angle_segments=360, Number_of_radius_segments=100):
    # random.seed(2)
    # 区域整体半径
    # ground_r_big = 100
    # # 安全区半径
    # safe_r = 0.05
    # # 角度分割数量
    # Number_of_Angle_segments = 360
    # # 半径分割数量
    # Number_of_radius_segments = 100
    # 所有半径列表
    ground_r_array = np.linspace(0, ground_r_big, Number_of_radius_segments + 1)  # +1是因为101个边才能构建100个扇形
    # 角度分割
    point_array = np.linspace(0, 359, Number_of_Angle_segments)

    # 保存扇形的位置,扇形编号:{左上,右上,左下,右下}
    sector_dict = {}
    # 获得所有扇形坐标,对扇形进行编号
    for ground_r in range(ground_r_array.shape[0] - 1):  # 遍历半径
        for point in range(point_array.shape[0]):  # 遍历弧度
            # 初始化扇形4个参数
            # 半径
            r_s = ground_r_array[ground_r]
            r_b = ground_r_array[ground_r + 1]

            # 角度
            p_s = point_array[point]
            if point == point_array.shape[0] - 1:
                p_b = point_array[0]
            else:
                p_b = point_array[point + 1]
            # 这里的角度获得的是数值型,360-->2π,需要进行这样的转换才能进行计算
            # θ/360=x/2π---->x(弧度表示) = θ/180*π
            top_left = (r_b * cos(p_b / 180 * pi), r_b * sin(p_b / 180 * pi))  # 左上角点
            top_right = (r_b * cos(p_s / 180 * pi), r_b * sin(p_s / 180 * pi))  # 右上角点
            down_left = (r_s * cos(p_b / 180 * pi), r_s * sin(p_b / 180 * pi))  # 左下角点
            down_right = (r_s * cos(p_s / 180 * pi), r_s * sin(p_s / 180 * pi))  # 右下角点
            # 扇形编号 左下,右下,左上,右上
            sector_dict[360 * ground_r + point] = [down_left, down_right, top_left, top_right]

    # 构建障碍物(10个)  真实环境下不需要进行构建,这个列表会直接传入的,但是要转换下坐标(转为以圆心为原点的坐标系)
    barrier_list = []
    # 随机 θ  半径
    for i in range(100):
        temp_angle = random.randint(0, 359)
        temp_r = random.randint(0, ground_r_big)
        # 计算这个点的坐标,并加入障碍物列表
        barrier_list.append((temp_r * cos(temp_angle), temp_r * sin(temp_angle)))

    # 被标记的扇形,可能有重复的,故使用集合
    flag_sector_set = set()
    # 遍历障碍物
    for barrier in barrier_list:
        # 在障碍物的安全区范围取100个点,获得这100个点相对于障碍物的坐标,然后再转换为相对于圆心的坐标,计算在哪个扇形中
        for i in range(100):
            temp_angle = random.randint(0, 359)
            temp_r = random.uniform(0, safe_r)
            # 随机点相对于障碍物的坐标
            coord = (temp_r * cos(temp_angle), temp_r * sin(temp_angle))
            # 将随机点相对于障碍物的坐标转换为该点相对于圆心的坐标
            coord_by_circle = (coord[0] + barrier[0], coord[1] + barrier[1])
            # 获得该坐标的极坐标(角度,半径)
            cn = complex(*coord_by_circle)
            r_temp, radian_temp = cmath.polar(cn)
            # 弧度转为角度--可能出现负值,需要模360
            temp_ponit = degrees(radian_temp) % 360
            # flag_sector = int(r_temp) * 360 + int(temp_ponit)
            # flag_sector_set.add(flag_sector)
            # 已经获得这个点的角度,半径
            # 计算这个点在哪个扇形中
            # 单圈数量*当前所在的圈层数+角度偏差
            # 当前圈数 = r_temp(当前半径)//[ground_r_big(总半径)/Number_of_radius_segments(半径分割数量)]
            # flag_sector = int(r_temp) * 360 + int(temp_ponit)
            now_turns = float(r_temp) // (float(ground_r_big) / int(Number_of_radius_segments))
            # 在当前圈时,根据角度进行编号
            now_angle = Number_of_Angle_segments / 360 * temp_ponit
            # 圈数*每圈的数量*角度偏差
            flag_sector = int(now_turns * Number_of_Angle_segments + now_angle)
            # 有可能产生的随机点在圆外面,这部分不需要采用
            if flag_sector > 36000:
                continue
            flag_sector_set.add(flag_sector)

    # flag_sector_set:不能作业区,  这个 范围需要加上最下面的一圈
    flag_sector_set = list(flag_sector_set) + [i for i in range(Number_of_Angle_segments)]
    # 保存所有4个点上的扇形的编号
    big_sector_list = []
    big_sector_dict = {}
    # 可视化函数,暂时不需要了,设置为100,360才能使用
    # temp = np.zeros((100, 360))
    # for flag_sector in flag_sector_set:
    #     # print((flag_sector, flag_sector // 360, flag_sector % 360))
    #     temp[flag_sector // 360, flag_sector % 360] = 1
    # def get_point_location(point):
    #     return (point // 360, point % 360)

    # 遍历被标记的格子
    for flag_sector in flag_sector_set:
        # for flag_sector in [25920]:
        # print(flag_sector)
        # (1)从该点开始向上查找(+360 等于该格子编号的为该点上面的点),直到找到下一个被标记的点为止,未找到则到边界为止
        # (2)分别向左右查找,左右再向上进行查找,直到左边,右边找到了下一个被标记的点
        # (3)此范围为需要筛选出的范围,获得该范围的四个顶角坐标,并保存其面积
        # top_gird, left_gird, right_gird = 0, 0, 0
        # 1.向上查找  top_gird:上方的点
        # 循环标志
        recycling_symbol = 1
        while True:
            new_grid = flag_sector + Number_of_Angle_segments * recycling_symbol
            top_gird = new_grid
            # 找到了上面被标记的点,那么就返回
            if new_grid in flag_sector_set:
                # 找到的那一行不能取,向前退一行
                top_gird -= Number_of_Angle_segments
                break
            # 或者到顶了
            if new_grid > Number_of_Angle_segments * Number_of_radius_segments - 1:
                # 击中的那一行不选择,后退一行
                top_gird -= Number_of_Angle_segments
                break
            recycling_symbol += 1
        # 被标记区域上面还有被标记的,那么是不可能有面积的
        if top_gird == flag_sector:
            continue
        # 2.向左查找,同时需要向左边的上方查找 new_grid_left 标记左边的点
        # 起始点为top_gird左边的点
        left_flag = False
        left_flag_sector = copy.deepcopy(top_gird)
        # 向左移动的数量:
        left_move_count = 0
        for i in range(1, Number_of_Angle_segments + 1):
            recycling_symbol = 0
            # 获得标记点左边的点  只能在本圈中查找,即如果整除为0时,将数字加360,继续筛选
            if left_flag_sector // Number_of_Angle_segments == (left_flag_sector - 1) // Number_of_Angle_segments:
                left_flag_sector -= 1
            else:
                left_flag_sector = left_flag_sector - 1 + Number_of_Angle_segments
            # if left_flag_sector % Number_of_Angle_segments == 0:
            #     left_flag_sector += Number_of_Angle_segments
            while True:
                new_grid = left_flag_sector - Number_of_Angle_segments * recycling_symbol
                left_gird = new_grid
                if new_grid in flag_sector_set:
                    # 可能找到最底部了(和障碍物在一行的格子,这是不能取的)
                    if new_grid // Number_of_Angle_segments == flag_sector // Number_of_Angle_segments:
                        break
                    else:
                        # 找到了左边上面被标记的格子,那么返回,并不继续向左查找了
                        left_flag = True
                        break
                # 或者到底部(选择障碍物所在的行)
                if new_grid // Number_of_Angle_segments == flag_sector // Number_of_Angle_segments:
                    break
                recycling_symbol += 1
            left_move_count += 1
            if left_flag:
                # 在当前列找到了,所以当前列不能取
                # 同样需要判断-1后是否会跳到下一行去了

                if left_flag_sector // Number_of_Angle_segments == (top_gird + 1) // Number_of_Angle_segments:
                    left_flag_sector += 1
                else:
                    left_flag_sector = left_flag_sector + 1 - Number_of_Angle_segments
                if left_flag_sector == Number_of_Angle_segments * Number_of_radius_segments:
                    left_flag_sector -= Number_of_Angle_segments

                # left_flag_sector += 1
                break

        # 3.向右查找,同时需要向右边的上方查找 new_grid_right 右边被标记的点
        right_flag = False
        right_flag_sector = copy.deepcopy(top_gird)
        # 向右移动点的数量
        right_move_count = 0
        for i in range(1, Number_of_Angle_segments + 1):
            recycling_symbol = 0
            # 获得标记点右边的点 只能在本圈中查找,即如果整除为0时,将数字减360,继续筛选
            if right_flag_sector // Number_of_Angle_segments == (right_flag_sector + 1) // Number_of_Angle_segments:
                right_flag_sector += 1
            else:
                right_flag_sector = right_flag_sector + 1 - Number_of_Angle_segments
            # if right_flag_sector % Number_of_Angle_segments == 0:
            #     right_flag_sector += Number_of_Angle_segments

            while True:
                new_grid = right_flag_sector - Number_of_Angle_segments * recycling_symbol
                right_gird = new_grid
                if new_grid in flag_sector_set:
                    if new_grid // Number_of_Angle_segments == flag_sector // Number_of_Angle_segments:
                        break
                    # 找到了左边上面被标记的格子,那么返回,并不继续向左查找了
                    right_flag = True
                    break
                # 或者到顶了
                if new_grid // Number_of_Angle_segments == flag_sector // Number_of_Angle_segments:
                    break
                recycling_symbol += 1
            right_move_count += 1
            if right_flag:
                # 在当前列找到了,所以当前列不能取
                # 同样需要判断-1后是否会跳到下一行去了

                if right_flag_sector // Number_of_Angle_segments == (right_flag_sector - 1) // Number_of_Angle_segments:
                    right_flag_sector -= 1
                else:
                    right_flag_sector = right_flag_sector - 1 + Number_of_Angle_segments
                # right_flag_sector -= 1
                break
        # 四个点位置:左下,右下(距离作业点最近的下边界)
        #            左上,右上(距离作业点最远的下边界)
        # 添加保存第五个数据,扫过的格子的数量.原因:使用极坐标计算相对位置,可能会出错,直接减的话可能会减错范围
        safe_area = (
            # 左下
            (flag_sector // Number_of_Angle_segments) * Number_of_Angle_segments +
            left_flag_sector % Number_of_Angle_segments + Number_of_Angle_segments,
            # 右下
            (flag_sector // Number_of_Angle_segments) * Number_of_Angle_segments +
            right_flag_sector % Number_of_Angle_segments + Number_of_Angle_segments,
            # 左上              右上          移动的格子数量 因为2边都多算了1个,需要减掉
            left_flag_sector, right_flag_sector, right_move_count + left_move_count - 1)

        big_sector_list.append(safe_area)
        # 保存  障碍点:4个边界
        big_sector_dict[flag_sector] = safe_area

    # 定义角度的转换,因为极坐标转换出来是[-π,π],我们的角度是[0,2π],
    # 需要进行转换,将转换出来小于0的数据x,使用(2π-θ)进行替代
    def angle_conversion(angle):
        if angle < 0:
            return 2 * pi + angle
        else:
            return angle

    # 返回的数据
    result_list = []
    # 保存所有面积,画一个直方图
    temp_list = []
    # 遍历符合的扇形区域,计算其面积
    # 扇形面积计算公式:角度制:（n/360）πR²
    # 用左边减去右边(新边减去旧边)
    for big_sector in big_sector_dict.keys():
        # for big_sector in big_sector_list:
        # 1.4个坐标转为极坐标,分别取对应的点,计算角度和半径,再计算面积
        # 小扇形保存:左下,右下,左上,右上
        # 先取出所属的扇形,再取出所属的位置
        # 左上点
        sector_left_up = sector_dict[big_sector_dict[big_sector][2]][2]
        # 左下点
        sector_left_down = sector_dict[big_sector_dict[big_sector][0]][0]
        # 右上点
        sector_right_up = sector_dict[big_sector_dict[big_sector][3]][3]
        # 右下点
        sector_right_down = sector_dict[big_sector_dict[big_sector][1]][1]
        # 直角坐标转极坐标
        # 获得四个顶点对应的极坐标
        # 半径,弧度
        # 左上
        polar_coordinates_sector_left_up_r, polar_coordinates_sector_left_up_radian = cmath.polar(
            complex(*sector_left_up))
        # 左下
        polar_coordinates_sector_left_down_r, polar_coordinates_sector_left_down_radian = cmath.polar(
            complex(*sector_left_down))
        # 右上
        polar_coordinates_sector_right_up_r, polar_coordinates_sector_right_up_radian = cmath.polar(
            complex(*sector_right_up))
        # 右下
        polar_coordinates_sector_right_down_r, polar_coordinates_sector_right_down_radian = cmath.polar(
            complex(*sector_right_down))
        # 面积计算  180*弧度/π
        # 移动格子的数量  数量乘以当初设置的角度分割度数,就是实际的扇形圆周角度数
        count = big_sector_dict[big_sector][4]
        point_temp = count / Number_of_Angle_segments
        # 计算大扇形面积
        # 使用弧度制计算  180*弧度/π
        # S_big = ((angle_conversion(polar_coordinates_sector_left_up_radian) - angle_conversion(
        #     polar_coordinates_sector_right_up_radian)) * (polar_coordinates_sector_left_up_r) ** 2) * 1 / 2
        # # 计算小扇形面积
        # S_small = ((angle_conversion(polar_coordinates_sector_left_up_radian) - angle_conversion(
        #     polar_coordinates_sector_right_up_radian)) * (polar_coordinates_sector_left_down_r) ** 2) * 1 / 2
        # 使用角度制计算  （n/360）πR²
        S_big = pi * (polar_coordinates_sector_left_up_r ** 2) * point_temp
        # 计算小扇形面积
        S_small = pi * (polar_coordinates_sector_left_down_r ** 2) * point_temp

        S_sector = abs(S_big) - abs(S_small)
        # 保存4个点的坐标,面积----左下,右下,左上,右上,面积
        temp_sector = [sector_left_down, sector_right_down, sector_left_up, sector_right_up, S_sector]
        result_list.append(temp_sector)
        temp_list.append(S_sector)
    plt.hist(temp_list, 100)
    plt.show()


if __name__ == '__main__':
    run()
