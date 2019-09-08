# set up
  1. change project root folder name to Django_test
  2. ask for token.pkl file and put on the test_app folder
  3. create db.sqlite3 on root folder
  4. run python manage.py migrate to construct db shcema
  5. run python manage.py runserver

# API schema
  1. API說明-取得師傅可預約時間
     - 規格定義
       - (1)	http://<server_ip>/freetime/get/
       - (2) GET    
     - Input
        | 項次 |  資料名稱  |  類型  |         屬性        | 備註 |
        | ---- | --------- | ------ | ------------------- | ---- |
        | 1    | group_name | string | 使用者選擇的師傅群組 | 預設為A group |
     - Output
        | 項次 |  資料名稱  |  類型  |         屬性        | 備註 |
        | ---- | --------- | ------ | ------------------- | ---- |
        | 1    | status | string | 狀態 | success or fail | 
        | 2    | infos | list | 所有師傅有空時間字典 | |
     - Json格式
        ```json
        result = {'status' : 'success or fail', 
          'infos' : [{'master' : 'master_id_name',  
                  'datetime' : 'datetime_str'} 
                  ,{}]
          }
        ```