import scipy.stats as sps
import numpy as np

V = 33
N = 100 #общее количество заявок

#решение первого задания
def task_1():
    np.random.seed(12345)
    #через сколько времени придет первая заявка 
    t_z = 0.768
    #величина показательного распределения
    mu = 1.334 

    #если заявка попадет на вход, то сколько времени она будет обрабатываться
    #(моделирование процесса с помощью показательного распределения)
    #получается массив на 100 элементов
    times_of_services = sps.expon.rvs(scale=mu, size=N)

    #наступление первого события
    t_event = t_z 
    current_event_stat = 1
    current_sys_stat = 1

    #сколько времени выполняется текущая заявка
    remaining_sevr_time = times_of_services[0]

    #когда заяка "попросится" на выполнение
    remaining_demand_time = t_z

    #над какой заявкой по номеру происходит выполнение ивента
    t_j = 1
    #заявка на выполнении в СМО
    t_l = 1

    #количество выполненных заявок
    t_total = 0
    #количество отклоненных заявок
    t_rejected_total = 0
    #сколько СМО проработала
    works_total = 0
    #сколько СМО была в ожидании
    stays_total = 0.768

    table_1 = []
    table_2 = [None] * 101

     #добавляем в таблицу 1 прошлый ивент:
        #номер заявки
        #момент появления заявки в СМО
        #время обслуживания заявки в СМО
        #момент окончания обслуживания заявки в СМО
    table_2[0] = ([
        1,
        float("%0.5f" % t_z), 
        float("%0.5f" % remaining_sevr_time),
        float("%0.5f" %(remaining_sevr_time + t_z))])
    
    j = 1
    for i in range(2, 101):
        #добавляем в таблицу 1 прошлый ивент:
            #номер заявки
            #время, через которое начнется выполнение заявки 
            #тип события (1, 2 или 3)
            #текущее состояние СМО
            #оставшееся время выполнения заявки
            #через сколько в СМО появится новая заявка
            #над какой заявкой происходит выполнение в данный момент
        table_1.append([
            i - 1,
            float("%0.5f" % t_event),
            current_event_stat,
            current_sys_stat,
            float("%0.5f" % remaining_sevr_time),
            float("%0.5f" % remaining_demand_time),
            t_j])    
        
        #если время, оставшееся до конца выполнения заявки, меньше времени,
        #когда попросится следующая заявка, то у нас событие - конец выполнения
        if remaining_sevr_time < remaining_demand_time and current_sys_stat == 1:
            remaining_demand_time = t_z
            #вычисляем, когда СМО освободится
            t_event += remaining_sevr_time
            #из условия
            current_event_stat = 3
            current_sys_stat = 0
            #через сколько в СМО появится новая заявка
            remaining_demand_time -= remaining_sevr_time
            #оставшееся время обслуживания заявки
            #(поскольку СМО свободна, то оно равно -1)
            remaining_sevr_time = -1
            #ивент происходит над заявкой, которая выполняется в СМО
            t_j = t_l
            t_total += 1
            stays_total += remaining_demand_time
            
        elif remaining_sevr_time > remaining_demand_time:
            #добавляем время, когда просится следующая заявка
            t_event += remaining_demand_time
            #заявка попросилась, но была отклонена - это второй ивент
            current_event_stat = 2
            #поскольку прошло t_z времени
            remaining_sevr_time -= remaining_demand_time
            t_j = i - t_total 
            t_rejected_total += 1

            j += 1
            table_2[i] = [
                j,
                float("%0.5f" % t_event), 
                0,
                float("%0.5f" % t_event)]

        elif current_sys_stat == 0:
            #добавляем время, когда просится следующая заявка
            t_event += remaining_demand_time
            current_event_stat = 1
            current_sys_stat = 1
            remaining_sevr_time = times_of_services[t_total]
            remaining_demand_time = t_z
            t_j = i - t_total
            t_l = t_j

            j += 1
            table_2[i - 1] = [
                j,
                float("%0.5f" % t_event), 
                float("%0.5f" % remaining_sevr_time),
                float("%0.5f" % (remaining_sevr_time + t_event))]

    table_1.append([
            100,
            float("%0.5f" % t_event),
            current_event_stat,
            current_sys_stat,
            float("%0.5f" % remaining_sevr_time),
            float("%0.5f" % remaining_demand_time),
            t_j])

    print("ТАБЛИЦА №1")
    for i in range(0, 100):
        print(table_1[i])

    print("-------------------------")
    print("ТАБЛИЦА №2")
    table_2 = l = [i for i in table_2 if i is not None]
    sorted(table_2)
    for i in range(0, len(table_2)):
        print(table_2[i])

    print("-------------------------")
    if table_1[-1][2] == 3: 
        stays_total -= table_1[-1][5]
    print("ТАБЛИЦА №3")
    print(str(0) + " | " 
          + str(t_total) + " | "
          + str(float("%0.5f" % (t_total/100))) + " | "
          + str(float("%0.5f" % stays_total)) + " | "
          + str(float("%0.5f" % (stays_total/t_event))) + " | ")

    works_total = t_event - stays_total
    print(str(1) + " | " 
          + str(100 - t_total) + " | "
          + str(float("%0.5f" % ((100 - t_total)/100))) + " | "
          + str(float("%0.5f" % works_total)) + " | "
          + str(float("%0.5f" % (works_total/t_event))) + " | ")

    print("  | " 
          + str(100) + " | "
          + str(1.0) + " | "
          + str(float("%0.5f" %t_event)) + " | "
          + str(float("%0.5f" %((stays_total/t_event) + (works_total/t_event)))) + " | ")
    
    print("-------------------------")
    print("Всего заявок поступило в СМО на интервале: " + str(len(table_2)))
    print("Всего обслужено заявок: " + str(t_total))
    print("Всего отклонено заявок: " + str(t_rejected_total))
    print("Доля отклонённых заявок: " + str(float("%0.5f" % (t_rejected_total/len(table_2)))))
    print("Коэффициент простоя прибора: " + str(float("%0.5f" % (stays_total/t_event))))

task_1()