from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from bs4 import BeautifulSoup
import time
from decimal import Decimal, getcontext, InvalidOperation

# 設定小數點位數
getcontext().prec = 10

# 設定東海大學的登入網址和成績頁面的網址
login_url = "https://fsis.thu.edu.tw/mosi/ccsd3/index.php?job=stud&loginn=&r=https://fsis.thu.edu.tw/"
grades_url = "https://fsiso.thu.edu.tw/wwwstud/STUD_V6/COURSE/rcrd_all_gpa.php"

# 登入的帳號和密碼
username = "s10350106"
password = "aa920216"

# GPA 對應表
gpa_conversion = {
    'A+': Decimal('4.3'), 'A': Decimal('4.0'), 'A-': Decimal('3.7'),
    'B+': Decimal('3.3'), 'B': Decimal('3.0'), 'B-': Decimal('2.7'),
    'C+': Decimal('2.3'), 'C': Decimal('2.0'), 'C-': Decimal('1.7'),
    'D+': Decimal('1.3'), 'D': Decimal('1.0'), 'D-': Decimal('0.7'),
    'E': Decimal('0.0')
}

# 啟動瀏覽器
driver = webdriver.Chrome()

try:
    # 打開登入頁面
    driver.get(login_url)

    # 等待頁面加載並找到帳號和密碼輸入框
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='THU-NID 帳號']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='THU-NID 密碼']")))

    # 輸入帳號和密碼
    username_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='THU-NID 帳號']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='THU-NID 密碼']")
    
    username_input.send_keys(username)
    password_input.send_keys(password)
    
    # 提交表單
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # 暫停腳本，等待手動完成驗證和登錄
    print("請手動完成驗證並登錄，完成後按下 Enter 繼續...")
    input()

    # 進入成績頁面
    driver.get(grades_url)

    # 等待成績頁面加載，處理可能的彈窗
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    except UnexpectedAlertPresentException:
        try:
            alert = driver.switch_to.alert
            print(f"Alert found: {alert.text}")
            alert.accept()
        except NoAlertPresentException:
            print("No alert present.")
        print("Session may be invalid. Exiting.")
        driver.quit()
        exit()

    # 解析頁面內容
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 找到id为 "no-more-tables" 的div
    grades_div = soup.find('div', id='no-more-tables')
    if not grades_div:
        print("未找到成績區塊，請檢查網頁結構")
        exit()

    # 找到成績表格
    grades_table = grades_div.find('table')
    if not grades_table:
        print("未找到成績表格，請檢查網頁結構")
        exit()

    # 解析表格内容
    grades = []
    processed_courses = {}  # 用於跟蹤已處理過的課程名稱和最低的GPA

    for row in grades_table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        row_content = [col.text.strip() for col in cols]
        print(f"Row content: {row_content}")

        # 只處理實際資料列
        if len(cols) == 6:
            year = cols[0].text.strip()
            semester = cols[1].text.strip()
            course_code = cols[2].text.strip()
            course_name = cols[3].text.strip()
            credits_text = cols[4].text.strip()
            try:
                # 去除不必要的字串並驗證資料
                credits = Decimal(credits_text)
            except InvalidOperation:
                print(f"Invalid credits value: {credits_text}")
                continue
            gpa = cols[5].text.strip()

            # 排除未通過的課程
            if gpa == '未過':
                continue

            # 特例處理：大一英文和國文課
            if course_name == '大一英文' or course_name == '中文：文學欣賞與實用':
                grades.append({'course_name': course_name, 'credits': credits, 'gpa': gpa})
                continue

            # 檢查課程名稱是否已處理過，如果處理過則更新成績為最低的GPA
            if course_name not in processed_courses:
                processed_courses[course_name] = {'course_name': course_name, 'credits': credits, 'gpa': gpa}
            else:
                existing_gpa = processed_courses[course_name]['gpa']
                if gpa_conversion.get(gpa, Decimal('4.3')) < gpa_conversion.get(existing_gpa, Decimal('4.3')):
                    processed_courses[course_name] = {'course_name': course_name, 'credits': credits, 'gpa': gpa}

    # 添加非特例课程到grades中
    for course_name, course_data in processed_courses.items():
        grades.append(course_data)

    # 計算學期總平均
    total_credits = Decimal('0')
    total_points = Decimal('0')

    for grade in grades:
        total_credits += grade['credits']  
        if grade['gpa'] in gpa_conversion:
            gpa_value = gpa_conversion[grade['gpa']]
            total_points += gpa_value * grade['credits']
            print(f"{grade['course_name']}: GPA={gpa_value} * 學分={grade['credits']} = {gpa_value * grade['credits']}")
        else:
            print(f"{grade['course_name']}: GPA={grade['gpa']} 不在 GPA 對應表中")

    semester_gpa = total_points / total_credits if total_credits > 0 else Decimal('0')

    print(f"總成績點數: {total_points}")
    print(f"總學分數: {total_credits}")
    print(f"學期總平均 GPA: {semester_gpa:.10f}")

finally:
    # 關閉瀏覽器
    driver.quit()
