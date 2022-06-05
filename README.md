## 開発メモ
### データベースを直すときは
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```
で一層（Linuxシェルでやる）
```
mysql> drop database `django-db`;
mysql> create database `django-db`;
```
でDBをリセット
```
python manage.py makemigrations
python manage.py migrate
```
で再度マイグレーション