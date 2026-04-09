# Backend E-commerce Microservices (Django + DRF + UV)

Tai lieu nay huong dan ban demo du an tu A-Z bang Docker, Swagger va Postman.

## 1) Tong quan he thong

Du an gom 3 microservice chinh:

- auth_service: dang ky, dang nhap, lay thong tin nguoi dung.
- inventory_service: quan ly san pham va ton kho.
- order_service: gio hang, checkout, tao don hang.

Ha tang di kem:

- mysql: luu du lieu.
- redis: message broker/result backend cho Celery.
- order_celery_worker: xu ly tac vu nen (gui email thong bao tao don).

## 2) Cac file ban can biet

- Docker Compose: `docker-compose.yml`
- Docker JSON helper: `docker/docker-services.json`
- SQL khoi tao DB: `docker/mysql/init/01-create-databases.sql`
- Postman Collection: `postman/ecommerce-microservices.postman_collection.json`
- Bien moi truong: `.env` (tao tu `.env.example` neu can)

## 3) Chuan bi truoc khi demo

### 3.1 Cai dat cong cu

Ban can co san:

- Docker Desktop (dang chay)
- Postman
- Trinh duyet web (Chrome/Edge)
- (Tuy chon) MySQL Workbench neu muon xem DB truc tiep

### 3.2 Cau hinh file `.env`

Mo file `.env` o thu muc goc du an va dam bao cac bien toi thieu:

- `MYSQL_ROOT_PASSWORD`
- `JWT_SIGNING_KEY`
- `INVENTORY_INTERNAL_API_KEY`
- `ORDER_INVENTORY_INTERNAL_API_KEY`

Luu y quan trong:

- `ORDER_INVENTORY_INTERNAL_API_KEY` phai giong `INVENTORY_INTERNAL_API_KEY`.

Khuyen nghi:

- `MYSQL_HOST_PORT=3307` de tranh trung cong 3306 tren may ban.

## 4) Chay du an bang Docker (buoc dau tien)

Tai thu muc goc du an, mo terminal va chay:

```powershell
docker compose up -d --build
```

Kiem tra container:

```powershell
docker compose ps
```

Ban ky vong thay du 6 service:

- mysql
- redis
- auth_service
- inventory_service
- order_service
- order_celery_worker

Neu can xem log khi gap loi:

```powershell
docker compose logs -f auth_service
docker compose logs -f inventory_service
docker compose logs -f order_service
docker compose logs -f order_celery_worker
```

## 5) Kiem tra nhanh bang Swagger

Sau khi Docker len, mo trinh duyet va truy cap:

- Auth Swagger: `http://127.0.0.1:8001/api/docs/`
- Inventory Swagger: `http://127.0.0.1:8002/api/docs/`
- Order Swagger: `http://127.0.0.1:8003/api/docs/`

OpenAPI schema:

- Auth schema: `http://127.0.0.1:8001/api/schema/`
- Inventory schema: `http://127.0.0.1:8002/api/schema/`
- Order schema: `http://127.0.0.1:8003/api/schema/`

Neu 3 trang docs mo duoc, he thong da san sang demo.

## 6) Huong dan demo chi tiet bang Postman (A-Z)

## 6.1 Import collection

1. Mo Postman.
2. Bam Import.
3. Chon file: `postman/ecommerce-microservices.postman_collection.json`.
4. Xac nhan cac bien mac dinh trong Collection Variables:
   - `auth_base=http://127.0.0.1:8001`
   - `inventory_base=http://127.0.0.1:8002`
   - `order_base=http://127.0.0.1:8003`
  - `password` co the de mac dinh hoac doi.

Luu y de demo nhieu lan khong bi trung:

- Collection da co bien `auto_generate_demo_data=true` mac dinh.
- Moi lan ban chay request `01-01 Register`, Postman tu dong sinh moi:
  - `username`
  - `email`
  - `sku`
- Vi vay ban co the demo lap lai nhieu lan ma khong bi loi trung du lieu.
- Neu ban muon tu nhap tay du lieu co dinh, doi `auto_generate_demo_data=false`.

## 6.2 Chay dung thu tu request

Hay chay lan luot dung thu tu sau:

1. `01-01 Register` (tu dong tao username/email/sku moi)
2. `01-02 Login Token`
3. `01-03 Me`
4. `02-01 Create Product`
5. `03-02 Add To Cart`
6. `04-01 Checkout`
7. `04-02 List Orders`
8. `02-02 List Products`

## 6.3 Y nghia tung buoc

1) Register

- Tao tai khoan moi.
- Mac dinh se tu dong tao moi username/email moi, khong can sua tay.

2) Login Token

- Dang nhap lay JWT token.
- Script test trong collection se tu dong luu `token`.

3) Me

- Goi endpoint can auth de xac nhan token dang hoat dong.

4) Create Product

- Tao san pham moi o inventory_service.
- SKU duoc tao moi moi lan demo nen khong bi trung.
- Script test tu dong luu `product_id`.

5) Add To Cart

- Them san pham vua tao vao gio hang cua user hien tai.

6) Checkout

- order_service goi inventory_service de tru ton kho qua internal API key.
- Tao order va order items.

7) List Orders

- Kiem tra don hang vua tao da xuat hien.

8) List Products

- Kiem tra ton kho da giam sau checkout.

## 6.4 Ket qua mong doi khi demo thanh cong

- `6. Checkout` tra ve HTTP 201.
- Don hang co `status=CONFIRMED`.
- `7. List Orders` thay don vua tao.
- `8. List Products` thay `stock_quantity` giam dung theo so luong mua.

## 7) Kiem tra MySQL bang Workbench (tuy chon)

Neu muon kiem tra du lieu truc tiep:

- Host: `127.0.0.1`
- Port: `3307` (hoac `MYSQL_HOST_PORT`)
- Username: `root`
- Password: gia tri `MYSQL_ROOT_PASSWORD`

SQL tao/kiem tra schema thu cong:

```sql
CREATE DATABASE IF NOT EXISTS ecommerce_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS ecommerce_inventory CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS ecommerce_order CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES LIKE 'ecommerce_%';
```

Ghi chu:

- Lan dau chay Docker, cac schema duoc tao tu dong boi file `docker/mysql/init/01-create-databases.sql`.

## 8) Xu ly su co thuong gap

1. Khong mo duoc Swagger

- Kiem tra `docker compose ps` xem service co Up khong.
- Xem log service tuong ung bang `docker compose logs -f <service_name>`.

2. Loi ket noi MySQL

- Kiem tra `MYSQL_ROOT_PASSWORD` trong `.env`.
- Neu may ban dang dung cong 3306 cho MySQL local, dung `MYSQL_HOST_PORT=3307`.

3. Checkout bi loi 400/502

- Kiem tra 2 bien API key noi bo co giong nhau khong:
  - `INVENTORY_INTERNAL_API_KEY`
  - `ORDER_INVENTORY_INTERNAL_API_KEY`

4. Register bi bao trung user/email

- Doi `username`/`email` trong Collection Variables, sau do chay lai.

## 9) Lenh reset nhanh

Dung he thong:

```powershell
docker compose down
```

Dung va xoa ca data MySQL (reset sach):

```powershell
docker compose down -v
```

Chay lai tu dau:

```powershell
docker compose up -d --build
```

## 10) Checklist demo nhanh

1. Sua `.env` dung cac bien bat buoc.
2. Chay `docker compose up -d --build`.
3. Kiem tra `docker compose ps` thay du 6 service.
4. Mo 3 trang Swagger.
5. Import Postman collection.
6. Chay 8 request dung thu tu.
7. Xac nhan order tao thanh cong va ton kho giam.
