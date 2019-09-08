# set up
  1. change project root folder name to Django_test
  2. ask for token.pkl file and put on the test_app folder
  3. create db.sqlite3 on root folder
  4. run python manage.py migrate to construct db shcema
  5. run python manage.py runserver

# API schema
  1. API說明-取得師傅可預約時間
    - 規格定義
      (1)	http://<server_ip>/freetime/get/
      (2) GET
    - Input
| data_class | data_type | data_sub_type |      資料      |
| ---------- | --------- | ------------- | -------------- |
| obs        | gis       |               | 九宮格         |
|||||
| obs        | geojson   | monitor       | 監控表格       |
| obs        | geojson   | lightning     | 閃電           |
|||||
| obs        | geojson   | ty_track      | 颱風路徑       |
|||||
| obs        | geojson   | max_rain      | 縣市最大雨量   |
| obs        | geojson   | max_rain      | 鄉鎮最大雨量   |
|||||
| geomap     | geojson   |               | 養工處轄區圖   |
| geomap     | geojson   |               | 氣象局台灣區域 |
    -Output
