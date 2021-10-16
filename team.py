import numpy as np
import pandas as pd
import random


def select_leaders(participants, results, heads, mentors, OBs, team_n): # 조장 하실 분..?
    heads_n = len(heads)
    mentors_n = len(mentors)
    OBs_n = len(OBs)

    if(team_n > heads_n) : # 회장단으로 조장 채우기 부족할 때
        leaders = heads # 일단 회장단으로 조장 채움

        if((team_n-heads_n) > mentors_n) : # 회장단+멘토진으로 조장 채우기 부족할 때
            if (team_n-heads_n-mentors_n) > OBs_n : # 회장단+멘토진+기존기수로 조장 채우기 부족할 때
                print("조졌다..!")
                quit() # 이럼 이제 좆된거임

            # 회장단 + 멘토진으로 조장을 채움
            leaders = pd.concat([leaders, mentors]) 

            # 부족한 조장 수를 기존 기수에서 랜덤 비복원 추출로 채움
            leaders = pd.concat([leaders, OBs.sample(n = (team_n-heads_n-mentors_n), replace=False, random_state = RANDOM) ])

        else: # 회장단+멘토진으로 조장 채울 수 있을 때
            # 부족한 조장 수를 멘토진에서 랜덤 비복원 추출로 채움
            leaders = pd.concat([leaders, mentors.sample(n = (team_n-heads_n), replace=False, random_state = RANDOM) ])

    else: # 회장단 수 < 팀 수 
        for i in range(team_n):
            # 회장단에서 조장을 랜덤 비복원 추출로 채움
            leaders = heads.sample(n = team_n, replace=False, random_state = RANDOM)
    
    
    # 조장들의 정보를 결과에 추가 후, 참가자 명단에서 조장들 삭제
    results_new = results

    for leader in leaders["이름"]:
        index = participants[participants["이름"]==leader].index

        if participants.loc[index, ['백신']].to_numpy()[0][0] == True:
            yes = 1
            no = 0
        else:
            yes = 0
            no = 1
        team = {'조장':leader, '조원':[leader], '기존':1, '신입':0, '접종':yes, '미접종':no, '총':1}
                
        results_new = results_new.append(team, ignore_index=True)
        participants = participants.drop(index)
    
    # 조를 한번 섞어준다
    results_new = results_new.sample(frac=1, random_state = RANDOM).reset_index(drop=True)

    return participants, results_new, leaders




def fill_non_vac(participants, results, team_n) : # 미접종자 채우기
    n = 0
    
    while len(participants.loc[participants["백신"]==False, :]) != 0: # 남은 참가자수가 없어질 때 까지 반복
        n += 1 # 목표로 하고자 하는 미접종자 수
        
        results = results.sort_values('총', ascending=True).reset_index(drop=True)
        
        for i in range(team_n):
            if (results.loc[i, ['미접종']].to_numpy()[0]<n) and len(participants.loc[participants["백신"]==False, :]) != 0: 
                # 목표로 하고자 하는 미접종자 수보다 적으면서 미접종자가 남아있을 경우에만

                # 1명의 미접종 인원을 랜덤 비복원 추출
                temp = participants.loc[participants["백신"]==False, :].sample(n = 1, replace=False, random_state = RANDOM)
                
                name = temp["이름"].to_numpy()[0] # 이름 값 받아오기
                index = participants[participants["이름"]==name].index
                    
                results.loc[i, ['조원']].to_numpy()[0].append(name) # 조원에 추가
                        
                # 기존/신입 인원 수 추가
                if participants.loc[index, ['구분']].to_numpy()[0][0] == '신입':
                    results.loc[i, ['신입']] += 1
                else:
                    results.loc[i, ['기존']] += 1

                results.loc[i, ['미접종']] += 1 # 미접종 인원 수 추가
                results.loc[i, ['총']] += 1 # 총 인원 수 업데이트

                # 선택한 인원을 참가자 명단에서 삭제
                participants = participants.drop(index)
        
        # 조를 한번 섞어준다
        results = results.sample(frac=1, random_state = RANDOM).reset_index(drop=True)

    return participants, results




def fill_vac(participants, results, team_n) : # 접종자 채우기
    n = 0
    
    while len(participants.loc[participants["백신"]==True, :]) != 0: # 남은 참가자수가 없어질 때 까지 반복
        n += 1 # 목표로 하고자 하는 미접종자 수
        
        results = results.sort_values('총', ascending=True).reset_index(drop=True) # 인원수대로 정렬 (인원 적은 팀에 우선적으로 배정하기 위함)

        for i in range(team_n):
            if (results.loc[i, ['접종']].to_numpy()[0]<n) and len(participants.loc[participants["백신"]==True, :]) != 0:
                # 목표로 하고자 하는 접종자 수보다 적으면서 접종자가 남아있을 경우에만

                # 1명의 접종 인원을 랜덤 비복원 추출
                temp = participants.loc[participants["백신"]==True, :].sample(n = 1, replace=False, random_state = RANDOM)
                
                name = temp["이름"].to_numpy()[0] # 이름 값 받아오기
                index = participants[participants["이름"]==name].index
                    
                results.loc[i, ['조원']].to_numpy()[0].append(name) # 조원에 추가
                        
                # 기존/신입 인원 수 추가
                if participants.loc[index, ['구분']].to_numpy()[0][0] == '신입':
                    results.loc[i, ['신입']] += 1
                else:
                    results.loc[i, ['기존']] += 1

                results.loc[i, ['접종']] += 1 # 접종 인원 수 추가
                results.loc[i, ['총']] += 1 # 총 인원 수 업데이트

                # 선택한 인원을 참가자 명단에서 삭제
                participants = participants.drop(index)

        # 조를 한번 섞어준다
        results = results.sample(frac=1, random_state = RANDOM).reset_index(drop=True)

    return participants, results




results = pd.read_excel('./result.xlsx') # 여기에 결과 쓸 거임
results = pd.DataFrame(columns = ['조장', '조원', '기존', '신입', '접종', '미접종', '총']) # columns 설정
participants = pd.read_excel('./참가자명단.xlsx').sort_values(by="이름").reset_index(drop=True) # 참가자명단 이름 순으로 정렬 후 인덱스 리셋


print('======참가자 명단======')
print(participants)
n = len(participants)
print ('총 인원 : ', n, '명')


print("=========================")
vac_participants = participants.loc[participants["백신"]==True, :]
vac_n = len(vac_participants)
print("접종자 : ", vac_n, "명")
non_vac_participants = participants.loc[participants["백신"]==False, :]
non_vac_n = len(non_vac_participants)
print("미접종자 : ", non_vac_n, "명")


print("======입력 후 엔터======") # 거리두기 단계에 따른 변수
valible_vac_n = int(input("최대로 모일 수 있는 백신 접종자 수 : "))
valible_non_vac_n = int(input("최대로 모일 수 있는 백신 미접종자 수 : "))


print("====숫자만 치고 엔터====") # 시드값은 잡담방에서 임의로 받는다
need_seed = int(input("시드 값 사용? (1. ㅇㅇ 사용, 2. ㄴㄴ 걍 쌩으로 랜덤) : "))
if(need_seed==1):
    RANDOM = int(input("시드 값으로 사용할 0 ~ 4294967295 사이 정수 입력 : "))
else:
    RANDOM = random.randint(0,2**32-1) # 난수
print("=========================")


# 회장단, 멘토진, 기존기수 저장
heads = participants.loc[participants["구분"]=="회장단", :]
heads_n = len(heads)
mentors = participants.loc[participants["구분"]=="멘토", :]
mentors_n = len(mentors)
OBs = participants.loc[participants["구분"]=="기존", :]
OBs_n = len(OBs)


if (vac_n/non_vac_n) > (valible_vac_n/valible_non_vac_n) : # 접종자가 꽤 있는 경우
    if vac_n%valible_vac_n == 0:
        team_n = vac_n//valible_vac_n
    else:
        team_n = vac_n//valible_vac_n + 1

    print("총", team_n, "팀")

    participants, results, leaders =  select_leaders(participants, results, heads, mentors, OBs, team_n)
    # 접종자 수 기준으로 팀 개수 설정. 접종자 먼저 채우고 미접종자 채우기
    participants, results = fill_non_vac(participants, results, team_n)
    participants, results = fill_vac(participants, results, team_n)

else: # 접종자가 많지 않은 경우
    if vac_n%valible_vac_n == 0:
        team_n = non_vac_n//valible_non_vac_n
    else:
        team_n = non_vac_n//valible_non_vac_n + 1
    print("총", team_n, "팀")

    participants, results, leaders =  select_leaders(participants, results, heads, mentors, OBs, team_n)
    # 미접종자 수 기준으로 팀 개수 설정. 미접종자 먼저 채우고 접종자 채우기
    participants, results = fill_non_vac(participants, results, team_n)
    participants, results = fill_vac(participants, results, team_n)


print("========================결과========================")
print(results)


results.to_excel('./result.xlsx') # 엑셀 파일로 저장