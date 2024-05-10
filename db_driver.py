import psycopg2
import datetime as dt
try:
    con = psycopg2.connect(dbname='dleete', user='postgres', password='0000', host='localhost')
    cur = con.cursor()
except:
    class EmptyObject:
        pass
    con = EmptyObject()
    cur = EmptyObject()
    cur.execute = lambda _: None
    cur.fetchall = lambda: list()

def get_doctors():
    cur.execute('''SELECT * FROM "Doctor"''')
    return cur.fetchall()

def add_service(id:str, name:str, cost:str):
    query = f'''INSERT INTO "Service" ("service_id", "service_name", "cost")
                VALUES ('{id}', '{name}', {cost})'''
    cur.execute(query)
    con.commit()

def delete_service(id:str):
    query = f'''DELETE FROM "Service"
WHERE "Service".service_id='{id}';'''
    cur.execute(query)
    con.commit()

def update_service(id:str, name:str, cost:str):
    query = f'''UPDATE "Service"
SET service_name = '{name}', cost ={cost}
WHERE "Service".service_id = {id};'''
    cur.execute(query)
    con.commit()


def get_service():
    cur.execute('''SELECT * FROM "Service";''')
    return cur.fetchall()

def get_discount():
    cur.execute('''SELECT * FROM "DiscountCategory";''')
    return cur.fetchall()

def add_discount(id:str, name:str, cost:str):
    query = f'''INSERT INTO "DiscountCategory" ("service_type_id", "service_type", "discount")
                VALUES ('{id}', '{name}', {cost})'''
    cur.execute(query)
    con.commit()

def delete_discount(id:str):
    query = f'''DELETE FROM "DiscountCategory"
WHERE "DiscountCategory".service_type_id='{id}';'''
    cur.execute(query)
    con.commit()

def update_discount(id:str, name:str, discount:str):
    query = f'''UPDATE "DiscountCategory"
SET service_type = '{name}', discount = {discount}
WHERE "DiscountCategory".service_type_id = {id};'''
    cur.execute(query)
    con.commit()


def get_department():
    cur.execute('''SELECT * FROM "Department";''')
    return cur.fetchall()

def get_department():
    cur.execute('''SELECT * FROM "Department";''')
    return cur.fetchall()

def add_department(id:str, name:str):
    query = f'''INSERT INTO "Department" ("department_id", "department_name")
                VALUES ('{id}', '{name}')'''
    cur.execute(query)
    con.commit()

def delete_department(id:str):
    query = f'''DELETE FROM "Department"
WHERE "Department".department_id='{id}';'''
    cur.execute(query)
    con.commit()

def update_departent(id:str, name:str):
    query = f'''UPDATE "Department"
SET department_name = '{name}'
WHERE "Department".department_id = {id};'''
    cur.execute(query)
    con.commit()

#1 запрос
def get_diagnosises():
    cur.execute('''
SELECT 
    diagnosis_name,
    COUNT(*) AS count
FROM 
    "DiagnosisCodeVisit"
    JOIN "DiagnosisCode" ON "DiagnosisCodeVisit".diagnosis_id = "DiagnosisCode".diagnosis_id
    JOIN "Visit" ON "DiagnosisCodeVisit".visit_id = "Visit".visit_id
WHERE 
    TO_TIMESTAMP("Visit".start_time, 'YYYY-DD-MM') >= TIMESTAMP '2022-09-11' - INTERVAL '7 days'
GROUP BY 
    diagnosis_name
HAVING 
    COUNT(*) >= 10;
                ''')
    return cur.fetchall()

#2 запрос нет приода
def get_two_zapros(name: str, date1: str, date2: str):
    date1 = dt.datetime.strptime(date1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M') if date1 != '' else dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    date2 = dt.datetime.strptime(date2, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M') if date1 != '' else dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    query = f'''
SELECT
    "Doctor".id_doctor,
    "Doctor".last_name, "Doctor".first_name,  "Doctor".patronymic AS full_name,
    "Specialty".specialty_name
FROM "Doctor"
JOIN "DoctorSpecialty" ON "Doctor".id_doctor = "DoctorSpecialty".doctor_id
JOIN "Specialty" ON "DoctorSpecialty".specialty_id = "Specialty".specialty_id
WHERE Trim("Specialty".specialty_name) = '{name}' AND
    "Doctor".id_doctor NOT IN (
        SELECT DISTINCT
            "DoctorSchedule".doctor_id
        FROM "DoctorSchedule"
        WHERE "DoctorSchedule".start_time <= '{date1}'
            AND ("DoctorSchedule".end_time IS NULL OR "DoctorSchedule".end_time >= '{date2}'
    ));'''
    cur.execute(query)
    return cur.fetchall()


#3 запрос нет приода
def get_three_zapros(date1: str, date2: str):
    date1 = dt.datetime.strptime(date1, '%Y-%m-%d').date() if date1 != '' else dt.date.today()
    date2 = dt.datetime.strptime(date2, '%Y-%m-%d').date() if date2 != '' else dt.date.today()
    query = f'''
SELECT "Department".department_id, "Department".department_name,
COALESCE(SUM("Service".cost), 0) AS суммарный_доход,
COALESCE(SUM("Service".cost * (1 - "DiscountCategory".discount / 100)),0) AS размер_льготного_лечения
FROM "Department"
LEFT JOIN "DoctorDepartment" ON "Department".department_id = "DoctorDepartment".department_id
LEFT JOIN "Doctor" ON "DoctorDepartment".doctor_id = "Doctor".id_doctor
LEFT JOIN "Visit" ON "Doctor".id_doctor = "Visit".doctor_id
LEFT JOIN "Service" ON "Visit".service_id = "Service".service_id
LEFT JOIN "ServiceDiscount" ON "Service".service_id = "ServiceDiscount".service_id
LEFT JOIN "DiscountCategory" ON "DiscountCategory".service_type_id = "ServiceDiscount".service_type_id
WHERE TO_TIMESTAMP("Visit".start_time, 'YYYY-DD-MM') BETWEEN TIMESTAMP '{date1}' AND TIMESTAMP '{date2}'
GROUP BY "Department".department_id, "Department".department_name
ORDER BY суммарный_доход DESC;'''
    cur.execute(query)
    return cur.fetchall()



#4 запрос
def get_four_zapros():
    cur.execute('''
SELECT "Specialty".specialty_name,
  COALESCE(
    (
      SELECT COUNT(*)
      FROM "Visit"
      JOIN "Doctor" ON "Visit".doctor_id = "Doctor".id_doctor
      JOIN "DoctorSpecialty" ON "Doctor".id_doctor = "DoctorSpecialty".doctor_id
      WHERE "DoctorSpecialty".specialty_id = "Specialty".specialty_id), 0) AS количество_визитов,
  COALESCE(
    (
      SELECT TRIM("Visit".reason_for_visit)
      FROM "Visit"
      JOIN "Doctor" ON "Visit".doctor_id = "Doctor".id_doctor
      JOIN "DoctorSpecialty" ON "Doctor".id_doctor = "DoctorSpecialty".doctor_id
      WHERE "DoctorSpecialty".specialty_id = "Specialty".specialty_id
      GROUP BY "Visit".reason_for_visit
      ORDER BY COUNT(*) DESC
      LIMIT 1), '') AS обращение
FROM "Specialty"
WHERE COALESCE(
        (
          SELECT COUNT(*)
          FROM "Visit"
          JOIN "Doctor" ON "Visit".doctor_id = "Doctor".id_doctor
          JOIN "DoctorSpecialty" ON "Doctor".id_doctor = "DoctorSpecialty".doctor_id
          WHERE "DoctorSpecialty".specialty_id = "Specialty".specialty_id), 0) != 0
ORDER BY количество_визитов DESC''')
    return cur.fetchall()



# #5 вывод всех пациентов и их среднего чека в больнице НЕ работает средний чек
def get_five_zapros(id: str,date: str):
    date = dt.datetime.strptime(date, '%Y-%m-%d').date() if date != '' else dt.date.today()
    query = f'''
        SELECT 
  ("Patient".last_name) as фамилия, 
  ("Patient".first_name) as имя, 
  ("Patient".patronymic) as отчество,
  ("Service".service_name) as название_услуги, 
  ("Service".cost) as стоимость_услуги,
  ("Service".cost - "Service".cost * "DiscountCategory".discount / 100) as сумма_по_скидке,
  SUM("Service".cost - "Service".cost * "DiscountCategory".discount / 100) as итоговый_счет,
  ROUND(AVG("Service".cost - "Service".cost * "DiscountCategory".discount / 100)) as средний_счет,
  COUNT("Service".service_id)
FROM "Patient"
JOIN "MedicalCard" ON "Patient".patient_id = "MedicalCard".patient_id
JOIN "Visit" ON "MedicalCard".card_id = "Visit".card_id 
JOIN "Service" ON "Visit".service_id = "Service".service_id 
JOIN "ServiceDiscount" ON "Service".service_id = "ServiceDiscount".service_id
JOIN "DiscountCategory" ON "DiscountCategory".service_type_id = "ServiceDiscount".service_type_id and "Visit".service_type_id = "DiscountCategory".service_type_id
WHERE "Patient".patient_id = '{id}'
AND TO_TIMESTAMP("Visit".start_time, 'YYYY-DD-MM') = TIMESTAMP '{date}'
GROUP BY "Patient".last_name, "Patient".first_name,"Patient".patronymic, 
"Service".service_name, "Service".cost, "DiscountCategory".discount
ORDER BY итоговый_счет DESC;'''
    cur.execute(query)
    return cur.fetchall()


#6 запрос
def get_six_zapros(id: str):
    query = f'''
    SELECT "Visit".start_time as дата_обращения,
    "Doctor".last_name as "фамилия_врача", "Doctor".first_name as имя_вррача, "Doctor".patronymic as отчество_врача,
    "Visit".Reason_for_visit as причина_обращения, "DiagnosisCode".diagnosis_name as диагноз
    FROM "Patient"
    JOIN "MedicalCard" ON "Patient".patient_id = "MedicalCard".patient_id
    JOIN "Visit" ON "MedicalCard".card_id = "Visit".card_id
    JOIN "Doctor" ON "Visit".doctor_id = "Doctor".id_doctor
    JOIN "DiagnosisCodeVisit" ON "Visit".visit_id = "DiagnosisCodeVisit".visit_id
    JOIN "DiagnosisCode" ON "DiagnosisCodeVisit".diagnosis_id = "DiagnosisCode".diagnosis_id
    WHERE "Patient".patient_id = '{id}'; '''
    cur.execute(query)
    return cur.fetchall()


#7 запрос
def get_seven_zapros(id: str):
    query = f'''
SELECT "Doctor".last_name, "Doctor".first_name, "Doctor".patronymic, "DiagnosisCodeVisit".diagnosis_id,
"DiagnosisCode".diagnosis_name
FROM "Doctor"
JOIN "Visit" ON "Doctor".id_doctor = "Visit".doctor_id
JOIN "MedicalCard" ON "MedicalCard".card_id = "Visit".card_id
JOIN "DiagnosisCodeVisit" ON "Visit".visit_id = "DiagnosisCodeVisit".visit_id
JOIN "DiagnosisCode" ON "DiagnosisCode".diagnosis_id = "DiagnosisCodeVisit".diagnosis_id
WHERE "MedicalCard".patient_id = '{id}' '''
    cur.execute(query)
    return cur.fetchall()


# #8 запрос рейтинг врачей в целом НЕТ РЕЙТИНГА одного пациента
def get_eight_zapros(id: str):
    query = f'''
SELECT 
  "Doctor".last_name, "Doctor".first_name, "Doctor".patronymic,
  COALESCE(ROUND(AVG("Rating".rating), 2), 0) AS средний_рейтинг,
  CASE WHEN "Rating".patient_id = {id} THEN 'пациента'
    ELSE 'общий'
  END AS тип_рейтинга
FROM "Doctor"
LEFT JOIN "Rating" ON "Doctor".id_doctor = "Rating".doctor_id
WHERE "Rating".patient_id = {id} OR "Rating".patient_id <> {id}
GROUP BY  "Doctor".id_doctor, "Rating".patient_id
ORDER BY тип_рейтинга, средний_рейтинг DESC; '''
    cur.execute(query)
    return cur.fetchall()