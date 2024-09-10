import requests, json


def call():
    headers = {
        "Origin": "http://attend.yc.ac.kr:18080",
        "Connection": "keep-alive",  # 연결 유지
        "Content-Length": "25",  # 요청 본문의 길이
        "Accept": "*/*",  # 모든 콘텐츠 타입 허용
        "X-Requested-With": "XMLHttpRequest",  # XMLHttpRequest를 통해 요청
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  # 요청 본문의 콘텐츠 타입
        "Accept-Encoding": "gzip, deflate",  # 압축된 응답 허용
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",  # 언어 설정 (한국어, 영어)
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G998B Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.122 Safari/537.36",
    }
    login_url = "http://portal.yc.ac.kr/enview/user/loginProcess.face"
    with open("idpw.json", "r", encoding="UTF-8") as f:
        payload = json.load(f)
    print("idpw is Loaded")
    session = requests.Session()
    response = session.post(login_url, data=payload)
    if response.ok:
        print("로그인 성공!")
        session.get(
            "http://sso.yonam.ac.kr:81/enpass/login?gateway=client&epAppId=YonamCommon&service=http://attend.yc.ac.kr:18080/Yc_Attend/user/main/view.do"
        )
        cookies_json = {cookie.name: cookie.value for cookie in session.cookies}
        url = "http://attend.yc.ac.kr:18080/Yc_Attend/user/square/menu/menuData.json?rowCount=1&currentPage=1"  # sql 요청
        menu = session.get(url, headers=headers, cookies=cookies_json)
        menus = json.loads(menu.text)

        sorted = menus["lunchList"]["list"]
        date = f'{sorted[0]["lunchDate"]} {sorted[0]["lunchWeek"]}'  # 날짜와 요일

        print(f"{date}요일 학식")
        for i in range(len(sorted)):
            print(f'{sorted[i]["lunchTimeNm"]}{sorted[i]["lunchType"]}')
            print(f'메인: {sorted[i]["lunchMenu"]}')
            if len(str(sorted[i]["lunchDetail"])) > 1:
                print(f'서브: {sorted[i]["lunchDetail"]}')
            print("=" * 80)

    else:
        print("로그인 실패:", response.status_code)


print(call())
