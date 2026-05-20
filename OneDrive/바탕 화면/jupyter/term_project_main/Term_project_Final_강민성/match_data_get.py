import requests
import os
import pandas as pd
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv('PUBG_API_KEY.env') 
apiKey = os.getenv('PUBG_API_KEY')
headers = {
    "Authorization": f"Bearer {apiKey}",
    "Accept": "application/vnd.api+json"
}

# 1. 플레이어 ID 및 매치 ID 가져오기
def getPlayerData(playerName):
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={playerName}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[{playerName}] Error: {response.status_code}")
        return None, []

    data = response.json().get("data", [])
    if not data:
        print(f"[{playerName}] No data found.")
        return None, []

    player = data[0]
    accountId = player.get("id")
    matches = player.get("relationships", {}).get("matches", {}).get("data", [])
    matchIds = [match["id"] for match in matches if "id" in match]

    return accountId, matchIds


# 2. 매치 데이터 가져오기
def getMatchData(matchId):
    url = f"https://api.pubg.com/shards/steam/matches/{matchId}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# 3. 해당 매치에서 플레이어 통계 추출
def extractPlayerStats(matchData, accountId):
    for entry in matchData.get("included", []):
        if entry.get("type") == "participant":
            participant = entry.get("attributes", {}).get("stats", {})
            if participant.get("playerId") == accountId:
                return {
                    "name": participant.get("name", "Unknown"),
                    "kills": participant.get("kills", 0),
                    "timeSurvived": participant.get("timeSurvived", 0),
                    "rank": participant.get("winPlace", 0)
                }
    return None


# 4. 여러 매치 통계 수집
def getPlayerStats(accountId, matchIds, limit=20):
    stats = []
    count = 0

    for matchId in matchIds:
        if count >= limit:
            break
        matchData = getMatchData(matchId)
        if matchData:
            stat = extractPlayerStats(matchData, accountId)
            if stat:
                stats.append(stat)
                count += 1
    return stats


# 5. 전체 플레이어 리스트 설정
players = {
    "Zucchini__": "주키니",
    "obbayasalido": "미라클",
    "rnsflaqh": "군림보",
    "kimblue": "김블루"
}

# 6. 통합 데이터 수집
allStats = []

for nickname, display_name in players.items():
    print(f"🔄 {display_name} 데이터 수집 중...")
    accountId, matchIds = getPlayerData(nickname)
    if accountId and matchIds:
        stats = getPlayerStats(accountId, matchIds, limit=20)
        for stat in stats:
            stat["name_kor"] = display_name  # 한글 이름 추가
        allStats.extend(stats)

# 7. CSV 파일 저장
def saveStatsToCsv(stats, fileName="player_stats.csv"):
    if stats:
        df = pd.DataFrame(stats)
        df.to_csv(fileName, index=False)
        print(f"\n✅ CSV 저장 완료: {fileName}")
    else:
        print("⚠️ 저장할 데이터가 없습니다.")

saveStatsToCsv(allStats)
